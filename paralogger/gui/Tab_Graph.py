#coding:utf-8
"""
PARALOGER ANALYSIS 

Graph Tab
Generated the widget emmbeded in the main display windows , on the Grpah tab
Cretaed a 2D graph of selected Section 

? maybe the graph creation can be interactive? or parameters in a seperated file ?
"""

import itertools
import os
import sys


import logging
logger = logging.getLogger("Tab_Graph")

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout,
                             QWidget)
from pyqtgraph.Qt import QtCore, QtGui


import numpy as np #Maybe useless
import pyqtgraph as pg
from pyqtgraph.dockarea import *

#from ..judge import Judge

def generated_layout(mdf):
    if len(mdf)>2 :

        area = DockArea()

        # Creat the docks
        d1 = Dock("D1 - altitude", size=(100, 150), closable=True)  
        d2 = Dock("D2 - Pitch",  closable=True)
        d3 = Dock("D3 - Nb_g",  closable=True)
        d4 = Dock("D4 - Yaw",  closable=True)
        d5 = Dock("D5 - Values",  closable=True)
        


        area.addDock(d1, 'left')      ## place d1 at left edge of dock area (it will fill the whole space since there are no other docks yet)
        area.addDock(d5, 'top', d1)      ## place d1 at left edge of dock area (it will fill the whole space since there are no other docks yet)
        area.addDock(d2, 'right', d1)     ## place d2 at right edge of dock area
        area.addDock(d3, 'above', d2)## place d3 at bottom edge of d1
        area.addDock(d4, 'above', d2)## place d3 at bottom edge of d1



        #mainLayout.addWidget(w4)

        # # Set up each plot 
        color = (0,255,120)
        color2 = (100,155,120)

        # %% Altitude  plot
        # considering the start of the  section dataframe as the 0
        p1 = pg.PlotWidget(title="Altitude")
        p1.addLegend()
        start_altitude =mdf["alt"].iloc[0] 
        start_altitude_baro =mdf["baro_alt_meter"].iloc[0] 

        altitude = (mdf["alt"].to_numpy() )   -  start_altitude # meters
        altitude_baro = (mdf["baro_alt_meter"].to_numpy() )   -  start_altitude_baro # meters

        p1.plot(mdf['time0_s'].to_numpy() , altitude, pen=color, name="Alt_gps [m]")
        p1.plot(mdf['time0_s'].to_numpy() , altitude_baro, pen=color2, name="Alt_baro [m]")
        d1.addWidget(p1)

        # Euler angle ( /!\ duplicate code with tab_3D.py :: prepare_data)
        mdf[["pitch", "yaw", "roll"]] = mdf[["pitch", "yaw", "roll"]].apply(np.rad2deg)
        pitch = mdf["pitch"].to_numpy()
        yaw = mdf["yaw"].to_numpy() 
        #roll = mdf["roll"].to_numpy()
        mdf["pitch"] = mdf["pitch"] * -1
        mdf["roll"] = mdf["roll"] * 1
        mdf["yaw"] = mdf["yaw"] * -1

        nbG_tot = mdf["nbG_tot"].to_numpy()


        p2 = pg.PlotWidget(title="Pitch")
        p2.plot(mdf['time0_s'].to_numpy() , pitch, pen=color, name="pitch [deg]")
        d2.addWidget(p2)

        p3 = pg.PlotWidget(title="G force")
        p3.plot(mdf['time0_s'].to_numpy() , nbG_tot, pen=color, name="roll [deg]")
        d3.addWidget(p3)

        p4 = pg.PlotWidget(title="Yaw")
        p4.plot(mdf['time0_s'].to_numpy() , yaw, pen=color, name="yaw [deg]")
        d4.addWidget(p4)
    else:
        area = QLabel()
        area.setText ("No valid data")

    return area

