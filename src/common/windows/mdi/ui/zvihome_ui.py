from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap

from src.util.zviutil import getResource


class Ui_HomeWindow(object):
    def setupUi(self, HomeWindow):
        HomeWindow.setObjectName("Home")
        HomeWindow.setWindowModality(QtCore.Qt.WindowModal)
        HomeWindow.resize(221, 267)
        HomeWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(HomeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.openDirectoryButton = QtWidgets.QPushButton(self.groupBox)
        self.openDirectoryButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.openDirectoryButton, 4, 0, 1, 1)
        self.startModuleProgramButton = QtWidgets.QPushButton(self.groupBox)
        self.startModuleProgramButton.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.startModuleProgramButton, 0, 0, 1, 1)
        self.showVSButton = QtWidgets.QPushButton(self.groupBox)
        self.showVSButton.setObjectName("pushButton_4")
        self.gridLayout_3.addWidget(self.showVSButton, 2, 0, 1, 1)
        self.openTemplatesButton = QtWidgets.QPushButton(self.groupBox)
        self.openTemplatesButton.setObjectName("pushButton_5")
        self.gridLayout_3.addWidget(self.openTemplatesButton, 5, 0, 1, 1)
        self.showMSButton = QtWidgets.QPushButton(self.groupBox)
        self.showMSButton.setObjectName("pushButton_3")
        self.gridLayout_3.addWidget(self.showMSButton, 1, 0, 1, 1)
        self.openProjectsButton = QtWidgets.QPushButton(self.groupBox)
        self.openProjectsButton.setObjectName("pushButton_6")
        self.gridLayout_3.addWidget(self.openProjectsButton, 6, 0, 1, 1)
        self.createProjectFolderButton = QtWidgets.QPushButton(self.groupBox)
        self.createProjectFolderButton.setObjectName("projectsFolder")
        self.gridLayout_3.addWidget(self.createProjectFolderButton, 7, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.label.setPixmap(QPixmap(getResource('zvilogo.bmp')))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        HomeWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(HomeWindow)
        QtCore.QMetaObject.connectSlotsByName(HomeWindow)
        HomeWindow.setTabOrder(self.startModuleProgramButton, self.showMSButton)
        HomeWindow.setTabOrder(self.showMSButton, self.showVSButton)
        HomeWindow.setTabOrder(self.showVSButton, self.openDirectoryButton)
        HomeWindow.setTabOrder(self.openDirectoryButton, self.openTemplatesButton)
        HomeWindow.setTabOrder(self.openTemplatesButton, self.openProjectsButton)
        HomeWindow.setTabOrder(self.openProjectsButton, self.createProjectFolderButton)

    def retranslateUi(self, HomeWindow):
        _translate = QtCore.QCoreApplication.translate
        HomeWindow.setWindowTitle(_translate("HomeWindow", "Home"))
        self.groupBox.setTitle(_translate("HomeWindow", "View"))
        self.openDirectoryButton.setText(_translate("HomeWindow", "Directory"))
        self.startModuleProgramButton.setText(_translate("HomeWindow", "MP"))
        self.showVSButton.setText(_translate("HomeWindow", "VS"))
        self.openTemplatesButton.setText(_translate("HomeWindow", "Templates"))
        self.showMSButton.setText(_translate("HomeWindow", "MS"))
        self.openProjectsButton.setText(_translate("HomeWindow", "Projects"))
        self.createProjectFolderButton.setText(_translate("HomeWindow", "Create New Projects Folder"))
