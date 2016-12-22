# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\vidtrim\SourceFileChooserDialog_UI.ui'
#
# Created: Wed Dec 21 16:57:15 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SourceFileChooserDialog_UI(object):
    def setupUi(self, SourceFileChooserDialog_UI):
        SourceFileChooserDialog_UI.setObjectName("SourceFileChooserDialog_UI")
        SourceFileChooserDialog_UI.resize(653, 439)
        self.buttonBox = QtGui.QDialogButtonBox(SourceFileChooserDialog_UI)
        self.buttonBox.setGeometry(QtCore.QRect(230, 400, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.source_files_tbl = QtGui.QTableWidget(SourceFileChooserDialog_UI)
        self.source_files_tbl.setGeometry(QtCore.QRect(50, 100, 551, 271))
        self.source_files_tbl.setObjectName("source_files_tbl")
        self.source_files_tbl.setColumnCount(0)
        self.source_files_tbl.setRowCount(0)
        self.label = QtGui.QLabel(SourceFileChooserDialog_UI)
        self.label.setGeometry(QtCore.QRect(50, 20, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(SourceFileChooserDialog_UI)
        self.label_2.setGeometry(QtCore.QRect(50, 50, 91, 16))
        self.label_2.setObjectName("label_2")
        self.browse_btn = QtGui.QPushButton(SourceFileChooserDialog_UI)
        self.browse_btn.setGeometry(QtCore.QRect(520, 50, 75, 23))
        self.browse_btn.setObjectName("browse_btn")
        self.source_dir_input = QtGui.QLineEdit(SourceFileChooserDialog_UI)
        self.source_dir_input.setGeometry(QtCore.QRect(180, 50, 321, 20))
        self.source_dir_input.setObjectName("source_dir_input")
        self.pushButton = QtGui.QPushButton(SourceFileChooserDialog_UI)
        self.pushButton.setGeometry(QtCore.QRect(610, 100, 31, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(SourceFileChooserDialog_UI)
        self.pushButton_2.setGeometry(QtCore.QRect(610, 130, 31, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(SourceFileChooserDialog_UI)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SourceFileChooserDialog_UI.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SourceFileChooserDialog_UI.reject)
        QtCore.QMetaObject.connectSlotsByName(SourceFileChooserDialog_UI)

    def retranslateUi(self, SourceFileChooserDialog_UI):
        SourceFileChooserDialog_UI.setWindowTitle(QtGui.QApplication.translate("SourceFileChooserDialog_UI", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SourceFileChooserDialog_UI", "Source Video Files", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SourceFileChooserDialog_UI", "Source Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_btn.setText(QtGui.QApplication.translate("SourceFileChooserDialog_UI", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("SourceFileChooserDialog_UI", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("SourceFileChooserDialog_UI", "Dwn", None, QtGui.QApplication.UnicodeUTF8))

