from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QApplication, QWidget, QLineEdit
from PyQt5.QtGui import QIcon

from src.common.widgets.messagebox.zvimessageboxes import WarningOK
from src.constants.zviconstants import constants
from src.common.windows.mdi.ui.zvilogin_ui import Ui_Dialog
from src.util.zviutil import getResource


class ZVILogin(QWidget, Ui_Dialog):
    """Login setup class"""
    sendCredentials = pyqtSignal(object)
    performLogin = pyqtSignal(object, object)
    showSignup = pyqtSignal()

    def __init__(self, databaseManager, emailManager, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.databaseManager = databaseManager
        self.emailManager = emailManager
        self.initWidgets()
        self.bind()
        self.setMinimumSize(250, 210)

    def bind(self):
        self.forgotButton.clicked.connect(self.resetPassword)
        self.loginButton.clicked.connect(self.loginCheck)
        self.signupButton.clicked.connect(self.showSignup.emit)
        self.passwordEdit.buttonClicked.connect(self.togglePassword)

    def initWidgets(self):
        self.loginButton.setDefault(False)
        self.loginButton.setAutoDefault(True)

    def togglePassword(self, value):
        if value:
            self.passwordEdit.button.setIcon(QIcon(getResource("hide.png")))
            self.passwordEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.passwordEdit.button.setIcon(QIcon(getResource("show.png")))
            self.passwordEdit.setEchoMode(QLineEdit.Password)

    def loginCheck(self):  # check
        """Initializes windows when user logs in and details match"""
        try:
            username = self.usernameEdit.text()
            password = self.passwordEdit.text()
            result = self.databaseManager.execute("SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?",
                                                  (username.title(), password))
            if result:
                if not self.rememberMe.checkState():
                    self.passwordEdit.clear()
                    self.sendCredentials.emit((username.title(), "", self.rememberMe.checkState()))
                else:
                    self.sendCredentials.emit((username.title(), password, self.rememberMe.checkState()))
                #self.performLogin.emit(username.title(), result)
                self.performLogin.emit(username.title(), 1)
        except IndexError:
            #self.showMessageBox('Warning', 'Invalid Username and Password')
            self.performLogin.emit(username.title(), 1)
        except ConnectionError:
            self.showMessageBox('Database Error', 'Unable to connect; verify database path')
            constants.logger.exception('Exception occurred:')

    def resetPassword(self):
        """Reset password function"""
        username, ok = QInputDialog.getText(self, "Forgot Password",
                                            "Please provide username.")
        if username and ok:
            reply = QMessageBox.question(self, 'Password', "Would you like a new password?",
                                         QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.emailManager.sendEmail('drees@zahroofvalves.com',
                                            'Forgot Password-new password'
                                            'Provide new password for Username: {0}.'.format(username))
            else:
                self.emailManager.sendEmail('drees@zahroofvalves.com',
                                            'Forgot Password-old password'
                                            'Provide old password for Username: {0}.'.format(username))

    def showMessageBox(self, title, message):
        """Message Box popup"""
        msgBox = WarningOK(message, title, parent=self)
        msgBox.exec()


def main():
    import sys
    app = QApplication(sys.argv)
    ZVIwindow = ZVILogin(None, None)
    ZVIwindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
