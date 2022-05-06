from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon

from src.util.zviutil import getResource


class Ui_System_Info(object):
    def setupUi(self, System_Info):
        System_Info.setObjectName("System_Info")
        System_Info.resize(386, 376)
        System_Info.setMaximumSize(QtCore.QSize(16777215, 376))
        self.setWindowIcon(QIcon(getResource("zvilogo.ico")))
        self.centralwidget = QtWidgets.QWidget(System_Info)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(332, 358))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 358))
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(13)
        for i in range(13):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        System_Info.setCentralWidget(self.centralwidget)

        self.retranslateUi(System_Info)
        QtCore.QMetaObject.connectSlotsByName(System_Info)

    def retranslateUi(self, System_Info):
        _translate = QtCore.QCoreApplication.translate
        System_Info.setWindowTitle(_translate("System_Info", "System Information"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("System_Info", "Computer Name:"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("System_Info", "Domain:"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("System_Info", "Username:"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("System_Info", "ValveSizing Directory:"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("System_Info", "System"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("System_Info", "Operating System:"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("System_Info", "Network"))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("System_Info", "Type:"))
        item = self.tableWidget.verticalHeaderItem(10)
        item.setText(_translate("System_Info", "Description:"))
        item = self.tableWidget.verticalHeaderItem(11)
        item.setText(_translate("System_Info", "Mac Address:"))
        item = self.tableWidget.verticalHeaderItem(12)
        item.setText(_translate("System_Info", "IP Address:"))
        item = self.tableWidget.verticalHeaderItem(14)