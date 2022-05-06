from PyQt5.QtWidgets import QComboBox

from src.constants.zviconstants import constants


class ComboBox(QComboBox):
    def __init__(self, objectName):
        super().__init__()
        self.setObjectName(objectName)
        self.setMinimumWidth(80)


class TypeCombo(QComboBox):
    def __init__(self, objectName):
        super().__init__()
        self.setSizeAdjustPolicy(self.AdjustToMinimumContentsLengthWithIcon)
        self.addItems(["", "M1", "M2"])
        self.setObjectName(objectName)
        self.setMinimumWidth(80)


class MaterialCombo(QComboBox):
    def __init__(self, objectName):
        super().__init__()
        self.setSizeAdjustPolicy(self.AdjustToMinimumContentsLengthWithIcon)
        self.addItems([""] + constants.jsons["Reeds"]["MaterialList"])
        self.setObjectName(objectName)
        self.setMinimumWidth(80)


class LiftCombo(QComboBox):
    def __init__(self, objectName):
        super().__init__()
        self.setSizeAdjustPolicy(self.AdjustToMinimumContentsLengthWithIcon)
        self.addItems([""] + constants.jsons["Module"]['LiftList'])
        self.setObjectName(objectName)
        self.setMinimumWidth(80)


class ReedCombo(QComboBox):
    def __init__(self, objectName):
        super().__init__()
        self.setSizeAdjustPolicy(self.AdjustToMinimumContentsLengthWithIcon)
        self.addItems([""] + constants.jsons["Reeds"]["ReedList"])
        self.setObjectName(objectName)
        self.setMinimumWidth(80)


class ChannelCombo(QComboBox):
    def __init__(self, objectName):
        super().__init__()
        self.addItems(["", "4", "6"])
        self.setObjectName(objectName)
        self.setMinimumWidth(80)
