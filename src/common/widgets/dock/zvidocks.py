from PyQt5.QtWidgets import QDockWidget

from src.constants.zviconstants import constants


class Dock(QDockWidget):
    def __init__(self, cDisplay, dDisplay):
        super(Dock, self).__init__()
        self.cDisplay = cDisplay
        self.dDisplay = dDisplay
        self.displayMap = {"compressor": self.cDisplay, "driver": self.dDisplay}
        self.open = False
        self.hide()

    def configure(self, obj):
        self.open = True
        self.resetDisplayStyles()
        if obj["display"]:
            self.setActiveDisplayStyle(obj["display"])
        self.setWindowTitle(obj["title"])
        self.setWidget(obj["view"])
        self.show()

    def setActiveDisplayStyle(self, display):
        if display and not isinstance(display, int):
            self.displayMap[display].setStyleSheet(constants.styles.activeStyle)
        else:
            tDisplay = self.cDisplay.compressor.getThrowByNumber(display, asDisplay=True)
            tDisplay.setStyleSheet(constants.styles.activeStyle)

    def resetDisplayStyles(self):
        self.cDisplay.setStyleSheet(constants.styles.inactiveStyle)
        self.dDisplay.setStyleSheet(constants.styles.inactiveStyle)
        for tDisplay in self.cDisplay.compressor.throws:
            tDisplay.setStyleSheet(constants.styles.inactiveStyle)

    def showEvent(self, event):
        self.setMinimumSize(self.minimumSizeHint())
        super().showEvent(event)
