from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTableView, QAbstractItemView, \
    QApplication
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QSize
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon

from src.constants.zviconstants import constants
from src.common.widgets.delegate.zvidelegates import ComboDelegate
from src.util.zviutil import getResource

if constants.system == "Windows":
    import win32com.client

    outApp = win32com.client.gencache.EnsureDispatch("Outlook.Application")
    outGAL = outApp.Session.GetGlobalAddressList()
    entries = outGAL.AddressEntries


class ZVIMail(QWidget):
    """Class for ZVImail which contains wrappers to send emails more effectively"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.build()
        self.bind()

    def build(self):
        self.setObjectName("Mail_Address_Book")
        self.layout = QVBoxLayout(self)
        self.filterEdit = QLineEdit()
        self.filterEdit.setPlaceholderText("Type to filter name.")
        self.label = QLabel("Select option for each person in message:")
        self.button = QPushButton("Mail")
        self.resetButton = QPushButton("Reset")

        self.setupView()

        self.layout.addWidget(self.filterEdit)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.tableview)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.resetButton)
        self.setWindowTitle('ZVI Address Book')
        self.setWindowIcon(QIcon(getResource("mail.ico")))

    def setupView(self):
        self.tableview = QTableView(self)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Email', 'Option'])
        self.tableview.verticalHeader().hide()
        self.tableview.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tableview.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.proxyModel = QSortFilterProxyModel(self)
        self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxyModel.setSourceModel(self.model)
        self.proxyModel.sort(0, Qt.AscendingOrder)
        self.proxyModel.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.tableview.setModel(self.proxyModel)
        self.fillModel(self.model)
        self.tableview.resizeColumnToContents(0)
        self.tableview.resizeColumnToContents(1)
        self.tableview.verticalHeader().setDefaultSectionSize(10)
        self.tableview.setItemDelegateForColumn(2, ComboDelegate())
        self.tableview.horizontalHeader().setStretchLastSection(True)

    def bind(self):
        self.filterEdit.textChanged.connect(self.proxyModel.setFilterRegularExpression)
        self.resetButton.clicked.connect(self.clear)
        self.button.clicked.connect(self.openMail)

    def openMail(self):
        """Open a new mail window for sending"""
        if constants.system == "Windows":
            sendToList, sendCCList = self.getSendLists()
            mail = outApp.CreateItem(0)
            mail.To = sendToList
            mail.CC = sendCCList
            mail.Display(True)

    def getSendLists(self):
        sendToList = ""
        sendCCList = ""
        model = self.tableview.model()
        for row in range(model.rowCount()):
            options = str(model.data(model.index(row, 2)))
            address = str(model.data(model.index(row, 1)))
            if options == "To":
                sendToList += "{0};".format(address)
            elif options == "CC":
                sendCCList += "{0};".format(address)
            elif options == "":
                pass
        return sendToList, sendCCList

    @staticmethod
    def fillModel(model):
        """Fill model with email information if found"""
        if constants.system == "Windows":
            for entry in entries:
                if entry.Type == "EX":
                    user = entry.GetExchangeUser()
                    if user:
                        if len(user.FirstName) > 0 and len(user.LastName) > 0:
                            nameItem = QStandardItem(str(user.Name))
                            emailItem = QStandardItem(str(user.PrimarySmtpAddress))
                            nameItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                            emailItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                            model.appendRow([nameItem, emailItem])

    def clear(self):
        """Clear model data"""
        for i in range(self.model.rowCount()):
            index = self.model.index(i, 2)
            self.model.setData(index, "")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = ZVIMail()
    w.show()
    sys.exit(app.exec())
