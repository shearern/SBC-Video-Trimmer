# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\vidtrim\VideoTrimMainWindow_UI.ui'
#
# Created: Wed Dec 21 13:48:53 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_VideoTrimMainWindow_UI(object):
    def setupUi(self, VideoTrimMainWindow_UI):
        VideoTrimMainWindow_UI.setObjectName("VideoTrimMainWindow_UI")
        VideoTrimMainWindow_UI.resize(839, 128)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/assets/images/app_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        VideoTrimMainWindow_UI.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(VideoTrimMainWindow_UI)
        self.centralwidget.setObjectName("centralwidget")
        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(730, 60, 31, 23))
        self.lcdNumber.setNumDigits(2)
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber_2 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(760, 60, 31, 23))
        self.lcdNumber_2.setNumDigits(2)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.lcdNumber_3 = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber_3.setGeometry(QtCore.QRect(790, 60, 31, 23))
        self.lcdNumber_3.setNumDigits(2)
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.horizontalSlider = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(10, 60, 681, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(420, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(630, 10, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalSlider_2 = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(720, 10, 91, 19))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(330, 10, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(90, 10, 81, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(550, 10, 81, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        VideoTrimMainWindow_UI.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(VideoTrimMainWindow_UI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 839, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        VideoTrimMainWindow_UI.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(VideoTrimMainWindow_UI)
        self.statusbar.setObjectName("statusbar")
        VideoTrimMainWindow_UI.setStatusBar(self.statusbar)
        self.actionSource_Files = QtGui.QAction(VideoTrimMainWindow_UI)
        self.actionSource_Files.setObjectName("actionSource_Files")
        self.actionCommmit = QtGui.QAction(VideoTrimMainWindow_UI)
        self.actionCommmit.setObjectName("actionCommmit")
        self.menuFile.addAction(self.actionSource_Files)
        self.menuFile.addAction(self.actionCommmit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(VideoTrimMainWindow_UI)
        QtCore.QMetaObject.connectSlotsByName(VideoTrimMainWindow_UI)

    def retranslateUi(self, VideoTrimMainWindow_UI):
        VideoTrimMainWindow_UI.setWindowTitle(QtGui.QApplication.translate("VideoTrimMainWindow_UI", "Video Trim", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("VideoTrimMainWindow_UI", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("VideoTrimMainWindow_UI", "Set In", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("VideoTrimMainWindow_UI", "Set Out", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("VideoTrimMainWindow_UI", "Back 5", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("VideoTrimMainWindow_UI", "Goto In Point", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setText(QtGui.QApplication.translate("VideoTrimMainWindow_UI", "Goto Out Point", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("VideoTrimMainWindow_UI", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSource_Files.setText(QtGui.QApplication.translate("VideoTrimMainWindow_UI", "Source Files", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCommmit.setText(QtGui.QApplication.translate("VideoTrimMainWindow_UI", "Commit", None, QtGui.QApplication.UnicodeUTF8))

import qt_assets_rc
