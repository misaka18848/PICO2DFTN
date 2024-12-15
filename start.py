#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, time, shutil, re, ui_mainwindow, res_rc
import sys
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
from ui_mainwindow import Ui_Form



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self) 




if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowIcon(QIcon(u":/img/pnlo.ico"))
    window.show()

    sys.exit(app.exec())





