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
import copy

logger = logging.getLogger("judge")

def make_hash(o):

  """
  Makes a hash from a dictionary, list, tuple or set to any level, that contains
  only other hashable types (including any lists, tuples, sets, and
  dictionaries).
  """

  if isinstance(o, (set, tuple, list)):

    return tuple([make_hash(e) for e in o])    

  elif not isinstance(o, dict):

    return hash(o)

  new_o = copy.deepcopy(o)
  for k, v in new_o.items():
    new_o[k] = make_hash(v)

  return hash(tuple(frozenset(sorted(new_o.items()))))

class Judge:
    """Judge Object     

    """
    def __repr__(self):
        return 'Judge v%s, %s , %s' % (self.version, self.file_path, self.dict_criteria)

    def __init__(self, mfilePath=None,):
        logger.info("Init judge")

        self.judge_version = 1  # version of the Judge file model
        self.file_path = mfilePath
        self.dict_sha1 = None
        self.date = None
        self.dict_criteria = None

        if mfilePath != None:
            self.load_judge(self.file_path)
            self.hash_state()

    def hash_state(self):
        """Compute hash of the judge and  a other one of the criteria dict.
        Usefull to detect change , to be sure we all use the same
        
        Returns:
            duple(str, str) -- judge hash ,  dict criteira hash
        """
        self_hash = make_hash(self.__dict__)
        dict_crit_hash = make_hash(self.dict_criteria)

        logger.info("Judge hash is: " + str(self_hash))
        logger.info("Citeria dict hash is: " + str(dict_crit_hash))

        return str(self_hash) , str(dict_crit_hash)
    
    def load_judge(self,mpath):
        self.file_path = mpath
        with open(self.file_path, 'r') as file:
            judge_string = file.read()
        freezed_judge =jsonpickle.decode(judge_string)
        self.__dict__.update(freezed_judge.__dict__)
        self.hash_state()

    def save_judge(self,mpath):
        judge_freeze = jsonpickle.encode(self)
        with open(mpath, 'w') as fp:
            fp.write(judge_freeze)

    def grade(self,score, mbreakpoint, mgrades=None):
        if mgrades == None or mbreakpoint == None:
            return None
        i = bisect.bisect_left(mbreakpoint,score)
        return mgrades[i]

  
    def run(self,df, sect_type) :
        result_section = {}
        dict_crit=self.dict_criteria[sect_type]

        for key, details in dict_crit.items():
            method_to_call = getattr(self, details['function'])
            result = method_to_call(df,details['breakpoint'], details['rates'])
        # result = altitude_lost(df,details['breakpoint'], details['rates'])
            result_section[details['name']] = result

        return result_section
  
  
  #### Extract numeric data ######
    
    def altitude_lost(self,mdf,mbreakpoint,mrates):
        start_altitude = mdf["alt"].iloc[0]
        val = mdf['alt'].min() - start_altitude
        mgrade = self.grade(val, mbreakpoint,mrates) 
        return {'value' : val , 'grade':mgrade}

    def pitch_max(self,mdf,mbreakpoint,mrates):
        val = np.rad2deg(abs(mdf['pitch'].max()))
        mgrade = self.grade(val, mbreakpoint,mrates) 
        return {'value' : val , 'grade':mgrade}

    def max_nbG(self,mdf,mbreakpoint,mrates):
        val = abs(mdf['nbG_tot'].max())
        mgrade = self.grade(val, mbreakpoint,mrates) 
        return {'value' : val , 'grade':mgrade}

