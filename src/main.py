import sys

from PyQt5.QtWidgets import QApplication
from src.common.widgets.splashscreen.zvisplashscreen import SplashScreen

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    from PyQt5 import QtWebEngineWidgets
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    splash = SplashScreen()
    splash.showMessage("Importing dependencies...")
    from src.common.windows.zviapp import ZVIApp
    splash.showMessage("Initializing graphical user interface...")
    window = ZVIApp()
    splash.close()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
