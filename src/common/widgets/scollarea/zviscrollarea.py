from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt

class ScrollArea(QScrollArea):
    def __init__(self, window, parent=None):
        super().__init__()
        self.setMinimumSize(500,500)
        self.setWidgetResizable(False)
        self.setAlignment(Qt.AlignHCenter)
        self.setWidget(window)
