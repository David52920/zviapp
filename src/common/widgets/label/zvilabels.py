from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, Qt


class Label(QLabel):
    def __init__(self, txt="", bold=False, parent=None):
        super().__init__()
        self.setText(txt)
        font = QFont()
        font.setPointSize(10)
        font.setBold(bold)
        self.setFont(font)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);


class LinkLabel(QLabel):
    clicked=pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()


class CalculateLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.setMinimumWidth(100)
        self.setAlignment(Qt.AlignHCenter)


class HeaderLabel(QLabel):
    def __init__(self, txt, isAligned=False):
        super().__init__()
        self.setText(txt)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)
        if isAligned:
            self.setMinimumWidth(100)
            self.setAlignment(Qt.AlignHCenter)

