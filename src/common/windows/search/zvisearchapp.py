from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QMainWindow, QApplication, QLabel, \
    QListWidget, QListWidgetItem, QMdiSubWindow, QAction, QTabWidget

from src.common.windows.mdi.zvilogin import ZVILogin

from src.common.windows.mdi.zvisignup import ZVISignup
from src.util.zviutil import getResource


class ZVISearchApp(QMainWindow):
    objectList = {}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.build()
        self.bind()

    def build(self):
        self.hideList = ["vs", "ms", "showvs", "showms", "showhw"]
        self.tabList = ["themes", "variables", "directories"]
        widget = QWidget()
        layout = QGridLayout(widget)
        self.searchLabel = QLabel("Searching for")
        layout.addWidget(self.searchLabel, 0, 0, 1, 1)
        self.searchResults = QListWidget()
        layout.addWidget(self.searchResults, 1, 0, 1, 2)

        self.setCentralWidget(widget)
        self.setWindowIcon(QIcon(getResource("search.ico")))
        self.setWindowTitle("Search...")
        self.setMinimumSize(300, 200)
        self.resize(300, 200)

    def bind(self):
        self.parent.searchAppText.returnPressed.connect(self.parent.searchAppButton.click)
        self.searchResults.itemDoubleClicked.connect(self.run)

    def find(self, text):
        loweredText = text.lower()
        self.clear()
        self.show()
        self.count = 0
        mapList = list(map(lambda item: item.get("name"), self.objectList.values()))
        for obj in self.parent.findChildren((QMdiSubWindow, QAction, QTabWidget)):
            name = obj.objectName().lower()
            if not loweredText:
                continue
            if isinstance(obj, QAction):
                name = name[6:].replace("_", " ")
                if name in self.hideList:
                    continue
                if loweredText in name and name not in mapList:
                    self.addToSearch(name, obj, "action")
            elif isinstance(obj, QMdiSubWindow):
                name = obj.widget().objectName().replace("_", " ").lower()
                if isinstance(obj.widget(), ZVILogin) or isinstance(obj.widget(), ZVISignup):
                    continue
                if loweredText in name and name not in mapList:
                    self.addToSearch(name, obj, "window")
            elif isinstance(obj, QTabWidget):
                for tab in range(obj.count()):
                    tabName = obj.tabText(tab).lower()
                    if loweredText in tabName and tabName in self.tabList:
                        self.addToSearch(obj.widget(tab).objectName(), obj.widget(tab), "tab", tabNum=tab)

        self.setResultText(text)

    def addToSearch(self, name, obj, objType, tabNum=None):
        item = QListWidgetItem(name.title())
        item.setSizeHint(QSize(0, 20))
        self.searchResults.insertItem(self.count, item)
        self.objectList[self.count] = {"name": name, "obj": obj, "objType": objType, "tabIndex": tabNum}
        self.count += 1

    def setResultText(self, text):
        result = self.searchResults.count()
        resultText = "result" if result == 1 else "results"
        self.searchLabel.setText("{0} {1} found for '{2}'. (Double-click item to run)".format(result, resultText, text))
        if result == 0:
            self.searchLabel.setText("No results found.")

    def run(self):
        row = self.searchResults.selectedIndexes()[0].row()
        obj = self.objectList[row]["obj"]
        objType = self.objectList[row]["objType"]
        if objType == "window":
            self.parent.setActiveSubWindow(type(obj.widget()))
        elif objType == "action":
            obj.trigger()
        elif objType == "tab":
            obj.parent().parent().setCurrentIndex(self.objectList[row]["tabIndex"])
            self.parent.setActiveSubWindow(type(obj.parent().parent().parent().parent()))
        self.close()

    def clear(self):
        self.objectList.clear()
        self.searchResults.clear()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = ZVISearchApp()
    w.show()
    sys.exit(app.exec_())
