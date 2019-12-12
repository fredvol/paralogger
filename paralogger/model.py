#coding:utf-8
"""
PARALOGER ANALYSIS 

Model file 

"""

import datetime
import hashlib
import json
import logging
import os.path
import pkgutil
import platform
import random
import string
import sys
import time

import numpy as np
import pandas as pd
import pip

from import_ulog import ulog_list_data, ulog_param, ulog_to_df
from list_param import Device, Kind, Position

logger = logging.getLogger("model")

# Local imports:


############################# DECORATOR #############################


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            logger.info("%r  %2.2f s" % (method.__name__, (te - ts)))
        return result

    return timed


############################# DEFINITIONS #############################


def id_generator(msize=6, chars=string.ascii_uppercase + string.digits):
    """ Generate a random ID .

    Parameters:
        msize (str): length of the random string.
        chars (list of string): the list of the possible characters

    :Returns:
        id_str(str): the random string   
    """

    id_str = "".join(random.choice(chars) for _ in range(int(msize)))
    return id_str


def sha256sum(filename):
    """ Compute the sha256 of the a file.
    Usefull to refind source file , or detect duplicate one

    Parameters:
        filename (str):The file path.

    :Returns:
        sha(str): tHe sha256 hars string   
    """
    # compute the SH256 of the file  to identify possible duplicated source file.
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def getSystemInfo():
        try:
            info={}
            info['platform']=platform.system()
            info['platform-release']=platform.release()
            info['platform-version']=platform.version()
            info['architecture']=platform.machine()
            info['processor']=platform.processor()

            info['python version:'] =sys.version
            info['modules:']=list(sys.modules.keys())

            return json.dumps(info)
        except Exception as e:
            logging.exception(e)

############################# MAIN MODEL #############################


