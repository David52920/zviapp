from PyQt5.QtWidgets import QLineEdit, QStyle, QToolButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QIcon


class ButtonLineEdit(QLineEdit):
    buttonClicked = pyqtSignal(bool)

    def __init__(self, icon_file, parent=None):
        super(ButtonLineEdit, self).__init__(parent)

        self.button = QToolButton(self)
        self.button.setCheckable(True)
        self.button.setIcon(QIcon(icon_file))
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.clicked.connect(self.buttonClicked.emit)

        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth*2 + 2),
                            max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth*2 + 2))

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),
                         int((self.rect().bottom() - buttonSize.height() + 1)/2))
        super(ButtonLineEdit, self).resizeEvent(event)


class Edit(QLineEdit):
    def __init__(self, objectName="", isDigitEdit=True, isInt=False, isDisabled=False):
        super().__init__()
        self.setObjectName(objectName)
        self.setMinimumWidth(80)
        self.setAlignment(Qt.AlignHCenter)
        if isDigitEdit:
            if not isInt:
                self.setValidator(QDoubleValidator(0, 20000, 10))
            else:
                self.setValidator(QIntValidator(0, 20000))
        else:
            self.setPlaceholderText("BLANK")

        if isDisabled:
            self.setEnabled(False)


class ThrowEdit(QLineEdit):
    def __init__(self, objName, originalText, parent=None):
        super().__init__()
        self.parent = parent
        self.objName = objName
        self.firstText = originalText
        self.originalText = originalText
        self.setObjectName(self.objName)
        self.setText(self.originalText)
        self.setValidator(QIntValidator(1, 6))
        self.setMaximumWidth(12)
        self.setAlignment(Qt.AlignHCenter)

    def setOriginalText(self, value):
        self.originalText = value

    def getOriginalText(self):
        return self.originalText
