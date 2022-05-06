import os
import socket
import getpass

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPixmap

from src.common.widgets.messagebox.zvimessageboxes import WarningOK
from src.common.windows.mdi.ui.zvisignup_ui import Ui_signUp
from src.constants.zviconstants import constants


class ZVISignup(QWidget, Ui_signUp):
    """Signup setup class"""
    hideWindow = pyqtSignal()

    def __init__(self, databaseManager, emailManager, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.databaseManager = databaseManager
        self.emailManager = emailManager
        self.build()
        self.bind()
        self.initWidgets()

    @staticmethod
    def getSize():
        return QSize(400, 300)

    def build(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        self.setWindowIcon(QIcon(pixmap))

    def bind(self):
        self.signupButton.clicked.connect(self.signup)

    def initWidgets(self):
        self.signupButton.setAutoDefault(True)
        self.workstationEdit.setText(socket.gethostname())

    def signup(self):
        """Insert data into database """
        try:
            username = self.usernameEdit.text()
            email = self.emailEdit.text()
            password = self.passwordEdit.text()
            wStation = self.workstationEdit.text() if self.workstationEdit.text() != "" else os.environ['COMPUTERNAME']
            vsLocation = self.valveSizingEdit.text()
            missingFields = self.checkEmptyRequirements()
            if missingFields != "":
                self.showMessageBox('Missing Fields', "Fill out the required missing fields; {0}".format(missingFields))
            else:
                result = self.databaseManager.execute("SELECT USERNAME FROM USERS WHERE USERNAME=?",
                                                      (username.title(),))
                if not result:
                    self.databaseManager.execute("INSERT INTO USERS VALUES(?,?,?,?,?)",
                                                 (username.title(), email, password, wStation, vsLocation))
                    if email != "":
                        self.sendVerificationEmail(username, email, password, vsLocation)
                    else:
                        self.showMessageBox('Account', 'Account Created.')
                    self.hideWindow.emit()
                    self.clear()
                else:
                    self.showMessageBox('Warning',
                                        '{0} already exists. Choose a different username.'.format(username.title()))
        except ConnectionError:
            self.showMessageBox('Database Error', 'Unable to connect; verify database path')
            constants.logger.exception('Exception occurred:')

    def checkEmptyRequirements(self):
        widgets = [self.usernameEdit, self.passwordEdit, self.workstationEdit, self.valveSizingEdit]
        requirements = []
        for widget in widgets:
            if widget.text() == "":
                requirements.append(widget.objectName())
        if len(requirements) > 0:
            return ", ".join(requirements)
        return ""

    def sendVerificationEmail(self, username, email, password, vsLocation):
        self.emailManager.sendHTMLEmail(email,
                                        'ZVIApp Account Created Successfully.',
                                        ("Your account has been added to the database, please verify the following information;<br> \
                                <ul>\
                                <li> Computer Login: '{login}'</li>\
                                <li> Username: '{user}'</li>\
                                <li> Password: '{zvipass}'</li>\
                                <li> Workstation: '{station}'</li>\
                                <li> ValveSizing Location: '{vslocation}'</li>\
                                </ul>\
                                To change any of the information, respond to this email.<br>\
                                <br>\
                                Best regards,<br>\
                                &emsp; ZVIApp Administrator\
                                ".format(login=getpass.getuser(), user=username.title(),
                                         station=os.environ['COMPUTERNAME'], vslocation=vsLocation,
                                         zvipass=password)))

    def showMessageBox(self, title, message):
        """Message Box popup"""
        msgBox = WarningOK(message, title, parent=self)
        msgBox.exec()

    def clear(self):
        widgets = [self.usernameEdit, self.passwordEdit, self.emailEdit, self.valveSizingEdit]
        for widget in widgets:
            widget.clear()


def main():
    import sys
    app = QApplication(sys.argv)
    ZVIwindow = ZVISignup()
    ZVIwindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
