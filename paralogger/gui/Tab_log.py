#coding:utf-8
"""
PARALOGER ANALYSIS 

Log Tab
Diplay log information 

"""

import sys
from PyQt5 import QtWidgets
import logging

class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)