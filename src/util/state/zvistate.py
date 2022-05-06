import inspect

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QByteArray, QIODevice, QDataStream, QItemSelectionModel
from PyQt5.QtGui import QStandardItem

from src.util.zviutil import strtobool


class State:
    def __init__(self, obj, settings):
        self.obj = obj
        self.settings = settings

    @staticmethod
    def readDefaults(widget):
        if widget.objectName() == "listwidget_1":
            widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            for i in range(10):
                widget.addItem(QtWidgets.QListWidgetItem(str(i)))
        elif widget.objectName() == "listwidget_2":
            widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            for i in "abcdefghijklmnopqrstuvwxyz":
                widget.addItem(QtWidgets.QListWidgetItem(i))
        elif widget.objectName() == "tablewidget":
            widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            widget.setRowCount(10)
            widget.setColumnCount(10)
            for row in range(widget.rowCount()):
                for column in range(widget.columnCount()):
                    widgetItem = QtWidgets.QTableWidgetItem("{}-{}".format(row, column))
                    widget.setItem(row, column, widgetItem)

    def dataToChild(self, info, item):
        self.tupleToItem(info["data"], item)
        for val in info["childrens"]:
            child = QtWidgets.QTreeWidgetItem()
            item.addChild(child)
            self.dataToChild(val, child)

    @staticmethod
    def tupleToItem(t, item):
        ba, isSelected = t
        ds = QtCore.QDataStream(ba)
        ds >> item
        item.setSelected(isSelected)

    def dataFromChild(self, item):
        l = []
        for i in range(item.childCount()):
            child = item.child(i)
            l.append(self.dataFromChild(child))
        self.settings.setValue("treeView_items", self.itemToTuple(item))
        return {"childrens": l, "data": self.itemToTuple(item)}

    @staticmethod
    def itemToTuple(item):
        ba = QByteArray()
        ds = QDataStream(ba, QIODevice.WriteOnly)
        ds << item
        return ba, item.isSelected()

    def save(self, obj=None):
        if not obj:
            obj = self.obj
        for name, widget in inspect.getmembers(obj):
            if isinstance(widget, QtWidgets.QTableView):
                name = widget.objectName()
                model = widget.model()
                self.settings.setValue("{}/editTriggers_tableview".format(name), widget.editTriggers())
                self.settings.setValue("{}/selectionMode_tableview".format(name), widget.selectionMode())
                self.settings.setValue("{}/selectionBehavior_tableview".format(name), widget.selectionBehavior())
                items = QtCore.QByteArray()
                stream = QtCore.QDataStream(items, QtCore.QIODevice.WriteOnly)

                rowCount = model.rowCount()
                columnCount = model.columnCount()
                stream.writeInt(rowCount)
                stream.writeInt(columnCount)
                for rowItem in range(rowCount):
                    for columnItem in range(columnCount):
                        item = model.index(rowItem, columnItem).data()
                        if item is not None:
                            stream.writeQString(item)
                        else:
                            pass
                self.settings.setValue("{}/items_tableview".format(name), items)
                selectedItems = QtCore.QByteArray()
                stream = QtCore.QDataStream(selectedItems, QtCore.QIODevice.WriteOnly)
                for item in widget.selectionModel().selectedRows():
                    stream.writeInt(item.row())
                self.settings.setValue("{}/selectedItems_tableview".format(name), selectedItems)
            if isinstance(widget, QtWidgets.QListView):
                name = widget.objectName()
                model = widget.model()
                self.settings.setValue("{}/editTriggers_listview".format(name), widget.editTriggers())
                self.settings.setValue("{}/selectionMode_listview".format(name), widget.selectionMode())
                self.settings.setValue("{}/selectionBehavior_listview".format(name), widget.selectionBehavior())
                items = QtCore.QByteArray()
                stream = QtCore.QDataStream(items, QtCore.QIODevice.WriteOnly)
                for i in range(model.rowCount()):
                    it = model.index(i, 0)
                    stream.writeInt(it.row())
                    stream.writeQString(it.data())
                self.settings.setValue("{}/items_listview".format(name), items)
                selectedItems = []
                for index in widget.selectionModel().selectedRows():
                    selectedItems.append(index.row())
                self.settings.setValue("{}/selectedItems_listview".format(name), selectedItems)
            if isinstance(widget, QtWidgets.QAbstractItemView):
                name = widget.objectName()
                self.settings.setValue("{}/selectionMode".format(name), widget.selectionMode())
            if isinstance(widget, QtWidgets.QSpinBox):
                name = widget.objectName()
                self.settings.setValue("{}/spinbox".format(name), widget.value())
            if isinstance(widget, QtWidgets.QDateTimeEdit):
                name = widget.objectName()
                self.settings.setValue("{}/calender".format(name), widget.date().toString("MMMM d, yyyy"))
            if isinstance(widget, QtWidgets.QLineEdit):
                name = widget.objectName()
                self.settings.setValue("{}/lineedit".format(name), widget.text())
            if isinstance(widget, QtWidgets.QComboBox):
                name = widget.objectName()
                self.settings.setValue("{}/combobox".format(name), widget.itemText(widget.currentIndex()))
            if isinstance(widget, QtWidgets.QCheckBox):
                name = widget.objectName()
                self.settings.setValue("{}/checkbox".format(name), widget.isChecked())
            if isinstance(widget, QtWidgets.QRadioButton):
                name = widget.objectName()
                print(name)
                self.settings.setValue("{}/radio".format(name), widget.isChecked())
            if isinstance(widget, QtWidgets.QListWidget):
                name = widget.objectName()
                items = QtCore.QByteArray()
                stream = QtCore.QDataStream(items, QtCore.QIODevice.WriteOnly)
                for item in range(widget.count()):
                    stream << widget.item(item)
                self.settings.setValue("{}/items_listWidget".format(name), items)
                selectedItems = QtCore.QByteArray()
                stream = QtCore.QDataStream(selectedItems, QtCore.QIODevice.WriteOnly)
                for selectedWidgetItem in widget.selectedItems():
                    stream.writeInt(widget.row(selectedWidgetItem))

                self.settings.setValue("{}/selectedItems_listWidget".format(name), selectedItems)

    def restore(self, obj=None):
        if not obj:
            obj = self.obj
        for name, widget in inspect.getmembers(obj):
            if isinstance(widget, QtWidgets.QTableView):
                name = widget.objectName()
                model = widget.model()
                selectionModel = widget.selectionModel()
                items = self.settings.value("{}/items_tableview".format(name))
                if items is None:
                    self.readDefaults(widget)
                else:
                    stream = QtCore.QDataStream(items, QtCore.QIODevice.ReadOnly)
                    rowCount = stream.readInt()
                    columnCount = stream.readInt()
                    for row in range(rowCount):
                        for column in range(columnCount):
                            cellText = stream.readQString()
                            if cellText:
                                index = model.index(row, column)
                                model.setData(index, cellText)

                selectedItems = self.settings.value("{}/selectedItems_tableview".format(name))
                stream = QtCore.QDataStream(
                    selectedItems, QtCore.QIODevice.ReadOnly
                )
                while not stream.atEnd():
                    selectionRow = stream.readInt()
                    index = widget.model().index(selectionRow, 0)
                    index1 = widget.model().index(selectionRow, model.columnCount() - 1)
                    itemSelection = QtCore.QItemSelection(index, index1)

                    if itemSelection is not None:
                        selectionModel.select(itemSelection,
                                              QtCore.QItemSelectionModel.Rows | QtCore.QItemSelectionModel.Select)
            if isinstance(widget, QtWidgets.QListView):
                name = widget.objectName()
                model = widget.model()
                if self.settings.contains("{0}/items_listview".format(name)):
                    editTriggers = self.settings.value(
                        "{}/editTriggers_listview".format(name), type=QtWidgets.QAbstractItemView.EditTriggers
                    )
                    selectionMode = self.settings.value(
                        "{}/selectionMode_listview".format(name), type=QtWidgets.QAbstractItemView.SelectionMode
                    )
                    selectionBehavior = self.settings.value(
                        "{}/selectionBehavior_listview".format(name),
                        type=QtWidgets.QAbstractItemView.SelectionBehavior
                    )
                    widget.setEditTriggers(editTriggers)
                    widget.setSelectionMode(selectionMode)
                    widget.setSelectionBehavior(selectionBehavior)
                    items = self.settings.value("{0}/items_listview".format(name))
                    stream = QtCore.QDataStream(items, QtCore.QIODevice.ReadOnly)
                    model.removeRows(0, model.rowCount())
                    while not stream.atEnd():
                        rowData = stream.readQString()
                        item = QStandardItem(str(rowData))
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                        try:
                            model.sourceModel().appendRow(item)
                        except AttributeError as e:
                            pass
                    selectedItems = self.settings.value("{}/selectedItems_listview".format(name))
                    if selectedItems is not None:
                        for row in selectedItems:
                            index = model.index(row, 0)
                            widget.selectionModel().select(
                                index, QItemSelectionModel.Select
                            )
            if isinstance(widget, QtWidgets.QAbstractItemView):
                name = widget.objectName()
                selectionMode = self.settings.value(
                    "{}/selectionMode".format(name), type=QtWidgets.QAbstractItemView.SelectionMode
                )
                widget.setSelectionMode(selectionMode)
            if isinstance(widget, QtWidgets.QSpinBox):
                name = widget.objectName()
                widget.setValue(int(self.settings.value("{}/spinbox".format(name))))
            if isinstance(widget, QtWidgets.QComboBox):
                name = widget.objectName()
                widget.setCurrentIndex(widget.findText(self.settings.value("{}/combobox".format(name))))
            if isinstance(widget, QtWidgets.QCheckBox):
                name = widget.objectName()
                widget.setChecked(strtobool(self.settings.value("{}/checkbox".format(name))))
            if isinstance(widget, QtWidgets.QRadioButton):
                name = widget.objectName()
                widget.setChecked(strtobool(self.settings.value("{}/radio".format(name))))
            if isinstance(widget, QtWidgets.QDateTimeEdit):
                name = widget.objectName()
                date = QtCore.QDate().fromString(self.settings.value("{}/calender".format(name)), "MMMM d, yyyy")
                widget.setDate(date)
            if isinstance(widget, QtWidgets.QLineEdit):
                name = widget.objectName()
                widget.setText(self.settings.value("{}/lineedit".format(name), widget.text()))
            if isinstance(widget, QtWidgets.QListWidget):
                name = widget.objectName()
                items = self.settings.value("{}/items_listWidget".format(name))
                selectedItems = self.settings.value("{}/selectedItems_listWidget".format(name))
                if items is None:
                    self.readDefaults(widget)
                else:
                    stream = QDataStream(items, QIODevice.ReadOnly)
                    while not stream.atEnd():
                        widgetItem = QtWidgets.QListWidgetItem()
                        stream >> widgetItem
                        if widget.count() == 0:
                            widget.addItem(widgetItem)
                    stream = QDataStream(
                        selectedItems, QIODevice.ReadOnly
                    )
                    while not stream.atEnd():
                        row = stream.readInt()
                        widgetItem = widget.item(row)
                        if widgetItem is not None:
                            widgetItem.setSelected(True)
            if isinstance(widget, QtWidgets.QTreeWidget):
                name = widget.objectName()
                widget.clear()
                items = self.settings.value("{}/items_treeWidget".format(name))
                if items is None:
                    self.readDefaults(widget)
                else:
                    self.dataToChild(items, widget.invisibleRootItem())
