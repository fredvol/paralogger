#coding:utf-8
"""
PARALOGER ANALYSIS 

File importing PX4 log.
also workable in Iteractive python

"""

# %% import , decorator and function
import numpy as np
import pandas as pd
import os.path
import time
import string

import logging
logger = logging.getLogger("import_Ulog")

from pyulog import ULog
from pyulog.px4 import PX4ULog

from functools import lru_cache

import quaternion

###  DECORATOR ####

def timeit(method):    # TODO use the one in model.py instead
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()       
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            logger.info('%r  %2.2f s' % \
                  (method.__name__, (te - ts) ))
        return result    
    return timed

### FUNCTIONS ###

@timeit
@lru_cache(maxsize=None)
def load_ulog_file(file_name):
    """ load an ULog file
    :return: ULog object
    """
    # The reason to put this method into helper is that the main module gets
    # (re)loaded on each page request. Thus the caching would not work there.

    # load only the messages we really need
    msg_filter = ['battery_status', 'estimator_status',
                  'sensor_combined', 'cpuload',
                  'vehicle_gps_position', 'vehicle_local_position',
                  'vehicle_global_position', 'vehicle_attitude', 
                  'vehicle_rates_setpoint', 
                  'vehicle_attitude_groundtruth',
                  'vehicle_local_position_groundtruth', 
                  'vehicle_status', 'airspeed', 
                  'rate_ctrl_status', 'vehicle_air_data',
                  'vehicle_magnetometer', 'system_power']

                  # has been removed , because useless:
                  #     position_setpoint_triplet
                  #     'actuator_controls_1' ,'actuator_controls_0','actuator_outputs'
                  #     distance_sensor
                  #     'vehicle_local_position_setpoint', 'vehicle_angular_velocity','vehicle_attitude_setpoint' 
                  #     'tecs_status'
                  #     'rc_channels', 'input_rc',
                  #     'manual_control_setpoint','vehicle_visual_odometry'
    try:
        ulog = ULog(file_name, msg_filter, disable_str_exceptions=False)
    except FileNotFoundError:
        print("Error: file %s not found" % file_name)
        raise

    # catch all other exceptions and turn them into an ULogException
    except Exception as error:
        traceback.print_exception(*sys.exc_info())
        raise ULogException()

    # filter messages with timestamp = 0 (these are invalid).
    # The better way is not to publish such messages in the first place, and fix
    # the code instead (it goes against the monotonicity requirement of ulog).
    # So we display the values such that the problem becomes visible.
#    for d in ulog.data_list:
#        t = d.data['timestamp']
#        non_zero_indices = t != 0
#        if not np.all(non_zero_indices):
#            d.data = np.compress(non_zero_indices, d.data, axis=0)

    return ulog

