# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_log_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_import_log(object):
    def setupUi(self, Dialog_import_log):
        Dialog_import_log.setObjectName("Dialog_import_log")
        Dialog_import_log.resize(486, 730)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_import_log)
        self.buttonBox.setGeometry(QtCore.QRect(350, 650, 131, 50))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.label_log_file1 = QtWidgets.QLabel(Dialog_import_log)
        self.label_log_file1.setGeometry(QtCore.QRect(20, 350, 81, 16))
        self.label_log_file1.setObjectName("label_log_file1")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog_import_log)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 293))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.manufacturerLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.manufacturerLabel.setObjectName("manufacturerLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.manufacturerLabel)
        self.manufacturerLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.manufacturerLineEdit.setObjectName("manufacturerLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.manufacturerLineEdit)
        self.line_5 = QtWidgets.QFrame(self.formLayoutWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.line_5)
        self.gliderModelLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.gliderModelLabel.setObjectName("gliderModelLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.gliderModelLabel)
        self.gliderModelLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.gliderModelLineEdit.setObjectName("gliderModelLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.gliderModelLineEdit)
        self.gliderSizeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.gliderSizeLabel.setObjectName("gliderSizeLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.gliderSizeLabel)
        self.gliderSizeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.gliderSizeLineEdit.setObjectName("gliderSizeLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.gliderSizeLineEdit)
        self.gliderModifLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.gliderModifLabel.setObjectName("gliderModifLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.gliderModifLabel)
        self.gliderModifLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.gliderModifLineEdit.setObjectName("gliderModifLineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.gliderModifLineEdit)
        self.line_6 = QtWidgets.QFrame(self.formLayoutWidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.line_6)
        self.pilotLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.pilotLabel.setObjectName("pilotLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.pilotLabel)
        self.pilotLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.pilotLineEdit.setObjectName("pilotLineEdit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.pilotLineEdit)
        self.weightKgLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.weightKgLabel.setObjectName("weightKgLabel")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.weightKgLabel)
        self.weightKgDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.weightKgDoubleSpinBox.setObjectName("weightKgDoubleSpinBox")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.weightKgDoubleSpinBox)
        self.line = QtWidgets.QFrame(self.formLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.line)
        self.locationLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.locationLabel.setObjectName("locationLabel")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.locationLabel)
        self.locationLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.locationLineEdit.setObjectName("locationLineEdit")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.locationLineEdit)
        self.laboratoryLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.laboratoryLabel.setObjectName("laboratoryLabel")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.laboratoryLabel)
        self.laboratoryLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.laboratoryLineEdit.setObjectName("laboratoryLineEdit")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.laboratoryLineEdit)
        self.formLayoutWidget_2 = QtWidgets.QWidget(Dialog_import_log)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(110, 350, 351, 61))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.positionLabel = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.positionLabel.setObjectName("positionLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.positionLabel)
        self.positionComboBox = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.positionComboBox.setObjectName("positionComboBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.positionComboBox)
        self.deviceLabel = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.deviceLabel.setObjectName("deviceLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.deviceLabel)
        self.deviceComboBox = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.deviceComboBox.setObjectName("deviceComboBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.deviceComboBox)
        self.label_3 = QtWidgets.QLabel(Dialog_import_log)
        self.label_3.setEnabled(False)
        self.label_3.setGeometry(QtCore.QRect(20, 440, 81, 16))
        self.label_3.setObjectName("label_3")
        self.formLayoutWidget_3 = QtWidgets.QWidget(Dialog_import_log)
        self.formLayoutWidget_3.setEnabled(False)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(130, 450, 341, 61))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.positionLabel_2 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.positionLabel_2.setEnabled(False)
        self.positionLabel_2.setObjectName("positionLabel_2")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.positionLabel_2)
        self.deviceLabel_2 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.deviceLabel_2.setEnabled(False)
        self.deviceLabel_2.setObjectName("deviceLabel_2")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.deviceLabel_2)
        self.deviceComboBox_2 = QtWidgets.QComboBox(self.formLayoutWidget_3)
        self.deviceComboBox_2.setEnabled(False)
        self.deviceComboBox_2.setObjectName("deviceComboBox_2")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.deviceComboBox_2)
        self.positionComboBox_2 = QtWidgets.QComboBox(self.formLayoutWidget_3)
        self.positionComboBox_2.setEnabled(False)
        self.positionComboBox_2.setObjectName("positionComboBox_2")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.positionComboBox_2)
        self.label = QtWidgets.QLabel(Dialog_import_log)
        self.label.setGeometry(QtCore.QRect(20, 560, 58, 16))
        self.label.setObjectName("label")
        self.formLayoutWidget_4 = QtWidgets.QWidget(Dialog_import_log)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(180, 560, 291, 41))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.deviceLabel_video_device = QtWidgets.QLabel(self.formLayoutWidget_4)
        self.deviceLabel_video_device.setObjectName("deviceLabel_video_device")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.deviceLabel_video_device)
        self.deviceComboBox_video_device = QtWidgets.QComboBox(self.formLayoutWidget_4)
        self.deviceComboBox_video_device.setObjectName("deviceComboBox_video_device")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.deviceComboBox_video_device)
        self.pushButton_import_file_log1 = QtWidgets.QPushButton(Dialog_import_log)
        self.pushButton_import_file_log1.setGeometry(QtCore.QRect(0, 370, 90, 28))
        self.pushButton_import_file_log1.setObjectName("pushButton_import_file_log1")
        self.label_file_log_1 = QtWidgets.QLabel(Dialog_import_log)
        self.label_file_log_1.setGeometry(QtCore.QRect(20, 410, 411, 20))
        self.label_file_log_1.setObjectName("label_file_log_1")
        self.pushButton_import_file_log2 = QtWidgets.QPushButton(Dialog_import_log)
        self.pushButton_import_file_log2.setEnabled(False)
        self.pushButton_import_file_log2.setGeometry(QtCore.QRect(10, 470, 90, 28))
        self.pushButton_import_file_log2.setObjectName("pushButton_import_file_log2")
        self.label_file_log_2 = QtWidgets.QLabel(Dialog_import_log)
        self.label_file_log_2.setEnabled(False)
        self.label_file_log_2.setGeometry(QtCore.QRect(20, 520, 431, 16))
        self.label_file_log_2.setObjectName("label_file_log_2")
        self.pushButton_import_file_video = QtWidgets.QPushButton(Dialog_import_log)
        self.pushButton_import_file_video.setGeometry(QtCore.QRect(0, 580, 90, 28))
        self.pushButton_import_file_video.setObjectName("pushButton_import_file_video")
        self.label_file_video = QtWidgets.QLabel(Dialog_import_log)
        self.label_file_video.setGeometry(QtCore.QRect(20, 620, 431, 16))
        self.label_file_video.setObjectName("label_file_video")
        self.line_2 = QtWidgets.QFrame(Dialog_import_log)
        self.line_2.setGeometry(QtCore.QRect(40, 320, 381, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(Dialog_import_log)
        self.line_3.setGeometry(QtCore.QRect(140, 430, 171, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(Dialog_import_log)
        self.line_4.setGeometry(QtCore.QRect(140, 540, 171, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.button_debug = QtWidgets.QPushButton(Dialog_import_log)
        self.button_debug.setGeometry(QtCore.QRect(10, 660, 90, 28))
        self.button_debug.setObjectName("button_debug")
        self.button_import = QtWidgets.QPushButton(Dialog_import_log)
        self.button_import.setGeometry(QtCore.QRect(230, 660, 90, 28))
        self.button_import.setObjectName("button_import")
        self.label_status = QtWidgets.QLabel(Dialog_import_log)
        self.label_status.setGeometry(QtCore.QRect(107, 690, 251, 20))
        self.label_status.setObjectName("label_status")

        self.retranslateUi(Dialog_import_log)
        self.buttonBox.accepted.connect(Dialog_import_log.accept)
        self.buttonBox.rejected.connect(Dialog_import_log.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_import_log)

    def retranslateUi(self, Dialog_import_log):
        _translate = QtCore.QCoreApplication.translate
        Dialog_import_log.setWindowTitle(_translate("Dialog_import_log", "Import log files"))
        self.label_log_file1.setText(_translate("Dialog_import_log", "Log files 1 *:"))
        self.manufacturerLabel.setText(_translate("Dialog_import_log", "Manufacturer"))
        self.gliderModelLabel.setText(_translate("Dialog_import_log", "Glider model *:"))
        self.gliderSizeLabel.setText(_translate("Dialog_import_log", "Glider size * "))
        self.gliderModifLabel.setText(_translate("Dialog_import_log", "Glider modif"))
        self.pilotLabel.setText(_translate("Dialog_import_log", "Pilot *"))
        self.weightKgLabel.setText(_translate("Dialog_import_log", "Weight(kg) *"))
        self.locationLabel.setText(_translate("Dialog_import_log", "Location"))
        self.laboratoryLabel.setText(_translate("Dialog_import_log", "Laboratory"))
        self.positionLabel.setText(_translate("Dialog_import_log", "Position"))
        self.deviceLabel.setText(_translate("Dialog_import_log", "Device"))
        self.label_3.setText(_translate("Dialog_import_log", "Log files 2:"))
        self.positionLabel_2.setText(_translate("Dialog_import_log", "Position"))
        self.deviceLabel_2.setText(_translate("Dialog_import_log", "Device"))
        self.label.setText(_translate("Dialog_import_log", "Video file:"))
        self.deviceLabel_video_device.setText(_translate("Dialog_import_log", "Device"))
        self.pushButton_import_file_log1.setText(_translate("Dialog_import_log", "Browse"))
        self.label_file_log_1.setText(_translate("Dialog_import_log", "No file selected"))
        self.pushButton_import_file_log2.setText(_translate("Dialog_import_log", "Browse"))
        self.label_file_log_2.setText(_translate("Dialog_import_log", "No file selected"))
        self.pushButton_import_file_video.setText(_translate("Dialog_import_log", "Browse"))
        self.label_file_video.setText(_translate("Dialog_import_log", "No file selected"))
        self.button_debug.setText(_translate("Dialog_import_log", "debug"))
        self.button_import.setText(_translate("Dialog_import_log", "Import"))
        self.label_status.setText(_translate("Dialog_import_log", "Field with * are mandatory"))

