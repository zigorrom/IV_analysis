import sys
import os
import time
import datetime
import configparser
import re
import ntpath
import numpy as np
import pandas as pd

from PyQt4 import uic, QtGui, QtCore
from PyQt4.QtCore import QThread

class IV_analyzer:
    def __init__(self):
        pass



mainViewBase, mainViewForm = uic.loadUiType("UI_IV_analysis.ui")
class MainView(mainViewBase, mainViewForm):
    DRAIN_VOLTAGE_OPTION, DRAIN_CURRENT_OPTION, GATE_VOLTAGE_OPTION, GATE_CURRENT_OPTION = ("Drain voltage", "Drain current", "Gate voltage", "Gate current")


    def __init__(self, parent = None):
        super(mainViewBase, self).__init__(parent)
        self.setupUi(self)
        self.measurement_data_frame = pd.DataFrame()
        self.measurement_folder = None
        self.measurement_file_path = None

    @QtCore.pyqtSlot()
    def on_actionWorkingDirectory_triggered(self):
        
        measurement_filename = os.path.abspath(QtGui.QFileDialog.getOpenFileName(self,caption="Select Folder", directory = self.measurement_folder))
        measurement_folder = os.path.dirname(measurement_filename)

        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("Measurement file selected")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Measurement file selected")
        msg.setDetailedText(measurement_filename)
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        retval = msg.exec_()
        if retval:
            self.measurement_file_path = measurement_filename
            self.measurement_folder = measurement_folder
            self.load_experiment()
        
        return retval


    def closeEvent(self,event):
        print("closing")
        

    def load_experiment(self):
        if self.measurement_file_path:
            self.measurement_data_frame.from_csv(self.measurement_file_path)
            self.parse_measurementdata_filename(self.measurement_file_path)

    @QtCore.pyqtSlot()
    def on_actionNext_triggered(self):
        print("next file")

    @QtCore.pyqtSlot()
    def on_actionPrev_triggered(self):
        print("prev file")

    def parse_measurementdata_filename(self,filename):
        filename = ntpath.basename(filename)
        pattern = re.compile("MeasurmentData_(?P<wafer>.*?)_(?P<chip>.*?)_(?P<info>.*?)\.dat$")
        
        match = pattern.match(filename)
        

        print(match.group("wafer"))
        print(match.group("chip"))
        print(match.group("info"))


    def parse_measurement_filename(self,filename):
        pass

    


def ui_application():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("LegacyNoiseMeasurementSetup")
    app.setStyle("cleanlooks")
    wnd = MainView()
    wnd.show()
    return app.exec_()

if __name__== "__main__":
    sys.exit(ui_application())
    #sys.exit(console_application())