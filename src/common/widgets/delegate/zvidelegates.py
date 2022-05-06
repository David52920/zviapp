from PyQt5.QtWidgets import QStyledItemDelegate, QItemDelegate, QComboBox, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from src.common.widgets.spinbox.zvispinboxes import DoubleSpinBox


class InitialDelegate(QStyledItemDelegate):
    """Changes number of decimal places in gas analysis self.chosen table"""

    def __init__(self, decimals, parent=None):
        super().__init__(parent)
        self.nDecimals = decimals

    def createEditor(self, parent, option, index):
        if index.column() == 2:
            editor = DoubleSpinBox(parent)
            return editor

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.column() == 1:
            option.displayAlignment = Qt.AlignCenter
            option.text = str(round(float(index.model().data(index, Qt.DisplayRole)),
                                    self.nDecimals))
        if index.column() == 2:
            option.displayAlignment = Qt.AlignCenter
            indexData = index.model().data(index, Qt.DisplayRole)
            if indexData is not None:
                option.text = str(format(indexData, '.10g'))


class ComboDelegate(QItemDelegate):
    """Custom delegate for combobox"""
    def __init__(self,parent=None):
        super().__init__(parent)
        self.items = ['','To', 'CC']

    def createEditor(self, widget, option, index):
        editor = QComboBox(widget)
        editor.addItems(self.items)
        return editor

    def setEditorData(self, editor, index):
        if index.column() == 2:
            editor.blockSignals(True)
            text = index.model().data(index, Qt.EditRole)
            try:
                i = self.items.index(text)
            except ValueError:
                i = 0
            editor.setCurrentIndex(i)
            editor.blockSignals(False)
        else:
            QItemDelegate.setModelData(editor,index)

    def setModelData(self, editor, model, index):
        if index.column() == 2:
            model.setData(index, editor.currentText())
        else:
            QItemDelegate.setModelData(editor,model,index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class FloatDelegate(QItemDelegate):
    """Validator for seat thickness table- changes number of decimal shown"""

    def __init__(self, _from, _to, _n_decimals, parent=None):
        QItemDelegate.__init__(self, parent=parent)
        self._from = _from
        self._to = _to
        self._n_decimals = _n_decimals

    def createEditor(self, parent, option, index):
        lineEdit = QLineEdit(parent)
        if index.column() == 1:
            lineEdit.setDisabled(True)
        _n_decimals = 6
        validator = QDoubleValidator(self._from, self._to, self._n_decimals, lineEdit)
        lineEdit.setValidator(validator)
        return lineEdit


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter