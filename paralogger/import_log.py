#coding:utf-8
"""
PARALOGER ANALYSIS 

File generating the Import log dialog in the GUI.

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
from PyQt5.QtWidgets import QDialog, QWidget, QProgressDialog
from PyQt5.QtGui import QFileDialog , QGuiApplication
from PyQt5.QtCore import QRect 

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

        self.ui.positionComboBox.setCurrentIndex(1) # to have pilot as default position


        #set up button
        self.ui.button_debug.clicked.connect(self.debug_)
        self.ui.button_import.clicked.connect(self.import_flight)
        self.ui.pushButton_import_file_log1.clicked.connect(self.browse_path)

        self.check_valid()

        #set up line edit:
        self.ui.gliderModelLineEdit.textChanged.connect(self.check_valid)

        self.imported_Flight = None


    def debug_(self):
        """Quickly populate all flied for rapid debug
        """
        logger.debug("Populate with dummy values")
        file_name = "/home/fred/Ozone/paralogger/paralogger/samples/log_6_2019-11-6-13-32-36_flight_1.ulg"

        self.ui.label_file_log_1.setText(file_name)
        self.ui.gliderModelLineEdit.setText("Macpi4")
        self.ui.manufacturerLineEdit.setText("Exemple_gliders_ltd")
        self.ui.locationLineEdit.setText("niceplace")
        self.ui.gliderSizeLineEdit.setText("24")
        self.ui.pilotLineEdit.setText("Arnold")
        self.ui.weightKgDoubleSpinBox.setValue(95)
        self.ui.laboratoryLineEdit.setText("GoodLab")

    def update_label_status(self, str_message):
        self.ui.label_status.setText(str_message)
        QGuiApplication.processEvents() # would be better to use a progressbar


    def browse_path(self):
        filename = QFileDialog.getOpenFileName(self, 'Open pickler File', "", 'Logs Files (*.*)')

        if isinstance(filename, tuple):
            filename = filename[0]
        if filename: 
            self.ui.label_file_log_1.setText(filename)


    def import_flight(self):
        """Create a Flight object, read the raw log file and add meta data .
        TODO mange if device != Pixracer 
        """
        
        self.update_label_status("Loading in progress, please wait  ...")
        self.update()

        logger.debug('import flight .......')

        self.imported_Flight = Flight()
        
        ulog_file_path = self.ui.label_file_log_1.text()
        ulog_device = text = str(self.ui.deviceComboBox.currentText())
        ulog_position = text = str(self.ui.positionComboBox.currentText())

        glider_name = self.ui.gliderModelLineEdit.text()
        manufacturer_name = self.ui.manufacturerLineEdit.text()
        modif = self.ui.gliderModifLineEdit.text()
        location = self.ui.locationLineEdit.text()
        size = self.ui.gliderSizeLineEdit.text()
        pilot = self.ui.pilotLineEdit.text()
        weight = self.ui.weightKgDoubleSpinBox.value()
        lab = self.ui.laboratoryLineEdit.text()

        self.imported_Flight.add_data_file(ulog_file_path, ulog_device, ulog_position)
        self.imported_Flight.add_info( manufacturer_name, glider_name,size, modif, pilot, weight, location,lab)
        self.imported_Flight.add_general_section()



        logger.debug("close import dialog")


        self.close()


    def check_valid(self):
        """Check if the  required field and ok  to enble the import.
        """
        check_list=[]
        item_to_check = [self.ui.gliderModelLineEdit,
                        self.ui.label_file_log_1
                            ]

        for item in item_to_check:
            check_list.append(len(item.text()) < 1)

        if not any(check_list):
            self.ui.button_import.setEnabled(True)
            self.ui.label_status.setText("Field with * are mandatory (OK)")
        else:
            self.ui.button_import.setEnabled(False)

