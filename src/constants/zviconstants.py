import json
import logging
import os
import platform
from pathlib import Path

from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QGuiApplication

from src.util.zviutil import getResource, walkPath, getDesktopDir


class DisplayStyles:
    def __init__(self):
        self.inactiveStyle = """
            #c, #d{
                background-color: #5a94ad;
                border: 2px solid black;
                border-radius: 20px;
            }
            #t{
                background-color: #5a94ad;
                border: 2px dashed black;
                border-radius: 20px;
            }
            """
        self.activeStyle = """
            #c, #d{
                background-color: #5a94ad;
                border: 2px solid red;
                border-radius: 20px;
            }
            #t{
                background-color: #5a94ad;
                border: 2px dashed red;
                border-radius: 20px;
            }
            """


class ZVIConstants:
    def __init__(self):
        self.DETACHED_PROCESS = 0x00000008
        self.CREATE_NEW_PROCESS_GROUP = 0x00000200
        self.default_palette = QGuiApplication.palette()
        self.system = platform.system()
        self.username = ""
        self.application = os.path.abspath(__file__)
        self.version = "0.0"
        self.debug_mode = True
        self.cmd_visible = True
        self.mainStatusBar = None
        self.styles = DisplayStyles()
        self.isConnected = os.path.exists("Z:\\")
        self.isLoggedIn = False
        self.isFirstStart = True
        self.isInternetConnection = self.checkConnection()
        self.initialFlowPool = QThreadPool.globalInstance()
        self.flowPool = QThreadPool.globalInstance()
        self.finalFlowPool = QThreadPool.globalInstance()
        self.pool = QThreadPool.globalInstance()
        self.fileDialogPath = getDesktopDir(self.system)
        self.jsons = {"Type": {}}
        self.directory = {"WD": "", "Working": "", "Save": ""}
        serverLoc = self.getServerPathFromJson()
        self.path = {"Server": serverLoc,
                     "Local": walkPath(os.path.dirname(__file__), depth=2),
                     "Database": serverLoc + "/database/"}
        if self.isConnected:
            self.initJSON(serverLoc)
        else:
            self.initJSON()
        self.initLogger()

    def initLogger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        fh = logging.FileHandler("zvilog.log")
        fh.setLevel(logging.ERROR)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '==%(asctime)s - %(funcName)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s==')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @staticmethod
    def getServerPathFromJson():
        with open(getResource("paths.json")) as path:
            paths = json.load(path)
            return paths.get("Server")

    def initJSON(self, location=None):
        """reads all json files"""
        with open(getResource("paths.json", location)) as path:
            self.jsons["Paths"] = json.load(path)
        self.updateQuery = self.jsons["Paths"]["Update"]

    @staticmethod
    def checkConnection():
        try:
            import urllib.request
            urllib.request.urlopen('https://www.google.com/', timeout=10)
            return True
        except:
            return False


constants = ZVIConstants()