class Flight:
    """THis is the main class representing one Flight
    
    """
    def __repr__(self):
        return str(self.__dict__)

    def __init__(self):
        logger.info("initialise empty Flight ")

        self.id = id_generator()
        self.createdDate = time.time()

        self.manufacturer = None    # Glider Manufacturer
        self.glider = None          # Glider model name
        self.size = None            # Glider Size info ( 24, XL)
        self.modif = None           # Glider modification version  
        self.pilot = None           # Pilot name
        self.weight = None          # Pilot all up weight
        self.location = None        # Testing place
        self.laboratory = None      # Labo name

        self.data = []              # List of all the data file

        self.sections = []          # List of Sections object

        self.flight_version = 2     # version of the data model

    @timeit
    def add_data_file(self, mfilePath, mdevice, mposition):
        """Add detail of a log file and process it
        
        Arguments:
            mfilePath {str} -- log file path
            mdevice {str} -- Device information
            mposition {str} -- Position of the device during the flight info
        """
        mData_File = Data_File(mfilePath, mdevice, mposition) # Crete the object Data file 
        mData_File.populate_df()  # Process the raw data
        mData_File.populated_device_param() # Extrcat the paramters  of the device.

        self.data.append(mData_File)

    def add_info(self, mmanufacturer, mglider,msize, mmodif, mpilot, mweight, mlocation,mlabo):
        """ Add Mete information on the flight
        This function can be remplce by a constructor
        
        Arguments:
            mmanufacturer {str} 
            mglider {str} 
            msize {str} 
            mmodif {str} 
            mpilot {str} 
            mweight {float} 
            mlocation {str} 
            mlabo {str} 
        """
        self.manufacturer = mmanufacturer
        self.glider = mglider
        self.size = msize
        self.modif = mmodif
        self.pilot = mpilot
        self.weight = mweight
        self.location = mlocation
        self.laboratory = mlabo


    def get_df_by_position(self, mposition):
        """Return the dataframe  for a given position (glider, pilot)
        
        Arguments:
            mposition {str} -- Device position during test flight
        
        Returns:
            List of dataframe   
            Empty list of no dataframe are avaible at th is position

        ? maybe shoul return a Datafrale and not a list , wiil we have 2 device at same place?
        """
        df_to_return = []
        for dataf in self.data:
            if dataf.position == mposition:
                df_to_return.append(dataf.df)
            
        return df_to_return

    def apply_section(self,uid,time_calibrate=5):
        """Generate a dataframe from the main dataframe with section detail
        
        Arguments:
            uid {str} -- Section ID to section to apply
        
        Keyword Arguments:
            time_calibrate {int} -- Time in second for performing calibration (default: {5})
        
        Returns:
            DataFrame -- Dataframe truncate for the section with value calibrated 
                        ( a standalone dataframe not a view on the main one)
        
        """

        mSection= self.section_by_id(uid)
        t_start,t_end = mSection.get_start_end()
        t_start,t_end =float(t_start),float(t_end)
        mdf = self.get_df_by_position(Position.PILOT)[0]
        df_plot = mdf.loc[mdf["lat"].notnull()]

        mSection.set_calibration(df_plot,t_start , t_start + time_calibrate)
        dict_calibration = mSection.get_calibration() 


        df_plot['pitch'] = df_plot['pitch'] - dict_calibration['pitch']
        df_plot['roll'] = df_plot['roll'] - dict_calibration['roll']

        mask = (df_plot["time0_s"] > t_start) & (df_plot["time0_s"] <= t_end)
        df_plot_sel = df_plot.loc[mask].copy()

        return df_plot_sel


    def add_general_section(self , time_min=None ,time_max=None, mkind =Kind.MISC):
        """Add a Section objet to the Flight object
        Using realative time of the dataframe : time0
        
        Keyword Arguments:
            time_min {float} -- Section 's start time in second (default: {None})
            time_max {float} -- Section 's end time in second  (default: {None})

            In None selected 0s to max time .
             ! This in the future will several df per Flight should be improve  and maybe use UTC time?
        """

        if not len(self.data)==0:
            
            df=self.data[0].df   #TODO Nedd to better selection , shorter one?  pilot one? 
            
            if time_min == None:
                time_min = df['time0_s'].min()
            if time_max == None:
                time_max = df['time0_s'].max()

            mSection= Sections(time_min,time_max,mkind)
            self.sections.append(mSection)
            
        else:
            logger.info("Impossible to create section, Data is empty")

    def delete_section(self, uid):
        self.sections = [i for i in self.sections if i.id!=uid]

    def section_by_id(self, uid):
        """Return Section object for a given ID
        
        Arguments:
            uid {str} -- Id of the section to Return
        
        Returns:
            Section
        """
        section_to_return = [i for i in self.sections if i.id == uid]
        return section_to_return[0]  
    
    def list_section(self):
        """Export the list of section  to list
        
        Returns:
            list -- list of flight sections
        """
        section_list=[]
        
        for sect in self.sections:
            section_list.append([sect.start,sect.end,sect.kind.name])

        return section_list

    def import_list_section(self,lst_section):
        """Import section list
        import list look like that: [['180', 539.1488, 'MISC'], ['250', '306', 'MISC']]
        
        Arguments:
            lst_section {list} -- list of sections to import
        """
        if len(lst_section) > 0:

            for sect in lst_section:
                mSection = Sections(sect[0],sect[1],getattr(Kind, sect[3], Kind.MISC) )
                self.sections.append(mSection)
        else:
            logger.info("list of section to import is empty")




