#coding:utf-8
"""
PARALOGER ANALYSIS 

NB_aplycriteria 
This notebook  help to develope the ctriteria aplication 
means giving a letter  to a manoeuvre according to criteria 
 ex: pitch angle > 45 -> C class

 WIP

 Note the array given to the bisect.bisect should be ascendant order
"""

#%% import
import bisect
import json
import logging
import pickle

import jsonpickle
import numpy as np

from judge import Judge
from model import Flight, Sections

log_file_name ="NB_apply_crit.log"
def config_logger():
    """Logger configuration.
    log in a file + send to debug console + send to log tab in the app
    """
    logger = logging.getLogger()
    # logging.basicConfig(filename='1_import.log',level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(module)s :: %(funcName)s ::  %(message)s")
    file_handler = logging.handlers.RotatingFileHandler(log_file_name, "a", 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Redirect log on console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    return logger


logger = config_logger()

#%% run
def grade(score, mbreakpoint=[60,70,80,90], grades='FDCBA'):
    i = bisect.bisect_left(mbreakpoint,score)
    return grades[i]

#[grade(score) for score in [33,99,77,70,89,90,100]]
#[grade(score, [100 , 200, 300 , 400],['A' , 'B', 'C' , 'D','F'])for score in [1,100,290,1000]]
#[grade(score, [-500 , -300, -300 , -100],['F' , 'D', 'C' , 'B','A'])for score in [-1,-100,-290,-990]]

# %% Create criteria book


criteria_dict_book = {}
criteria_misc = { 1: 
        {
        'name' : 'Altitude lost',
        'unit' : 'm',
        'function' : 'altitude_lost',
        'breakpoint' : [-100 , -60, -40 , -20],
        'rates' : ['F' , 'D', 'C' , 'B','A'],
        } ,
        2: {
        'name' : 'Maximun pitch',
        'unit' : '°',
        'function' : 'pitch_max',
        'breakpoint' : [20 , 30, 45 , 50],
        'rates' : ['A' , 'B', 'C' , 'D'],
        }  
    }

criteria_spiral = { 1:
        {
        'name' : 'Altitude lost',
        'unit' : 'm',
        'function' : 'altitude_lost',
        'breakpoint' : [-500 , -400, -300 , -200],
        'rates' : ['F' , 'D', 'C' , 'B','A'],
        } , 
        2: {
        'name' : 'Maximun nb_g',
        'unit' : '°',
        'function' : 'max_nbG',
        'breakpoint' : [2 , 3, 4 , 5,6],
        'rates' : ['A' , 'B', 'C' ,'D','F'],
        } 
    }

criteria_dict_book['Misc'] = criteria_misc
criteria_dict_book['Asym'] = criteria_misc
criteria_dict_book['Frontal'] = criteria_misc
criteria_dict_book['Spiral'] = criteria_spiral

with open('crit_book.json', 'w') as fp:
    json.dump(criteria_dict_book, fp)
#json_data = json.dumps(criteria_dict_book)


#%% load flight

flight = None 

pikle_path = "Flight2_gourdon_v0-2-0.pkl"

with open(pikle_path, 'rb') as pickle_file:
    flight = pickle.load(pickle_file)


# # %% function
# class Judge :

#     def altitude_lost(mdf,mbreakpoint,mrates):
#         start_altitude = mdf["alt"].iloc[0]
#         val = mdf['alt'].min() - start_altitude
#         mgrade = grade(val, mbreakpoint,mrates) 
#         return {'value' : val , 'grade':mgrade}


#     def pitch_max(mdf,mbreakpoint,mrates):
#         val = np.rad2deg(abs(df['pitch'].max()))
#         mgrade = grade(val, mbreakpoint,mrates) 
#         return {'value' : val , 'grade':mgrade}


#     def max_nbG(mdf,mbreakpoint,mrates):
#         val = abs(df['nbG_tot'].max())
#         mgrade = grade(val, mbreakpoint,mrates) 
#         return {'value' : val , 'grade':mgrade}

# #%% process
# for sect in flight.sections:

#     print("\n section:" , sect)

#     #get list of criteria
#     df = flight.apply_section(sect.id)
#     dict_crit= criteria_dict_book[sect.kind.value]
    

#     for key, details in dict_crit.items():
#         method_to_call = getattr(Judge, details['function'])
#         result = method_to_call(df,details['breakpoint'], details['rates'])
#        # result = altitude_lost(df,details['breakpoint'], details['rates'])
#         print(details['name'],result)


# %% using class 


path_file = "crit_book.json"

jdg = Judge()

jdg.dict_criteria = criteria_dict_book

jdg.save_judge("judge1.json")

# %%
jdg2=Judge()

print(jdg2)
jdg2.load_judge('judge1.json')

print(jdg2)


# %%
