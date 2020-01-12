#%% import

from __future__ import print_function

import argparse
import sys
import time
import math
import glob
import os

import pandas as pd


#%%  MAIN 
print("\n---START---")

Reload_file = False

Folder_path= ''


list_file= glob.glob(Folder_path+'*.csv')
tot_file=len(list_file)
print(" file found ("+ str(tot_file) +") :")
for name in list_file:
    print(name)

#list_file = ['sample_log/log_0_2019-9-14-21-54-24.ulg','sample_log/log_14_2019-9-24-23-31-14.ulg']


#%% 
dfg = pd.DataFrame()
i=0
for file_csv in  list_file:
    pdi = pd.read_csv(file_csv)
    print(pdi.info())

# %%
