"""
Created a pickle file from ulog from other use

Fred
12/10/2019
"""

import os
import sys
import time
import math
import pickle

import pandas as pd
import numpy as np

from model import Flight, timeit
from list_param import Device, Position ,VideoDevice

from gui.import_log_gui import Ui_Dialog_import_log

import logging
logger = logging.getLogger("import_log")
from PyQt5.QtWidgets import QDialog

def populate_combo_box( combo , class_param):
    list_param = [i for i in dir(class_param) if not "__" in i]
    for val in list_param:
        combo.addItem(getattr(class_param, val))

class import_log_diaglog(QDialog):
    def __init__(self, parent=None):
        super(import_log_diaglog, self).__init__(parent)

        self.ui = Ui_Dialog_import_log()
        self.ui.setupUi(self)

        self.flight = None

        populate_combo_box(self.ui.positionComboBox, Position)
        populate_combo_box(self.ui.positionComboBox_2, Position)

        populate_combo_box(self.ui.deviceComboBox, Device)
        populate_combo_box(self.ui.deviceComboBox_2, Device)

        populate_combo_box(self.ui.deviceComboBox_video_device, VideoDevice)



