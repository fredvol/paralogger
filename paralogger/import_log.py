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
from PyQt5.QtGui import QFileDialog

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

        #set up button
        self.ui.button_debug.clicked.connect(self.debug_)
        self.ui.button_import.clicked.connect(self.import_flight)
        self.ui.pushButton_import_file_log1.clicked.connect(self.browse_path)

        self.check_valid()

        #set up line edit:
        self.ui.gliderModelLineEdit.textChanged.connect(self.check_valid)


    def debug_(self):
        print("populate with dummy values")
        file_name = "/home/fred/Ozone/paralogger/paralogger/samples/log_6_2019-11-6-13-32-36_flight_1.ulg"

        self.ui.label_file_log_1.setText(file_name)
        self.ui.gliderModelLineEdit.setText("Macpi4")
        self.ui.manufacturerLineEdit.setText("Exemple_gliders_ltd")
        self.ui.locationLineEdit.setText("niceplace")
        self.ui.gliderSizeLineEdit.setText("24")
        self.ui.pilotLineEdit.setText("Arnold")
        self.ui.weightKgDoubleSpinBox.setValue(95)
        self.ui.laboratoryLineEdit.setText("GoodLab")

    def browse_path(self):
        print("browsing")

        filename = QFileDialog.getOpenFileName(self, 'Open pickler File', "", 'Logs Files (*.*)')

        if isinstance(filename, tuple):
            filename = filename[0]
        if filename: 
            self.ui.label_file_log_1.setText(filename)


    def import_flight(self):
        print('import flight .......')
        print(super.flight)

        self.close()


    def check_valid(self):
        print("in check valid")
        check_list=[]
        item_to_check = [self.ui.gliderModelLineEdit,
                        self.ui.label_file_log_1
                            ]

        for item in item_to_check:
            check_list.append(len(item.text()) < 1)
        print(check_list)

        if not any(check_list):
            self.ui.button_import.setEnabled(True)

        else:
            self.ui.button_import.setEnabled(False)

