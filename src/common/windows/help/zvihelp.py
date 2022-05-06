import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QTextBrowser, QMainWindow, QApplication, QTabWidget, QSplitter
from PyQt5.QtHelp import QHelpEngine

from src.util.zviutil import getResource

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class HelpBrowser(QTextBrowser):
    def __init__(self, helpEngine, parent=None):
        super().__init__(parent)
        self.helpEngine = helpEngine

    def loadResource(self, _type, name):
        if name.scheme() == "qthelp":
            return self.helpEngine.fileData(name)
        else:
            return super().loadResource(_type, name)


class ZVIHelp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.build()

    def build(self):
        self.helpEngine = QHelpEngine(getResource("zvihelp.qhc"))
        self.helpEngine.setupData()

        tWidget = QTabWidget()
        tWidget.setMaximumWidth(280)
        tWidget.addTab(self.helpEngine.contentWidget(), "Contents")
        tWidget.addTab(self.helpEngine.indexWidget(), "Index")

        textViewer = HelpBrowser(self.helpEngine)
        textViewer.setSource(QUrl.fromLocalFile(getResource("general.html")))

        horizSplitter = QSplitter(Qt.Horizontal)
        horizSplitter.insertWidget(0, tWidget)
        horizSplitter.insertWidget(1, textViewer)

        self.helpEngine.setUsesFilterEngine(True)
        self.helpEngine.contentWidget().linkActivated.connect(textViewer.setSource)
        self.helpEngine.indexWidget().linkActivated.connect(textViewer.setSource)
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.addWidget(horizSplitter)
        self.setCentralWidget(widget)
        self.setWindowIcon(QIcon(getResource("question.ico")))
        self.setWindowTitle("ZVI Help")
        self.setMinimumSize(500, 500)
        self.resize(640, 480)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = ZVIHelp()
    w.show()
    sys.exit(app.exec_())
