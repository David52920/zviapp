import os

from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QSpinBox, QComboBox,
                             QGridLayout, QFileDialog, QListWidgetItem, QListWidget, QTableWidget,
                             QInputDialog, QHeaderView)
from PyQt5.QtCore import Qt, QSortFilterProxyModel, pyqtSlot
from PyQt5.QtGui import QStandardItem, QIcon, QPixmap, QColor, QPainter, QPen, QFont

from src.common.widgets.colordialog.zvicolordialog import ColorDialog
from src.common.widgets.undo.zviundos import CommandEdit
from src.constants.zviconstants import constants
from src.common.widgets.messagebox.zvimessageboxes import ThemeBox
from src.common.windows.settings.ui.zvisettings_ui import Ui_Settings
from src.util.zviutil import setInDict


class ZVISettings(QMainWindow, Ui_Settings):
    """ZVI settings class"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.build()
        self.initWidgets()
        self.bind()

    def bind(self):
        self.localButton.clicked.connect(self.setPath)
        self.serverButton.clicked.connect(self.setPath)
        self.undoButton.clicked.connect(self.undoStack.undo)
        self.redoButton.clicked.connect(self.undoStack.redo)
        #self.rootModel.handleItemChanged.connect(self.handleItemChangedSlot)
        self.rootModel.itemChanged.connect(self.itemChangedSlot)
        self.filterEdit.textChanged.connect(self.onTextChanged)
        self.workingDirectoryButton.clicked.connect(self.changeWorkingDirectory)
        self.previousWorkingDirectoryButton.clicked.connect(self.setWorkingDirectory)
        self.previousValveSizingButton.clicked.connect(self.setValveSizingDirectory)
        self.revertButton.clicked.connect(self.revertAll)
        self.expandButton.clicked.connect(self.variablesTree.expandAll)
        self.collapseButton.clicked.connect(self.variablesTree.collapseAll)
        self.themeListWidget.itemClicked.connect(self.preview)
        self.themeListWidget.itemDoubleClicked.connect(self.setTheme)
        self.customThemeButton.clicked.connect(self.getCustomColor)

    def build(self):
        self.addThemeItems()
        self.setupTree()
        self.themeListWidget.setMaximumWidth(250)
        layout = QGridLayout()
        label = QLabel("Preview:")
        font = QFont()
        font.setPixelSize(12)
        font.setBold(True)
        label.setFont(font)
        layout.addWidget(label)
        layout.addWidget(QLabel("ComboBox:"))
        combo = QComboBox()
        combo.addItems(["Item1", "Item2"])
        layout.addWidget(combo)
        layout.addWidget(QLabel("Button:"))
        layout.addWidget(QPushButton("Push"))
        layout.addWidget(QLabel("LineEdit:"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QLabel("SpinBox:"))
        layout.addWidget(QSpinBox())
        layout.addWidget(QLabel("List:"))
        listWidget = QListWidget()
        listWidget.addItem(QListWidgetItem("Item1"))
        listWidget.addItem(QListWidgetItem("Item2"))
        listWidget.setCurrentRow(1)
        layout.addWidget(listWidget)
        layout.addWidget(QLabel("Table:"))
        table = QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(2)
        table.selectRow(0)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(table)
        self.previewWidget.setMinimumHeight(500)
        self.previewWidget.setLayout(layout)

    def initWidgets(self):
        self.valveSizingDirectoryEdit.setText(constants.directory["WD"])
        self.startupLineEdit.setText(constants.path["Server"])
        self.valveSizingListWidget.addItem(constants.directory["WD"])
        self.themeListWidget.setMouseTracking(True)
        self.workingDirectoryEdit.setEnabled(False)
        self.valveSizingDirectoryEdit.setEnabled(False)
        self.tabWidget.setCurrentIndex(0)
        themeRow = self.parent.userProps.value("theme/selectedRow")
        self.themeListWidget.setCurrentRow(int(themeRow) if themeRow else 0)

    def setupTree(self):
        self.refreshModel()
        self.proxyModel = QSortFilterProxyModel(self, filterKeyColumn=0, recursiveFilteringEnabled=True)
        self.proxyModel.setSourceModel(self.rootModel)
        self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.variablesTree.setModel(self.proxyModel)
        self.variablesTree.header().setMinimumSectionSize(300)
        self.variablesTree.expandAll()

    def preview(self, item):
        """Preview selected theme"""
        selected = item.text()
        if "Dark" in selected:
            self.background.setStyleSheet("background-color: rgb(53, 53, 53);")
        else:
            self.background.setStyleSheet("background-color: white;")
        palette = self.parent.themeManager.createPalette(selected)
        self.previewWidget.setPalette(palette)
        self.previewWidget.repaint()

    def setTheme(self, item):
        self.parent.userProps.setValue("theme/selectedRow", item.listWidget().row(item))
        self.parent.userProps.setValue("theme/themeName", item.text())
        self.parent.themeManager.setTheme(self.previewWidget.palette())
        self.repaint()
        self.setFocus()

    def addThemeItems(self):
        self.themeList = self.parent.userProps.value("theme/themeList")
        if not self.themeList:
            self.themeList = self.parent.themeList
        self.checkPalettes()
        for theme in self.themeList:
            pixmap = QPixmap(100, 100)
            color = self.parent.themeManager.paletteColorDict.get(theme)
            pixmap.fill(QColor("white") if color == "Default" else color)
            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.black, 8))
            painter.drawRect(pixmap.rect())
            painter.end()
            item = QListWidgetItem(QIcon(pixmap), theme)
            self.themeListWidget.addItem(item)

    def checkPalettes(self):
        if not self.parent.userProps.value("theme/themePalettes"):
            self.parent.userProps.setValue("theme/themeList", list(self.parent.themeManager.paletteColorDict.keys()))

    def getCustomColor(self):
        name, ok = QInputDialog.getText(self, "Theme Name", "Choose theme name")
        if name and ok:
            bMap = {0: "Dark", 1: "Light", 2: "Cancel"}
            themeMessage = ThemeBox(self)
            buttonClicked = themeMessage.exec()
            if buttonClicked != 2:
                colorDialog = ColorDialog(name, bMap[buttonClicked])
                colorDialog.colorSignal.connect(self.setSelectedColor)
                colorDialog.exec()

    def setSelectedColor(self, name, color, style):
        if color:
            name = name.title() + "-{0}".format(style)
            self.parent.userProps.setValue("theme/themeName", name)
            self.updateThemeList(name, color)
            self.parent.themeManager.setTheme(
                self.parent.themeManager.createCustomPalette(name, color, style))
            self.parent.userProps.setValue("theme/selectedRow",
                                           self.themeListWidget.row(
                                               self.themeListWidget.findItems(name, Qt.MatchContains)[0]))
            lastRow = self.themeListWidget.count() - 1
            self.themeListWidget.setCurrentRow(lastRow)
            self.preview(self.themeListWidget.item(lastRow))
            self.setFocus()

    def updateThemeList(self, name, color):
        pixmap = QPixmap(100, 100)
        pixmap.fill(color)
        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 8))
        painter.drawRect(pixmap.rect())
        painter.end()
        item = QListWidgetItem(QIcon(pixmap), name)
        self.themeListWidget.addItem(item)
        self.parent.themeManager.paletteColorDict[name] = color
        self.parent.userProps.setValue("theme/themeDict", self.parent.themeManager.paletteColorDict)
        if name not in self.themeList:
            self.themeList.append(name)
            self.parent.userProps.setValue("theme/themeList", self.themeList)

    @pyqtSlot(str)
    def onTextChanged(self, text):
        """During typing it will filter out results"""
        self.variablesTree.expandAll()
        self.proxyModel.setFilterRegularExpression(text)
        self.variablesTree.expandAll()

    @staticmethod
    def findTopLevel(item):
        parents = [item.parent().child(item.row(), 0).text()]
        while item.parent():
            item = item.parent()
            parents.append(item.text())
        parents.reverse()
        return parents

    def itemChangedSlot(self, item):
        """Handle change info for user input (changes current values)"""
        try:
            levels = self.findTopLevel(item)
            parent = levels[0]
            if parent == "Other":
                setInDict(constants.jsons["Other"], levels[1:], float(item.text()))
            else:
                pass
        except (AttributeError, ValueError):
            pass

    def handleItemChangedSlot(self, item, oldValue, newValue, role):
        if role == Qt.EditRole:
            command = CommandEdit(self, item, oldValue, newValue)
            self.undoStack.push(command)

    def revertAll(self):
        """ Revert all variables to original values"""
        if self.startupLineEdit.text() == constants.path["Server"]:
            constants.initJSON(constants.path["Server"])
        else:
            constants.initJSON()

        self.refreshModel()

    def fill_model(self, parent, d):
        """Fill treeview with all dictionary items"""
        if isinstance(d, dict):
            for key, value in d.items():
                if str(key) == 'Add':
                    pass
                elif str(key) == '':
                    pass
                else:
                    it = QStandardItem(str(key))
                    it.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    if isinstance(value, dict):
                        parent.appendRow(it)
                        self.fill_model(it, value)
                    elif isinstance(value, tuple):
                        parent.appendRow(it)
                        self.fill_model(it, value[1])
                    elif isinstance(value, list):
                        parent.appendRow(it)
                        self.fill_model(it, value)
                    else:
                        if it.text() == "Material":
                            continue
                        if parent.text() == "Other":
                            it2 = QStandardItem(str(value[0]))
                            parent.appendRow([it, it2])
                        else:
                            it2 = QStandardItem(str(value))
                            parent.appendRow([it, it2])
        elif isinstance(d, list):
            it = QStandardItem(str(d[0]))
            it.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            it1 = QStandardItem(str(d[1]))
            it1.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            parent.appendRow(it)
            parent.appendRow(it1)

    def refreshModel(self):
        """Refresh settings model to previous values from server/local"""
        self.rootModel.removeRows(0, self.rootModel.rowCount())
        tree = {} # private
        self.fill_model(self.rootModel.invisibleRootItem(), tree)
        self.variablesTree.expandAll()

    def setWorkingDirectory(self):
        """Change directory to selected item """
        selected = self.workingDirectoryListWidget.selectedItems()
        if len(selected) != 0 and os.path.exists(selected[0].text()):
            os.chdir(selected[0].text())
            self.workingDirectoryEdit.setText(selected[0].text())

    def setValveSizingDirectory(self):
        """Change directory to selected item """
        selected = self.valveSizingListWidget.selectedItems()
        if len(selected) != 0 and os.path.exists(selected[0].text()):
            constants.directory["ValveSizing"] = selected[0].text()
            self.valveSizingDirectoryEdit.setText(selected[0].text())

    def changeWorkingDirectory(self):
        """Change working directory """
        directory = str(
            QFileDialog.getExistingDirectory(self, "Select Working Directory", options=QFileDialog.DontUseNativeDialog))
        if directory:
            self.workingDirectoryEdit.setText(directory)
            if self.workingDirectoryListWidget.count() < 20:
                self.workingDirectoryListWidget.addItem(directory)
            else:
                self.workingDirectoryListWidget.takeItem(0)
                self.workingDirectoryListWidget.addItem(directory)
            constants.directory["Working"] = directory
            os.chdir(directory)
        return directory

    def changeValveSizingDirectory(self):
        """Change valvesizing directory """
        directory = str(QFileDialog.getExistingDirectory(self, "Select ValveSizing Directory",
                                                         options=QFileDialog.DontUseNativeDialog))
        if directory:
            self.valveSizingDirectoryEdit.setText(directory)
            self.valveSizingListWidget.addItem(directory)
            constants.directory["ValveSizing"] = directory
        return directory

    def setPath(self):
        """Set path for server info"""
        if self.sender() == self.serverButton:
            self.startupLineEdit.setText(constants.path["Server"])
            constants.initJSON(constants.path["Server"])
        elif self.sender() == self.localButton:
            self.startupLineEdit.setText(constants.path["Local"])
            constants.initJSON()
        self.refreshModel()


def main():
    import sys
    app = QApplication(sys.argv)
    ZVIwindow = ZVISettings()
    ZVIwindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
