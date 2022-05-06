from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from src.constants.zviconstants import constants
from src.util.zviutil import getResource


class SplashScreen(QSplashScreen):
    """Splash screen class for main ZVI application"""

    def __init__(self):
        splash_pix = QPixmap(getResource("zviwave.png"))
        if constants.isConnected:
            windowHint = Qt.WindowStaysOnTopHint
        else:
            windowHint = Qt.FramelessWindowHint
        super().__init__(splash_pix, windowHint)
        self.setMask(splash_pix.mask())
        self.show()

    def mousePressEvent(self, event):
        # disable default "click-to-dismiss" behaviour
        pass
