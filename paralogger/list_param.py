#coding:utf-8
"""
PARALOGER ANALYSIS 

Parameters list :
Classe use to ensure a consistence between all modeule/files , regarding the parameters name.

"""



############################# PARAMETERS CLASS #############################
from enum import Enum


class Device(Enum):
    SENSBOX = "Sensbox (not suported)"
    PIXRACER = "Pixracer"

class VideoDevice(Enum):
    GOPRO_3 = "GOPRO_3"
    GOPRO_5 = "GOPRO_5"
    GOPRO_7 = "GOPRO_7"

class Position(Enum):
    PILOT = "Pilot"
    GLIDER = "Glider"

class Kind(Enum):
    FRONTAL = "Frontal"
    ASYM = "Asym"
    SPIRAL = "Spiral"
    MISC = "Misc"




