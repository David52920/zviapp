from PyQt5.QtWidgets import QButtonGroup

class ButtonGroup(QButtonGroup):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()
        
    def toggleButton(self, id):
        for button in self.buttons():
            if button.objectName() == id:
                button.setChecked(True)
