from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

from src.util.zviutil import getResource


class FlowMessage(QMessageBox):
    """Custom messagebox for flow"""
    def __init__(self, throwNum, parent=None):
        QMessageBox.__init__(self, parent=parent)
        self.setWindowTitle('Throw{0} Results:'.format(throwNum))
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowIcon(QIcon(getResource("zvilogo.ico")))
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.setFont(font)

    def closeEvent(self, event):
        self.close()


class MessageBox(QMessageBox):
    """Custom messagebox for gas components"""
    def __init__(self, parent=None):
        QMessageBox.__init__(self, parent=parent)
        self.setWindowTitle('Component Number')
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowIcon(QIcon(getResource("gas_icon.ico")))
        self.setText('Choose between 1-6 components')


class ThemeBox(QMessageBox):
    """Custom messagebox for theme"""
    def __init__(self, parent=None):
        QMessageBox.__init__(self, parent=parent)
        self.setWindowTitle('Theme Style')
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowIcon(QIcon(getResource("zvilogo.ico")))
        self.setIcon(self.Icon.Question)
        self.setText('Choose style')
        self.darkButton = self.addButton("Dark", QMessageBox.YesRole)
        self.lightButton = self.addButton("Light", QMessageBox.YesRole)
        self.addButton("Cancel", QMessageBox.RejectRole)


class StandardOK(QMessageBox):
    """Custom messagebox for theme"""
    def __init__(self, text, title="", parent=None):
        QMessageBox.__init__(self, parent=parent)
        self.setWindowTitle(title)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowIcon(QIcon(getResource("zvilogo.ico")))
        self.setIcon(self.Icon.Information)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Ok)


class WarningOK(QMessageBox):
    """Custom messagebox for theme"""
    def __init__(self, text, title="", parent=None):
        QMessageBox.__init__(self, parent=parent)
        self.setWindowTitle(title)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowIcon(QIcon(getResource("warning.ico")))
        self.setIcon(self.Icon.Warning)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Ok)
