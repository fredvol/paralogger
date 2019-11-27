#coding:utf-8
"""
PARALOGER ANALYSIS 

Main file , start Point.

"""
__credits__ = ["Mattleg", "Bruno D", "Fred P"]
__license__ = "GPL V3"
__version__ = '0.1.1'
__pickle_file_version__ = 2  #This will help to detect previous version of pkl file when imported

import logging
import os
import pickle
import platform
import sys
import time
import csv
from logging.handlers import RotatingFileHandler

from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from gui.main_gui import Ui_MainWindow
from gui.Tab_3D import Visualizer3D
from gui.Tab_Graph import generated_layout
from gui.Tab_log import QTextEditLogger
from gui.Tab_Table import pandasTableModel
from import_log import import_log_diaglog
from list_param import Position
from model import Flight, Sections, getSystemInfo, timeit

os.environ["DISPLAY"] = ":0"  #Use for linux  on vscode at least


log_file_name = "main_paralogger.log"


def config_logger():
    """Logger configuration.
    log in a file + send to debug console + send to log tab in the app
    """
    logger = logging.getLogger()
    # logging.basicConfig(filename='1_import.log',level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(module)s :: %(funcName)s ::  %(message)s")
    file_handler = logging.handlers.RotatingFileHandler(log_file_name, "a", 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Redirect log on console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    return logger


logger = config_logger()

def deleteItemsOfLayout(layout):
     if layout is not None:
         while layout.count():
             item = layout.takeAt(0)
             widget = item.widget()
             if widget is not None:
                 widget.setParent(None)
             else:
                 deleteItemsOfLayout(item.layout())

class Prog(QtGui.QMainWindow):
    """This is the MAIN program, this is the start point,
     nothing should be calle from doutside of this class.
    
    Arguments:
        QtGui.QMainWindow {QMainWindow object } -- QMainWindow legacy
    
    Returns:
        [None] -- Just run until it closed
    """
    def __init__(self):
        super().__init__(None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QtCore.QTimer(self)

        #set up the log tab
        logTextBox = QTextEditLogger(self)

        logTextBox.setFormatter(
            logging.Formatter('"%(asctime)s - %(levelname)s \t- %(module)s \t- %(funcName)s ::  %(message)s"'))
        logging.getLogger().addHandler(logTextBox)
        layout_log = QtWidgets.QVBoxLayout()
        layout_log.addWidget(logTextBox.widget)
        self.ui.tab_log.setLayout(layout_log)
        logger.info("--- Start ---")
        logger.info("Python : " + str(sys.version))
        logger.info("Prog  version : " + str(__version__))
        logger.info("-------")
        

        #Set up variable
        self.flight = None
        self.visualizer_3d = None        

        #add Action
        self.ui.actionOpen.triggered.connect(self.open_pickle_file)
        self.ui.actionSave_as.triggered.connect(self.save_pickle_file)
        self.ui.actionimport.triggered.connect(self.import_log_window)
        self.ui.actionVersion.triggered.connect(self.about_popup)
        self.ui.actionHelp.triggered.connect(self.openUrl_help)
        self.ui.actiondebug_open.triggered.connect(self.debug)

        self.ui.treeWidget.itemClicked.connect(self.onTreeItemClicked)
        self.ui.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.openMenu)

        #setup Qtree
        self.ui.treeWidget.setHeaderLabels(["Name", "Kind", "Id"])

        #setup table view detail section
        self.ui.model = QtGui.QStandardItemModel(self)  # SELECTING THE MODEL - FRAMEWORK THAT HANDLES QUERIES AND EDITS
        self.ui.tableView.setModel(self.ui.model)  # SETTING THE MODEL
        self.ui.model.dataChanged.connect(self.on_datachange_model)
    


    def debug(self):
        ''' only use for speed up de developement
        '''
        self.open_pickle_file("Flight2_gourdon.pkl")

    def open_pickle_file(self, filename=None): 
        """Function to import a file already saved, format is classic python pickle .pkl
        
        Keyword Arguments:
            filename {[str]} -- if a path is given the browse dialog do not open ( use for debug function) (default: {None})
        
        Returns:
            [None] -- But saved the nex loaded flight in the main self.Flight object.
        """            

        if filename == False:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open pickler File', "", 'Pickle Files (*.pkl)')

        if isinstance(filename, tuple):
            filename = filename[0]
        if filename:
            try:
                logger.info(" importing : " + str(filename))
                self.file_name = filename
                self.id = 0
                with open(filename, 'rb') as pickle_file:
                    self.flight = pickle.load(pickle_file)

                #Check for version of the opened file 
                if hasattr(self.flight, 'flight_version'):
                    if int(self.flight.flight_version) < __pickle_file_version__ :
                        logger.info(" !! Importing Old file format: " + str(self.flight.flight_version) + " current is: " + str(__pickle_file_version__))
                else:
                    logger.info(" !! Importing a file without flight_version info: version can not be checked ")

                self.update_project_tree()

            except Exception as ex:
                logger.error(ex)

    def save_pickle_file(self):
        """Save the current self.Flight object to a pickle file. (.pkl)
        """
        try:
            tuple_saved_file = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '', 'Pickle(*.pkl)')
            name_saved_file = tuple_saved_file[0] + '.pkl'
            logger.info("Saving as : " + name_saved_file[0] + '.pkl')
            with open(name_saved_file, "wb") as f:
                pickle.dump(self.flight, f)

        except Exception as ex:
            logger.error(ex)
    
    def import_log_window(self):
        """Function will display a other dialog to fill for loading a raw  log file
        the dialog will auto close when the import is finish.
        """
        widget_import_new = import_log_diaglog()
        widget_import_new.exec_()
        logger.debug("back in main prog")
        try:  # try to copy the flight object from the dialog windows to the main Flight object
            self.flight = widget_import_new.imported_Flight
            self.update_project_tree()
        except Exception as ex:
            logger.warning(ex)

    def about_popup(self):
        """ About section 
        Display various info for debug and system details
        TODO ; having a better list of the enviroment module and their version.
        """

        # from https://stackoverflow.com/questions/54447535/how-to-fix-typeerror-in-qtwidgets-qmessagebox-for-popup-messag
        cwd = os.path.dirname(os.path.abspath(__file__))
        
        log_content = getSystemInfo()

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Version : " + str(__version__) + "\n"
                    "pkl file version: " + str(log_file_name) + "\n"
                    "Log file name: " + str(__pickle_file_version__) + "\n"
                    "curent working directory: " + str(cwd))
        msg.setInformativeText("More info on :\nhttps://github.com/fredvol/paralogger ")
        msg.setWindowTitle("About")
        msg.setDetailedText(log_content)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)  #| QtWidgets.QMessageBox.Cancel)

        retval = msg.exec_()

    def openUrl_help(self):
        """Open github page in browser
        """
        url = QtCore.QUrl('https://github.com/fredvol/paralogger')
        if not QtGui.QDesktopServices.openUrl(url):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')



    ### TREE VIEW  ###
    # Tree view will display the flight and all the sections attach to. 
    
    def update_project_tree(self):
        """repopulated the tree view , to show modif.
        """
        logger.info("update_project_tree")
        tw = self.ui.treeWidget
        tw.clear()
        l1 = QtWidgets.QTreeWidgetItem([self.flight.glider, "--", self.flight.id])

        for sect in self.flight.sections:
            l1_child = QtWidgets.QTreeWidgetItem([str(sect.start) + " - " + str(sect.end), sect.kind, sect.id])
            l1.addChild(l1_child)

        tw.addTopLevelItem(l1)
        tw.expandAll()

    def get_level_from_index(self, indexes):
        """Return the level in the treeview
        level 0 = Flight
        level 1 = Section
        
        Arguments:
            indexes {[QModelIndex]} -- not realy clear for me !
        
        Returns:
            level [Int]  -- The level of the cliked item
        """

        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        else:
            level = -1

        return level

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onTreeItemClicked(self, it, col):
        """function trigered when an object is cliked on the tree view
        This a central function which dispath the work to the other objects .
        
        Arguments:
            it {QTreeWidgetItem} -- item cliked
            col {int} -- index of  columns cliked
        """

        indexes = self.ui.treeWidget.selectedIndexes()

        level = self.get_level_from_index(indexes)

        if level >= 0: # if a Flight or a Section
            uid = it.text(2)  # The text of the node.
            logger.debug("clicked: " + str(it) + ", " + str(col) + ", " + str(uid) + " level: " + str(level))
        else:
            uid = None


        #Job dispatching
        if level == 0:  # flight  level
            self.populate(uid, level)
            self.display_tab_Table(None)

        elif level == 1:  # section level
            #update all tabs
            self.display_tab_graph(uid)
            self.display_tab_Table(uid)
            self.display_tab_3D(uid)

            self.populate(uid, level)

    def openMenu(self, position):
        """Open contextual menu in tree View widget
        
        Arguments:
            position {[type]} -- [description]
        """
        indexes = self.ui.treeWidget.selectedIndexes()
        item = self.ui.treeWidget.itemAt(position)

        menu = QtWidgets.QMenu()

        level = self.get_level_from_index(indexes)
        if level > 0 and item != None:
            uid = item.text(2)  # The UId of teh object

        if level == 0:  # Flight
            action_add = menu.addAction(self.tr("Add Section"))
            action_add.triggered.connect(self.add_section)
            action_refresh = menu.addAction(self.tr("Refresh"))
            action_refresh.triggered.connect(self.update_project_tree)

            action_export_csv = menu.addAction('Export CSV')
            action_export_csv.triggered.connect(lambda: self.export_df(expformat="csv"))

            action_export_xls = menu.addAction('Export XLSX')
            action_export_xls.triggered.connect(lambda: self.export_df(expformat="xlsx"))

            action_export_xls = menu.addAction('Export device parameters')
            action_export_xls.triggered.connect(self.export_device_param)

        elif level == 1: #Section
            action_export_csv = menu.addAction('Export CSV')
            action_export_csv.triggered.connect(lambda: self.export_df(uid,expformat="csv"))

            action_export_xls = menu.addAction('Export XLSX')
            action_export_xls.triggered.connect(lambda: self.export_df(uid,expformat="xlsx"))

            action_del = menu.addAction('Delete')
            action_del.triggered.connect(lambda: self.delete_section(uid))

            action_refresh = menu.addAction(self.tr("Refresh"))
            action_refresh.triggered.connect(self.update_project_tree)

        menu.exec_(self.ui.treeWidget.viewport().mapToGlobal(position))

    def delete_section(self, uid):
        """Delete the a Section from the self.Flight and refresh
        
        Arguments:
            uid {Str} -- Uid of the Section to delete
        """
        logger.info("delete section :" + str(uid))
        self.flight.delete_section(uid)
        self.update_project_tree()

    def add_section(self):
        """Add a section in self.Flight
        By default  there start from 0 to the end.
        """
        logger.info("add section")
        self.flight.add_general_section()
        self.update_project_tree()
    
    def export_device_param(self):
        """ Export the internal parameters of the PX4 
        TODO  not avaible if not PX4 filter
        """

        df_param = self.flight.data[0].device_param
        tuple_export_file = QtGui.QFileDialog.getSaveFileName(self, 'csv_file', '', '.csv')
        name_export_file = tuple_export_file[0] + '.csv'
        with open(name_export_file, 'w', newline="") as csv_file:  
            writer = csv.writer(csv_file)
            for key, value in df_param.items():
                writer.writerow([key, value])

        logger.info("Device parameters exported : " + str(name_export_file))


    def export_df(self,uid = None, expformat="csv"):
        """Export Dataframe  in different format
        
        Keyword Arguments:
            uid {str} -- Uid of the Section to export (default: {None})
            expformat {str} -- Format to export [csv , xlsx] (default: {"csv"})
        
        If UID is None then export the flight ( maybe change to use the level info, to be consitent)
        """
        # TODO add multi sheet( xlsx) or file (csv) if multi data_file in flight
        if uid != None:  # if it is a section
            df_to_export = self.flight.apply_section(uid)
        else:  # if not section passed , then export main df
            df_to_export = self.flight.get_df_by_position(Position.PILOT)[0] 
        try:
            tuple_export_file = QtGui.QFileDialog.getSaveFileName(self, 'Export Dataframe File', '', '.'+str(expformat))
            name_export_file = tuple_export_file[0] + '.' + str(expformat)
            if expformat == 'csv':
                df_to_export.to_csv(name_export_file)
            elif expformat == 'xlsx':
                logger.info("Exporting to Excel can take a while, coffee time ...")
                df_to_export.to_excel(name_export_file) 
            logger.info("Exported as : " + name_export_file)
        except Exception as ex:
            logger.error(ex)

            

    #### TAB WIDGET ACTIONS ###
    # This section manage all the Tab ins the view part of the main windows.

    def display_tab_3D(self, uid):
        """Call the Tab_3d.py  and generated a 3D view .
        
        Arguments:
            uid {str} -- id of the Section to display
        Nothing append if Flight is selected, only for Sections

        TODO reload data when other section are cliked ( only display the first cliked one)
        """

        df_to_plot = self.flight.apply_section(uid)
        ####
        #empty actual area if exist
        if len(self.ui.tab_3d.children()) > 0:
            print("not empty")  #TODO  need doublec cliked for update
            deleteItemsOfLayout(self.visualizer_3d.layout_general)
            self.visualizer_3d.layout_general.deleteLater()
            self.visualizer_3d.layout_general = None
            
            #self.visualizer_3d.reset()  WIP
            #self.visualizer_3d.animation(df_to_plot, True, timer=self.timer)

        self.visualizer_3d = Visualizer3D(self.ui.tab_3d)
        self.visualizer_3d.animation(df_to_plot, True, timer=self.timer)
        self.ui.tab_3d.setLayout(self.visualizer_3d.layout_general)

    def display_tab_Table(self, uid):
        """ Display the Pilot dataframe  in a table
        
        Arguments:
            uid {str} -- id of the Section to display

        For Flight and Section.
        ! only for dataframe  at pilot position
        TODO : Manage if no pilot position is available
        """
        try:
            if uid != None:  # if it is a section
                df_to_plot = self.flight.apply_section(uid)
            else:  # if not section passed , then plot main df
                df_to_plot = self.flight.get_df_by_position(Position.PILOT)[0] 

            model = pandasTableModel(df_to_plot)
            if len(self.ui.tab_table.children()) > 0:
                self.ui.tab_table.children()[1].setModel(model)
            else:
                mainLayout = QtWidgets.QVBoxLayout()

                view = QtWidgets.QTableView()
                view.setModel(model)

                mainLayout.addWidget(view)

                self.ui.tab_table.setLayout(mainLayout)
        except Exception as ex:
            logger.warning(ex)
            pass

    def display_tab_graph(self, uid):
        """PLot different Graph 

        Arguments:
            uid {str} -- id of the Section to display
        
        Work only for Section
        TODO: Display full Flight with the section part Highlighted.
        """

        df_to_plot = self.flight.apply_section(uid)
        inside_widget = generated_layout(df_to_plot)

        #empty actual area if exist
        if len(self.ui.tab_graph.children()) > 0:
            print("not empty")
            layout = self.ui.tab_graph.children()[0]
            deleteItemsOfLayout(layout)
            # Old code for deleting item
            # for i in reversed(range(layout.count())):
            #     widgetToRemove = layout.itemAt(i).widget()
            #     # remove it from the layout list
            #     layout.removeWidget(widgetToRemove)
            #     # remove it from the gui
            #     widgetToRemove.setParent(None)

            layout.addWidget(inside_widget)

        else:
            mainLayout = QtWidgets.QVBoxLayout()
            mainLayout.addWidget(inside_widget)
            self.ui.tab_graph.setLayout(mainLayout)

    ## DETAILS OBJECT

    def on_datachange_model(self, signal):
        """Function use to update the self.Flight object  when a value is changed in the Detail table view
        
        Arguments:
            signal {QModelIndex} -- Index of the modified cell
        """
        row = signal.row()  # retrieves row of cell that was double clicked
        column = signal.column()  # retrieves column of cell that was double clicked
        cell_dict = self.ui.model.itemData(signal)  # returns dict value of signal
        cell_value = cell_dict.get(0)  # retrieve value from dict

        uid = self.ui.model.itemData(signal.sibling(0, 1)).get(0)

        index = signal.sibling(row, 0)
        index_dict = self.ui.model.itemData(index)
        index_value = index_dict.get(0)
        logger.debug('Edited Row {}, Col {} value: {} index_value: {}, uid: {}'.format(
            row, column, cell_value, index_value, uid))

        ## Update the Data model ( self.flight) from the changed done in self.ui_model
        if self.flight.id == uid:
            setattr(self.flight, index_value, cell_value)
        else:
            for sect in self.flight.sections:
                if sect.id == uid:
                    setattr(sect, index_value, cell_value)

        ## Update tree view:
        self.update_project_tree()

    def populate(self, uid, level):

        """ Add data in the Table view , via model 
        Exxtract a Dict of of a object properties.
        ! model only accepts strings - must convert.
 
        Arguments:
            uid {str} -- ID of the object to display
            level {int} -- object cliked level ( FLight or Section)
        """

        logger.debug("display_properties of: " + str(uid))
        self.ui.model.clear() # Clear th UI model notthe self.Flight

        if level == 0:
            dict_to_display = vars(self.flight)
        elif level == 1:
            dict_to_display = vars(self.flight.section_by_id(uid))

        for name, value in dict_to_display.items():
            row = []
            cell_name = QtGui.QStandardItem(str(name))
            row.append(cell_name)
            cell_value = QtGui.QStandardItem(str(value))
            row.append(cell_value)

            self.ui.model.appendRow(row)

        # self.show()


def main():
    logger.info(" --- Start ----")
    app = QtGui.QApplication(sys.argv)
    MyProg = Prog()
    MyProg.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    """Absolute Start Point of the universe!
    """
    main()

# MISC
# pyuic5 paraloger_GUI1.ui > main_gui.py
# pyuic5 import_log_GUI.ui > import_log_gui.py 
# panda to table view:  https://stackoverflow.com/questions/44603119/how-to-display-a-pandas-data-frame-with-pyqt5-pyside2
#
