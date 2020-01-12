#######################################################################################
# NoteBook to compare the differents calibration for the RK angle
#
# input : the dataframe of each section expoted as CSV 
# output : graph of all the rk angle 
# note to distingish the different rk angle the column as the start time as suffix
# 
#######################################################################################

#%% import
from __future__ import print_function

import argparse
import sys
import time
import math
import glob
import os
import matplotlib.pyplot as plt

import pandas as pd


#%%  MAIN 
print("\n---START---")

Reload_file = False

Folder_path= 'test_rk/'

list_file= glob.glob(Folder_path+'*.csv')
tot_file=len(list_file)
print(" file found ("+ str(tot_file) +") :")
for name in list_file:
    print(name)

#list_file = ['sample_log/log_0_2019-9-14-21-54-24.ulg','sample_log/log_14_2019-9-24-23-31-14.ulg']
#%% sort list
def get_key(mstr):
    return int(mstr.split("/")[-1].split("-")[0])


list_file = sorted(list_file, key=get_key)


#%% 
dfg = pd.DataFrame()
i=0
for file_csv in  list_file:
    dfi = pd.read_csv(file_csv)
    dfi = dfi[['timestamp','time0_s','q[0]','q[1]','q[2]','q[3]','pitch','roll','yaw','rk_angle']]
    #print(dfi.info())

    #Merge Datafrme
    if len(dfg)==0:
        dfg=dfi
    else:
        dfg=pd.merge(dfg, dfi, on="timestamp" ,how='outer' ,suffixes=('', '-'+str(get_key(file_csv))))
        
        dfg.sort_values('timestamp',inplace=True)

# %% plot

#to popup graph if interactive :
#  %matplotlib qt
col_to_plot= dfg.filter(like='rk', axis=1).columns

dfg.plot(x="timestamp", y=col_to_plot, kind="line")


# %%
