# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sms_manager.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import os

FNAME = "./phone_book"
infoList = list()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

@pyqtSlot


class Ui_MainWindow(object):
    def fileContentsUpdate(self):
        if os.path.exists(FNAME):
            file_reader = open(FNAME, "r")
            lines = file_reader.readlines()
            for line in lines:
                if line:
                    infoList.append(line)
        for info in infoList:
            self.listUpdate(info)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(429, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 90, 91, 20))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 81, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.listView = QtGui.QListWidget(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(20, 140, 391, 401))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 40, 191, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 90, 191, 27))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))

        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 60, 81, 26))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.add_contents)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 429, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSetting_SMS_Service = QtGui.QMenu(self.menubar)
        self.menuSetting_SMS_Service.setObjectName(_fromUtf8("menuSetting_SMS_Service"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuSetting_SMS_Service.menuAction())
        self.label.setBuddy(self.lineEdit_2)
        self.label_2.setBuddy(self.lineEdit)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton, self.listView)

        self.fileContentsUpdate()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Cell phone.  ", None))

        self.label_2.setText(_translate("MainWindow", "Name.  ", None))

        self.pushButton.setText(_translate("MainWindow", "ADD", None))

        self.menuSetting_SMS_Service.setTitle(_translate("MainWindow", "Manage SMS Service", None))

    def add_contents(self):
        name = self.lineEdit.text()
        phone = self.lineEdit_2.text()
        info = str(name)
        info += str("/" + phone + "\n")
        infoList.append(info)

        file_writer = open(FNAME, "w")
        for x in infoList:
            file_writer.write(x)
        self.listUpdate(info)


    def listUpdate(self, info):
        self.listView.addItem(info[:-1])
        self.listView.repaint()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
