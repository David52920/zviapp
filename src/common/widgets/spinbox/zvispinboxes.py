from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtCore import Qt

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent):
        super(DoubleSpinBox, self).__init__(parent)
        self.setRange(0, 100)
        self.setDecimals(15)
        self.setAlignment(Qt.AlignCenter)
        self.setButtonSymbols(2)

    def textFromValue(self, value):
        return str(format(value, '.15g'))
