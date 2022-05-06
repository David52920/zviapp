import os
import subprocess
import shutil

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox, QFileDialog, QApplication

from src.constants.zviconstants import constants
from src.common.windows.mdi.ui.zvihome_ui import Ui_HomeWindow


class ZVIHome(QMainWindow, Ui_HomeWindow):
    """Homewindow setup class"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.bind()

    @staticmethod
    def getSize():
        return QSize(258, 345)

    def bind(self):
        self.openDirectoryButton.clicked.connect(self.openDirectory)
        self.openTemplatesButton.clicked.connect(self.openTemplates)
        self.openProjectsButton.clicked.connect(self.openProjects)
        self.createProjectFolderButton.clicked.connect(self.newProject)

    def createFolders(self, mainDirectory):
        """create folder method """
        try:
            SOA, ok = QInputDialog.getText(self, "#", "Provide #, if none enter customer name.\nAvoid spaces.")
            if SOA and ok:
                exampleDirectory = self.createDirectories(mainDirectory)
                self.copyFilesTo(SOA, mainDirectory, exampleDirectory)
                subprocess.call('explorer "{0}"'.format(mainDirectory), shell=False)
        except:
            constants.logger.exception('Exception occurred:')

    @staticmethod
    def createDirectories(mainDirectory):
        exampleDirectory = '{0}\\Exampl'.format(mainDirectory)
        os.makedirs(mainDirectory)
        os.makedirs(exampleDirectory)
        return exampleDirectory

    def copyFilesTo(self, SOA, mainDirectory, ex, ex1):
        pass

    def newProject(self):
        """check whether or not project is new"""
        try:
            reply = QMessageBox.question(self, 'Customer', "Is project for new customer?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                customer, ok = QInputDialog.getText(self, "Customer", "Enter customer name.")
                if customer and ok:
                    location, ok = QInputDialog.getText(self, "Location", "Enter location name.")
                    if location and ok:
                        self.createFolders(
                            "{0}\\{1}\\{2}".format(constants.jsons["Paths"]['Projects'], customer, location))
            elif reply == QMessageBox.No:
                reply = QMessageBox.question(self, 'Location', "Is project for new location?",
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    fileDirectory = str(QFileDialog.getExistingDirectory(self, "Select Customer Folder",
                                                                         options=QFileDialog.DontUseNativeDialog))
                    location, ok = QInputDialog.getText(self, "Location", "Enter location name.")
                    if location and ok:
                        self.createFolders('{0}\\{1}'.format(fileDirectory, location))
                elif reply == QMessageBox.No:
                    fileDirectory = str(QFileDialog.getExistingDirectory(self, "Select Directory",
                                                                         options=QFileDialog.DontUseNativeDialog))
                    if fileDirectory != "":
                        self.createFolders('{0}'.format(fileDirectory))
        except:
            constants.logger.exception('Exception occurred:')

    @staticmethod
    def openDirectory():
        """open working directory in explorer """
        if constants.system == "Windows":
            subprocess.call('explorer "{0}"'.format(os.getcwd()), shell=False)
        else:
            subprocess.call(['xdg-open', "{0}".format(os.getcwd())])

    @staticmethod
    def openTemplates():
        """open templates directory in explorer """
        if os.path.exists(constants.jsons["Paths"]['Template']):
            if constants.system == "Windows":
                subprocess.call(
                    'explorer "{0}"'.format("{0}".format(constants.jsons["Paths"]['Template']), shell=False))
            else:
                subprocess.call(['xdg-open', "{0}".format(constants.jsons["Paths"]['Template'])])

    @staticmethod
    def openProjects():
        """open projects directory in explorer """
        if os.path.exists(constants.jsons["Paths"]['Projects']):
            if constants.system == "Windows":
                subprocess.call(
                    'explorer "{0}"'.format("{0}".format(constants.jsons["Paths"]['Projects']), shell=False))
            else:
                subprocess.call(['xdg-open', "{0}".format(constants.jsons["Paths"]['Projects'])])


def main():
    import sys
    app = QApplication(sys.argv)
    ZVIwindow = ZVIHome()
    ZVIwindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
