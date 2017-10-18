import sys
import os
import time
import datetime
import configparser
import numpy as np
import pandas as pd

from PyQt4 import uic, QtGui, QtCore
from PyQt4.QtCore import QThread

mainViewBase, mainViewForm = uic.loadUiType("UI_IV_analysis.ui")
class MainView(mainViewBase, mainViewForm):
    def __init__(self, parent = None):
        super(mainViewBase, self).__init__(parent)
        self.setupUi(self)




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