def add_rk_angle(df_i,mask):
    """    
    This function returns best guessed vertical vector r of PIX4 device in PIX4 coordinate (r_BX) calculated within the mask range
    It also adds 1 column with r angle to Geo vertical (=acos(r.k)) for the all df_i
    """
    #minimum acceptable value for the mean of the guessed vertical vector dot product with the Geo vertical vector
    #event if r_BGeo is actually vertical when flying strait the mean dot product is < 1 because when turning it is < 1
    #value 0.92 is to be ajusted TODO
    min_mean_r_BGeo_z = 0.92

    df_m = df_i.loc[mask].copy()
    df = df_i.copy()

    # Read quaternions from PIX4 log
    q4_array_m = np.array(df_m[["q[0]","q[1]","q[2]","q[3]"]])
    q_array_m = quaternion.as_quat_array(q4_array_m)

    q4_array = np.array(df[["q[0]","q[1]","q[2]","q[3]"]])
    q_array = quaternion.as_quat_array(q4_array)
    # for each timestep the matrix is the BX base (u,v,w) expressed in BGeo base (i,j,k) therefore it is an array of matrices
    # [[u.i v.i w.i]
    #  [u.j v.j w.j]
    #  [u.k v.k w.k]]
    mat_rot_array_m = quaternion.as_rotation_matrix(q_array_m) 
    mat_rot_array = quaternion.as_rotation_matrix(q_array) 

    """
    # We are going to add colums to the df
    # nine columns will be added for the rotation matrice where the BX base (u,v,w) expressed in BGeo base (i,j,k)
    # three columns containing the mean vertical vector (which hopefully is the r vector in BP the parapente base (p,q,r)) 
    # in the BGeo base, and one for the angle between this one and the vertical vector k. 13 columns altogether
    Store in df as columns u.i,u.j,u.k,v.i,v.j,v.k,w.i,w.j,w.k 
    uvw_array=np.zeros((len(df.index),9))

    for i in range(0,len(df.index)):
        for j in range(0,3):
            for k in range(0,3):
                uvw_array[i,3*j+k]=mat_rot_array[i,k,j] 
    #print(mat_rot_array[0])  
    #print(str(uvw_array[0]) + "\n")
    df.loc[:,"ui"]=uvw_array[:,0]
    df.loc[:,"uj"]=uvw_array[:,1]
    df.loc[:,"uk"]=uvw_array[:,2]
    df.loc[:,"vi"]=uvw_array[:,3]
    df.loc[:,"vj"]=uvw_array[:,4]
    df.loc[:,"vk"]=uvw_array[:,5]
    df.loc[:,"wi"]=uvw_array[:,6]
    df.loc[:,"wj"]=uvw_array[:,7]
    df.loc[:,"wk"]=uvw_array[:,8] 
    #print(df.head(3))
    """
    # we are going to find the vector r expressed in BX which is the best we can find as the 3rd vector in the BP base (p,q,r)
    # r = au+bv+cw with r_BX=(a,b,c) coord of r in BX are found thank to mu and lam coming rom partial derivatives=0 on r_BX.k
    mean_rot_mat_m = np.mean(mat_rot_array_m, axis=0)
    #print("\n mean_rot_mat : " )
    #print(mean_rot_mat)
    #print("\n moyennes : \n" )
    #print("ui_vi_wi_mean=" + str(mean_rot_mat[0]))
    #print("uj_vj_wj_mean=" + str(mean_rot_mat[1]))
    #print("uk_vk_wk_mean=" + str(mean_rot_mat[2]))
    # mu and lam calculation to find optimal vertical guessed vector r which maximises r.k
    mu=np.arctan2(mean_rot_mat_m[2,2],mean_rot_mat_m[2,1])
    lam=np.arctan2(mean_rot_mat_m[2,1]*np.cos(mu)+mean_rot_mat_m[2,2]*np.sin(mu),mean_rot_mat_m[2,0])
    #print("mu = " + str(mu) + "     lam = " + str(lam) + "\n")
    r_BX_m=np.array([np.cos(lam), np.sin(lam)*np.cos(mu), np.sin(lam)*np.sin(mu)]) #[a,b,c]=[cos(lam),sin(lan)cos(mu),sin(lam)sin(mu)]
    mean_r_BGeo_m = mean_rot_mat_m@r_BX_m
    
    if mean_r_BGeo_m[2] < 0:
        logger.info("r_BX is upside down we are changing to -r_BX")
        r_BX_m=-r_BX_m #r_BX we found is the opposite of vertical still it is vertical

    if mean_r_BGeo_m[2] < min_mean_r_BGeo_z: #mean(r.k)=mean_r_BGeo[2] has to be near but cannot be 1.0
        logger.info("WARNING : vertical_vector r might not have been guessed correctly, mean_r_BGeo_m = " + str(mean_r_BGeo_m))
        #print("r_BX : r_BX = " + str(r_BX) + "\n")
    else:
        logger.info("vertical_vector r seems correct, mean_r_BGeo_m = " + str(mean_r_BGeo_m))
    
    r_BGeo_array=np.zeros((len(df.index),3))
    for i in range(0,len(df.index)):
        r_BGeo_array[i] = mat_rot_array[i]@r_BX_m
        #print("r_BGeo_array[0] = " + str(r_BGeo_array[0]))
        #print("r_BGeo_array[1] = " + str(r_BGeo_array[1]))
    """
    df.loc[:,"ri"]=r_BGeo_array[:,0]
    df.loc[:,"rj"]=r_BGeo_array[:,1]
    df.loc[:,"rk"]=r_BGeo_array[:,2]
    """    
    # Now we put a column with arccos(r.k) which is the angle between the mean vertical and the actual vertical 
    df.loc[:,"rk_angle"]=np.arccos(r_BGeo_array[:,2])

    df_i["rk_angle"] = df["rk_angle"]
    logger.debug(df_i[["time0_s","rk_angle"]].head(5))
    return(r_BX_m)




#%% PARAMETERS 

gravity = 9.80665 #m·s-2


# %% Main Functions    ##############################################
@timeit
def ulog_list_data(file_path):
    """ Create a panda dataframe with all the record avaible,
     the number and frequency.
    """
    logger.info("\n Ulog ulog_list_data: " +str(file_path))

    ulog = load_ulog_file(file_path)
    logger.debug(ulog)

    time_s= int((ulog.last_timestamp - ulog.start_timestamp)/1e6)
    logger.info("time_s: ",time_s)

    data = []
    data_list_sorted = sorted(ulog.data_list, key=lambda d: d.name + str(d.multi_id))
    for d in data_list_sorted:
        parent_id = "{:}".format(d.name)
        for d2 in d.data:
            try:
                size = d.data[d2].size
                avg = np.mean(d.data[d2])
                std = np.std(d.data[d2])
            except:
                print("")

            name_id = "{:}".format(d2)
            data.append(dict({'parent': parent_id, 'name':name_id, 'size':size ,'frequency':size / time_s , 'avg':avg ,'std':std }))

    df = pd.DataFrame(data)
    return df


