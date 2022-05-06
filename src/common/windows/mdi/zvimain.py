from PyQt5.QtWidgets import QApplication, QMainWindow

from src.common.windows.mdi.ui.zvimain_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """Mainwindow setup class"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


def main():
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
