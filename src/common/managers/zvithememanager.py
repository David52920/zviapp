import re

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from src.constants.zviconstants import constants
import os


class ThemeManager:
    paletteColorDict = {"Default": QColor(42, 130, 218),
                        "Dark Blue": QColor(42, 130, 218),
                        "Dark Orange": QColor(255, 174, 0),
                        "Dark Purple": QColor(215, 42, 218),
                        "Dark Green": QColor(4, 117, 53),
                        "Dark Red": QColor(196, 6, 6),
                        "Dark Yellow": QColor(255, 255, 0),
                        "Dark Pink": QColor(255, 192, 203)
                        }
    colorDict = {
        "text": {
            "Dark": Qt.white,
            "Light": Qt.black
        },
        "base": {
            "Dark": QColor(48, 48, 48),
            "Light": QColor(255, 255, 255)
        },
        "main": {
            "Dark": QColor(53, 53, 53),
            "Light": QColor(240, 240, 240)
        }
    }

    def __init__(self, parent=None):
        self.parent = parent
        self.app = QApplication.instance()
        if self.app is None:
            raise RuntimeError("No Qt Application found.")
        if not os.path.exists(self.parent.userProps.fileName()):
            self.themePalettes = {}
        else:
            self.themePalettes = self.parent.userProps.value("theme/themePalettes")
            themeDict = self.parent.userProps.value("theme/themeDict")
            self.paletteColorDict = themeDict if themeDict else self.paletteColorDict

    def setTheme(self, palette):
        self.app.setPalette(palette)
        self.parent.userProps.setValue("theme/theme", palette)

    def createPalette(self, color):
        """Toggle the stylesheet to use the desired path in the Qt resource"""
        try:
            palette = QPalette()
            pColor = self.paletteColorDict.get(color)
            if pColor is not None:
                palette.setColor(QPalette.Link, pColor)
                palette.setColor(QPalette.Highlight, pColor)
            else:
                return self.themePalettes[color]
            color = "Light" if color == "Default" else color
            style = re.search(r'(Dark|Light)', color).group(1)
            palette.setColor(QPalette.Window, self.colorDict["main"][style])
            palette.setColor(QPalette.Base, self.colorDict["base"][style])
            palette.setColor(QPalette.AlternateBase, self.colorDict["main"][style])
            palette.setColor(QPalette.ToolTipBase, self.colorDict["main"][style])
            palette.setColor(QPalette.ToolTipText, self.colorDict["text"][style])
            palette.setColor(QPalette.Button, self.colorDict["main"][style])
            palette.setColor(QPalette.ButtonText, self.colorDict["text"][style])
            palette.setColor(QPalette.WindowText, self.colorDict["text"][style])
            palette.setColor(QPalette.Text, self.colorDict["text"][style])
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.HighlightedText, Qt.black)

            return palette
        except:
            constants.logger.exception('Exception occurred:')

    @staticmethod
    def getDefaultPalette():
        return constants.default_palette

    def createCustomPalette(self, name, color, style=""):
        try:
            palette = QPalette()
            if style == "Dark":
                palette.setColor(QPalette.Window, self.colorDict["main"][style])
                palette.setColor(QPalette.Base, self.colorDict["base"][style])
                palette.setColor(QPalette.AlternateBase, self.colorDict["main"][style])
                palette.setColor(QPalette.ToolTipBase, self.colorDict["main"][style])
                palette.setColor(QPalette.ToolTipText, self.colorDict["text"][style])
                palette.setColor(QPalette.Button, self.colorDict["main"][style])
                palette.setColor(QPalette.ButtonText, self.colorDict["text"][style])
                palette.setColor(QPalette.WindowText, self.colorDict["text"][style])
                palette.setColor(QPalette.Text, self.colorDict["text"][style])
                palette.setColor(QPalette.BrightText, Qt.red)
                palette.setColor(QPalette.HighlightedText, Qt.black)
            elif style == "Light":
                palette = constants.default_palette
            palette.setColor(QPalette.Link, color)
            palette.setColor(QPalette.Highlight, color)
            if isinstance(self.themePalettes, dict):
                self.themePalettes[name] = palette
            else:
                self.themePalettes = {name: palette}
            self.parent.userProps.setValue("theme/themePalettes", self.themePalettes)
            return palette
        except:
            constants.logger.exception('Exception occurred:')
