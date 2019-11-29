#coding:utf-8
"""
PARALOGER ANALYSIS 

NB_aplycriteria 
This notebook  help to devvelope the ctriteria aplication 
"""
#%% import
import bisect
import pickle
from model import Flight, Sections, Criteria_book, Criteria


#%% run
def grade(score, breakpoint=[60,70,80,90], grades='FDCBA'):
    i = bisect.bisect(breakpoint,score)
    return grades[i]

#[grade(score) for score in [33,99,77,70,89,90,100]]


# %% Create criteria book

crit_book = Criteria_book()

crit1 = Criteria()
crit1.name="altitude_lost"
crit1.plain_name="Altitude lost"
crit1.unit="m"
crit1.breakpoint= [20 , 30, 40 , 100]
crit1.rates="ABCD"

crit_book.criteria_list.append(crit1)


crit2 = Criteria()
crit2.name="pitch-max"
crit2.plain_name="Maximun pitch"
crit2.unit="°"
crit2.breakpoint= [20 , 30, 45 , 80]
crit2.rates="ABCD"

crit_book.criteria_list.append(crit2)

#%% load flight

flight = None 

pikle_path = "Flight2_gourdon_v3.pkl"

with open(pikle_path, 'rb') as pickle_file:
    flight = pickle.load(pickle_file)


# %% function

def altitude_lost(mdf,breakpoint,rates):
    alt_lost = df['alt'].min()
    mgrade = grade(alt_lost, breakpoint,rates) 
    return {'value' : alt_lost , 'grade':mgrade}

#%% process
for sect in flight.sections:
    print("\n section:" , sect)
    df = flight.apply_section(sect.id)
    result = altitude_lost(df,crit1.breakpoint, crit1.rates)
    print(result)


# %%
