#coding:utf-8
"""
PARALOGER ANALYSIS 

Judge class
Use to extract numeric value and add classify them 

"""


import bisect
import pickle
from model import Flight, Sections ,sha256sum
import json
import numpy as np
import pandas as pd
import logging
import jsonpickle

logger = logging.getLogger("judge")

class Judge:
    """Judge Object     

    """
    def __repr__(self):
        return 'Judge v%s, %s , %s' % (self.version, self.file_path, self.dict_criteria)

    def __init__(self, mfilePath=None,):
        logger.info("Init judge")

        self.version = 1  # version of the Judge file model
        self.file_path = mfilePath
        self.file_sha1 = None
        self.date = None
        self.dict_criteria = None

        if mfilePath != None:
            self.load_judge(self.file_path)
            self.display_hash_state()


    def display_hash_state(self):
        if self.check_hash():
            logger.info ( "Hash is ok")
            #print ( "Hash is ok")
        else:
            logger.info ( "Hash is Not ok !!")


    def check_hash(self):
        if self.file_path != None :
            file_hash = sha256sum(self.file_path)
            if self.file_sha1 != None:
                return self.file_sha1 == file_hash
            else:  
                self.file_sha1 = file_hash
                logger.info("Hash has been added")
               # print("Hash has been added")
                return True

        else:
            self.file_sha1 = None
            logger.info("No file to check hash")

    
    def load_judge(self,mpath):
        self.file_path = mpath
        with open(self.file_path, 'r') as file:
            judge_string = file.read()
        freezed_judge =jsonpickle.decode(judge_string)
        self.__dict__.update(freezed_judge.__dict__)
        self.display_hash_state()


    def save_judge(self,mpath):
        judge_freeze = jsonpickle.encode(self)
        with open(mpath, 'w') as fp:
            fp.write(judge_freeze)

    def grade(score, mbreakpoint, mgrades=None):
        if mgrades == None or mbreakpoint == None:
            return None
        i = bisect.bisect_left(mbreakpoint,score)
        return mgrades[i]

  
    def run(df, sect_type) :
        result_section = {}
        dict_crit=self.dict_criteria[sect_type]

        for key, details in dict_crit.items():
            method_to_call = getattr(self, details['function'])
            result = method_to_call(df,details['breakpoint'], details['rates'])
        # result = altitude_lost(df,details['breakpoint'], details['rates'])
            result_section[details['name']] = result

        return result_section
  
  
  #### Extract numeric data ######
    
    def altitude_lost(mdf,mbreakpoint,mrates):
        start_altitude = mdf["alt"].iloc[0]
        val = mdf['alt'].min() - start_altitude
        mgrade = grade(val, mbreakpoint,mrates) 
        return {'value' : val , 'grade':mgrade}

    def pitch_max(mdf,mbreakpoint,mrates):
        val = np.rad2deg(abs(df['pitch'].max()))
        mgrade = grade(val, mbreakpoint,mrates) 
        return {'value' : val , 'grade':mgrade}

    def max_nbG(mdf,mbreakpoint,mrates):
        val = abs(df['nbG_tot'].max())
        mgrade = grade(val, mbreakpoint,mrates) 
        return {'value' : val , 'grade':mgrade}

