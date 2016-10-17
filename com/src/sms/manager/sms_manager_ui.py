# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sms_manager.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import os
import re

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

class Ui_MainWindow(object):
    def fileContentsUpdate(self):
        if os.path.exists(FNAME):
            file_reader = open(FNAME, "r")
            lines = file_reader.readlines()
            file_reader.close()

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

        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 140, 391, 401))
        self.listWidget.setObjectName(_fromUtf8("listView"))


        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 40, 191, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))


        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 90, 191, 27))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))

        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 40, 81, 26))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.add_contents)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 90, 81, 26))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.clicked.connect(self.delete_contents)

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
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.retranslateUi(MainWindow)
        MainWindow.setTabOrder(self.pushButton, self.listWidget)

        self.fileContentsUpdate()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

        self.label.setText(_translate("MainWindow", "Cell phone.  ", None))

        self.label_2.setText(_translate("MainWindow", "Name.  ", None))

        self.pushButton.setText(_translate("MainWindow", "ADD", None))

        self.pushButton_2.setText(_translate("MainWindow", "DELETE", None))

        self.menuSetting_SMS_Service.setTitle(_translate("MainWindow", "Manage SMS Service", None))

    def add_contents(self):
        name = self.lineEdit.text()
        phone = self.lineEdit_2.text()
        checked_phone = self.checkPhonenumber(phone)

        if not checked_phone == None:
            info = str(name)
            info += str("/" + phone + "\n")
            infoList.append(info)

            file_writer = open(FNAME, "w")
            for x in infoList:
                file_writer.write(x)
            self.listUpdate(info)
            file_writer.close()

        else:
            self.lineEdit_2.setText("ex) 01012345678")

    def delete_contents(self):
        listItem = list()
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        item = None
        self.listWidget.repaint()

        for x in range(self.listWidget.count()):
            listItem.append(str(self.listWidget.item(x).text()))

        # [for test] print listItem

        file_writer = open(FNAME, "w")
        for x in listItem:
            file_writer.write(x + "\n")
        file_writer.close()

    def checkPhonenumber(self, phone):
        if len(phone) == 11:
            st = re.match(r"01[0-1][0-9]+", phone)
        else:
            st = None

        if st == None:
            return None
        elif len(st.group()) == 11:
            return st
        else:
            return None

    def listUpdate(self, info):
        self.listWidget.addItem(info[:-1])
        self.listWidget.repaint()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