def ulog_param(file_path):
    """ Extract all the parameters of the Ulog
    """

    logger.info("\n Ulog_param: " +str(file_path))
    dict_param={}

    ulog = load_ulog_file(file_path)

    dict_param['initial_parameters'] = ulog.initial_parameters
    dict_param['msg_info_dict'] = ulog.msg_info_dict
    dict_param['logged_messages'] = ulog.logged_messages
    dict_param['file_corruption'] = ulog.file_corruption
    dict_param['logged_messages'] = ulog.logged_messages

    return dict_param


@timeit
def ulog_to_df(file_path):
    """ Created a Panda dataframe with all the interestion data
        All the data are join by the timestamp
        """
    logger.info("generated_dataFrame_Ulog from: " +str(file_path))

    ulog = load_ulog_file(file_path)
    px4_ulog = PX4ULog(ulog)
    px4_ulog.add_roll_pitch_yaw()

    #Dict to list all the interesting parameters to extract
    dict_param_to_get ={'vehicle_attitude' : ['timestamp','q[0]','q[1]','q[2]','q[3]','pitch','roll','yaw','yawspeed' ],
                        'vehicle_local_position' : ['timestamp','x','y','z','ax','ay','az' ],   
                        'vehicle_gps_position': ['timestamp','time_utc_usec','lat','lon','alt','hdop','vdop','fix_type','satellites_used' ],
                        'vehicle_air_data' : ['timestamp','baro_alt_meter','baro_temp_celcius','baro_pressure_pa','rho' ] 
    }

    df_G = pd.DataFrame(columns=['timestamp'])

    # For each cetgory : vehicle_attitude ,vehicle_local_position , etc ..
    for key in dict_param_to_get:
        logger.info("fetching category: " + str(key))

        data_category = ulog.get_dataset(key)

        data={ }

        # For data in cetgory : timestamp ,q[0] , etc ..
        for param in dict_param_to_get[key]: 
            logger.info("\t fetching data: " + str(param))

            data[param] = data_category.data[param]

        # Create DataFrame 
        dfi = pd.DataFrame(data) 
        logger.debug('\n--------\n DF for : ' + str(key))
        #logger.debug(dfi)
        
        #Merge Datafrme
        df_G=pd.merge(df_G, dfi, on="timestamp" ,how='outer')
        
        df_G.sort_values('timestamp',inplace=True)

    #interpolated some misinsg value 
    #euler angle and quaternion
    df_G['pitch'].interpolate(method='linear',inplace=True)
    df_G['roll'].interpolate(method='linear',inplace=True)
    df_G['yaw'].interpolate(method='linear',inplace=True)

    df_G['q[0]'].interpolate(method='linear',inplace=True)
    df_G['q[1]'].interpolate(method='linear',inplace=True)
    df_G['q[2]'].interpolate(method='linear',inplace=True)
    df_G['q[3]'].interpolate(method='linear',inplace=True)

    df_G['ax'].interpolate(method='linear',inplace=True)
    df_G['ay'].interpolate(method='linear',inplace=True)
    df_G['az'].interpolate(method='linear',inplace=True)

    df_G['baro_alt_meter'].interpolate(method='linear',inplace=True)
    df_G['az'].interpolate(method='linear',inplace=True)
    df_G['az'].interpolate(method='linear',inplace=True)

    #Find first row with quaternion
    df_G.dropna(subset=['q[0]'], inplace=True)

    ## Create additional data
    #Created a time 0 column
    df_G['time0_s']= (df_G['timestamp'] - df_G.iloc[0]['timestamp'])/10**6  #timestamp are in micro second

    # Compute nb of G
    df_G['nbG_x'] = df_G['ax'] / gravity 
    df_G['nbG_y'] = df_G['ay'] / gravity
    df_G['nbG_z'] = df_G['az'] / gravity

    df_G['nbG_tot'] = np.linalg.norm(df_G[['nbG_x','nbG_y','nbG_z']].values,axis=1)

    #Convert to more convential unit
    df_G['alt'] = df_G['alt'] / 1e3 #Convert altitude to meter

    #Calculate absolute angle to vertical ----- NO this is done during section calibration now
    #add_rk_angle(df_G)

    #move time 0 column to the begining of the table
    time0s = df_G['time0_s']
    df_G.drop(labels=['time0_s'], axis=1,inplace = True)
    df_G.insert(1, 'time0_s', time0s)


    logger.debug(df_G.info())

    return df_G



# %% Main RUN
if __name__ == "__main__":
    log_name = "log_23_2019-11-26-12-09-10.ulg"

    cwd = os.path.dirname(os.path.abspath(__file__))
    logger.info('cwd:' + cwd)
    ulog_file_path = os.path.join(cwd, "samples", log_name)
    logger.info('ulog_file_path:' + ulog_file_path)

    df = ulog_to_df(ulog_file_path)

    #Export  the result dataframe  in csv 
    df.to_csv("full_dataFrame.csv")

    #Making a dataframe containg the name of the parameters
    df_list_param = ulog_list_data(ulog_file_path)
    df_list_param.to_csv("list_param.csv")
