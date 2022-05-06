from PyQt5.QtGui import QStandardItem


class Item(QStandardItem):
    def __init__(self, text):
        super().__init__(text)
        self.objectName = ""
        self.setEditable(False)

    def setObjectName(self, text):
        self.objectName = text