class Sections:
    """Section object store the detail sof the interesting part of the flight.

    """
    def __repr__(self):
        return '%s (%s,%s) ' % (self.kind, self.start , self.end)

    def __init__(self, start = None , end=None , kind=None):

        self.id = id_generator()    # Unique ID
        self.kind = kind            # Kind of manoeuvre ( frontal asymetric collapse , etc...)
        self.start = start          # start time
        self.end = end              # End time 
        self.version = 1            # version of the Sections model
        self.calibration = {"pitch" : 0 , "roll" :0 , "yaw" : 0 } # Calibration data for the Section

    def get_start_end(self):
        return (self.start, self.end)

    def set_calibration(self,df, t_start=0 ,t_end =5):
        """Give the average value on a part of the section.
        Used to calibrate the Section, will be used to compasente the mounting offset during testing.
        
        Arguments:
            df {Dataframe} -- Datafrme to extract the calibration
        
        Keyword Arguments:
            t_start {int} -- calibration start time (default: {0})
            t_end {int} -- Calibration end time (default: {5})
        
        Returns:
            Dict -- Average values

        ! In the future will be better to use the Quaternion instead of the euler angle TODO
        """
        mask = (df["time0_s"] > t_start) & (df["time0_s"] <= t_end)


        avg_pitch = df.loc[mask, 'pitch'].mean()
        avg_roll = df.loc[mask, 'roll'].mean()
        avg_yaw = df.loc[mask, 'yaw'].mean() # Yaw need to be calibrated using the GPS track. TODO

        if (avg_pitch == None or avg_roll == None or avg_yaw == None):
            logger.warning("Calibration failed section: " + self.__repr__)

        logger.info( " calibrating  from time0_s: " + str(t_start) + "s to : " + str(t_end) + " s" )
        logger.debug( ' avg_pitch :' + str(avg_pitch) + " rad so: " + str(np.rad2deg(avg_pitch)) + " deg")
        logger.debug( ' avg_roll :' + str(avg_roll) + " rad so: " + str(np.rad2deg(avg_roll)) + " deg")
        #logger.debug( ' avg_yaw :' + str(avg_yaw) + " rad so: " + str(np.rad2deg(avg_yaw)) + " deg" + " wanted (deg): "+ str(start_yaw_angle_deg))
        
        self.calibration = {"pitch" : avg_pitch , "roll" :avg_roll , "yaw" : avg_yaw }
        return {"pitch" : avg_pitch , "roll" :avg_roll , "yaw" : avg_yaw }
    
    def get_calibration(self):
        return self.calibration

        

class Data_File:
    """Data file object  hold the detail of the file containing the raw data and the data processed in a dataframe
    
    """

    def __init__(self, mfilePath, mdevice, mposition):
        logger.info("Data_File ")

        self.file_path = mfilePath  # Path of the raw log file
        self.file_date = None       # Date of file creation
        self.file_sha1 = None       # Hash of the file , for retrieve if lost , move or rename
        self.device = mdevice       # Device name { str)}
        self.device_sn = None       # serial number of the devices
        self.device_param = None    # Device parameters during test flight
        self.position = mposition   # Position of the device during the testflight ( pilot , glider) 

        self.df = None              # Dataframe holding the imported and processed data
        self.version = 2          # version of the Data_File model

        self.file_sha1 = sha256sum(self.file_path) 

        self.file_date = time.ctime(os.path.getctime(self.file_path))


    def __repr__(self):
        return '%s (%s) ' % (self.position, str(self.df.shape))

    def populate_df(self):
        """Function importing raw data form log file
        """
        logger.info("populate_df ")
        if self.device == Device.PIXRACER:
            self.df = ulog_to_df(self.file_path)

    def list_available_data(self):
        """ List all the data avaible in the log file"""
        if self.device == Device.PIXRACER:
            return ulog_list_data(self.file_path)

    def populated_device_param(self):
        """ Function importing all the parameters of the device"""
        if self.device == Device.PIXRACER:
            self.device_param = ulog_param(self.file_path)

    def get_start_end_time(self):
        """
        return the start and end timestamp in s of the log file 
        """
        timestamp_start = (
            self.df[~self.df["time_utc_usec"].isnull()].iloc[0]["time_utc_usec"]
            / 10 ** 6
        )
        timestamp_end = (
            self.df[~self.df["time_utc_usec"].isnull()].iloc[-1]["time_utc_usec"]
            / 10 ** 6
        )

        return {"timestamp_start": timestamp_start, "timestamp_end": timestamp_end}

class Video_File:
    """Object to store video file info, WIP
    

    """
    def __repr__(self):
        return '%s' % (self.device)

    def __init__(self, mfilePath, mdevice):
        logger.info("Data_File ")

        self.version = 1  # version of the Video_file model
        self.file_path = mfilePath
        self.file_date = None
        self.file_sha1 = None
        self.device = mdevice

        self.file_sha1 = sha256sum(self.file_path)

        self.file_date = time.ctime(os.path.getctime(self.file_path))



