import os
import json
import sys
import atexit
import urllib.request

from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication
from PyQt5.QtCore import Qt

from src.common.windows.update.ui.zviupdate_ui import Ui_Update
from src.constants.zviconstants import constants


class UpdateApp(QMainWindow, Ui_Update):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.userDesktop = constants.fileDialogPath
        self.desktopcopy = None
        self.initWidget()
        self.bind()

    def initWidget(self):
        self.current_version.setText("{0}".format(constants.version))
        self.available_version.setText("-")
        self.current_version.setDisabled(True)
        self.available_version.setDisabled(True)

    def bind(self):
        self.checkButton.clicked.connect(self.performUpdate)

    def getUpdateQuery(self):
        with urllib.request.urlopen(constants.updateQuery["URL"] + constants.updateQuery["File"]) as url:
            self.updateQueryInfo = json.loads(url.read().decode())

    def checkVersion(self):
        self.getUpdateQuery()
        self.available_version.setText("{0}".format(self.updateQueryInfo["Version"]))
        return constants.version == str(self.updateQueryInfo["Version"])
    
    def performUpdate(self):
        try:
            if self.checkVersion():
                print("ZVIApp is using the current version: {0}".format(self.updateQueryInfo["Version"]))
                QMessageBox.information(self, 'Version Info',
                                        "ZVIApp is using the current version: {0}".format(self.updateQueryInfo["Version"]), QMessageBox.Ok)
                return True
            else:
                print("ZVIApp Version {0} is available".format(self.updateQueryInfo["Version"]))
                reply = QMessageBox.question(self, 'Version info',
                                             "Would you like to download ZVIApp version {0}?".format(
                                                 self.updateQueryInfo["Version"]),
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    print("Installing new version. Please wait.")
                    # self.downloadQuery = DownloadQuery(constants.updateQuery["URL"],
                    #                                    constants.updateQueryInfo["Installer"],
                    #                                    self.userDesktop)
                    # self.downloadQuery.finished.connect(self.restart)
                    # self.downloadQuery.start()
                    return False
                else:
                    return True
        except FileNotFoundError:
            print("File Not found")

    def restart(self, installer):
        reply = QMessageBox.question(self, 'Info',
                                     """ZVIApp needs to close to process update.
Saving your work is suggested before installing new version.
Would you like to continue?""", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            atexit.register(os.execl, installer, installer)
            sys.exit()
        else:
            print("User to save work before proceeding.")


def main():
    app = QApplication(sys.argv)
    Update_Window = UpdateApp()
    Update_Window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
