#coding:utf-8
"""
PARALOGER ANALYSIS 

NB_aplycriteria 
This notebook  help to devvelope the ctriteria aplication 
"""
#%% import
import bisect
import pickle
from model import Flight, Sections 
import json


#%% run
def grade(score, breakpoint=[60,70,80,90], grades='FDCBA'):
    i = bisect.bisect(breakpoint,score)
    return grades[i]

#[grade(score) for score in [33,99,77,70,89,90,100]]


# %% Create criteria book


criteria_dict_book = {}
criteria_misc = { 1: 
        {
        'name' : 'Altitude lost',
        'unit' : 'm',
        'function' : 'altitude_lost',
        'breakpoint' : [20 , 30, 40 , 100],
        'rates' : ['A' , 'B', 'C' , 'D','F'],
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
        'breakpoint' : [100 , 200, 300 , 400],
        'rates' : ['A' , 'B', 'C' , 'D','F'],
        } , 
        2: {
        'name' : 'Maximun nb_g',
        'unit' : '°',
        'function' : 'max_nbG',
        'breakpoint' : [2 , 3, 4 , 5],
        'rates' : ['A' , 'B', 'C' , 'D'],
        } 
    }

criteria_dict_book['Misc'] = criteria_misc
criteria_dict_book['Spiral'] = criteria_spiral

with open('crit_book.json', 'w') as fp:
    json.dump(criteria_dict_book, fp)
#json_data = json.dumps(criteria_dict_book)


#%% load flight

flight = None 

pikle_path = "Flight2_gourdon_v3_2.pkl"

with open(pikle_path, 'rb') as pickle_file:
    flight = pickle.load(pickle_file)


# %% function
class Judge :

    def altitude_lost(mdf,breakpoint,rates):
        val = df['alt'].min()
        mgrade = grade(val, breakpoint,rates) 
        return {'value' : val , 'grade':mgrade}


    def pitch_max(mdf,breakpoint,rates):
        val = df['pitch'].max()
        mgrade = grade(val, breakpoint,rates) 
        return {'value' : val , 'grade':mgrade}


    def max_nbG(mdf,breakpoint,rates):
        val = df['pitch'].max()
        mgrade = grade(val, breakpoint,rates) 
        return {'value' : val , 'grade':mgrade}

#%% process
for sect in flight.sections:

    print("\n section:" , sect)

    #get list of criteria
    df = flight.apply_section(sect.id)
    dict_crit= criteria_dict_book[sect.kind.value]
    

    for key, details in dict_crit.items():
        method_to_call = getattr(Judge, details['function'])
        result = method_to_call(df,details['breakpoint'], details['rates'])
       # result = altitude_lost(df,details['breakpoint'], details['rates'])
        print(details['name'],result)


# %%
