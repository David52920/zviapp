from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QColorDialog, QPushButton, QHBoxLayout, QVBoxLayout, QDialog

from src.util.zviutil import getResource


class ColorDialog(QDialog):
    colorSignal = pyqtSignal(object, object, object)

    def __init__(self, name, style, parent=None):
        super().__init__(parent)
        self.name = name
        self.style = style
        self.build()

    def build(self):
        self.setWindowTitle("Select Theme Color")
        self.setWindowIcon(QIcon(getResource("colorwheel.ico")))
        self.widget = QColorDialog()
        self.widget.setWindowFlags(Qt.Widget)
        self.widget.setOptions(QColorDialog.DontUseNativeDialog | QColorDialog.NoButtons)
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)
        ok = QPushButton('Ok')
        cancel = QPushButton('Cancel')
        ok.clicked.connect(self.selectColor)
        cancel.clicked.connect(self.close)
        hbox = QHBoxLayout()
        hbox.addWidget(ok)
        hbox.addWidget(cancel)
        layout.addLayout(hbox)

    def selectColor(self):
        self.colorSignal.emit(self.name, self.widget.currentColor(), self.style)
        self.close()