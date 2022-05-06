from PyQt5.QtWidgets import QUndoCommand
from PyQt5.QtCore import Qt

class CommandEdit(QUndoCommand):
    def __init__(self, window, item, oldText, newText):
        super(CommandEdit, self).__init__()
        self.item = item
        self.window = window
        self.oldText = oldText
        self.newText = newText

    def redo(self):
        self.item.model().handleItemChanged.disconnect(self.window.handleItemChangedSlot)
        self.item.model().setData(self.item, self.newText, Qt.EditRole)
        self.item.model().handleItemChanged.connect(self.window.handleItemChangedSlot)

    def undo(self):
        self.item.model().handleItemChanged.disconnect(self.window.handleItemChangedSlot)
        self.item.model().setData(self.item, self.oldText, Qt.EditRole)
        self.item.model().handleItemChanged.connect(self.window.handleItemChangedSlot)
