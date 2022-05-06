import os
import sys
import time

from PyQt5.QtWidgets import (QDesktopWidget, QApplication, QInputDialog, QFileDialog, QMdiSubWindow,
                             QAction, QSystemTrayIcon, QToolBar, QMenu, QMessageBox, QLineEdit, QWidget, QGridLayout,
                             QToolButton, QCompleter, QSizePolicy, QLabel)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSettings, QPoint, QSize, QTimer
from cryptography.fernet import Fernet

from constants.zvienums import ZVI, WINDOW
from src.common.windows.search.zvisearchapp import ZVISearchApp
from src.common.windows.mdi.zvimain import MainWindow
from src.constants.zviconstants import constants
from src.common.windows.browser.zvibrowser import Browser
from src.common.windows.mdi.zvihome import ZVIHome
from src.common.windows.settings.zvisettings import ZVISettings
from src.common.windows.mail.zvimail import ZVIMail
from src.common.windows.mdi.zvilogin import ZVILogin
from src.common.windows.mdi.zvisignup import ZVISignup
from src.common.windows.system.zvisysteminfo import ZVISystemInfo
from src.common.windows.help.zvihelp import ZVIHelp
from src.common.windows.report.zvireportbug import ZVIReportBug
from src.common.managers.zviemailmanager import EmailManager
from src.common.managers.zvithememanager import ThemeManager
from src.common.managers.zvidatabasemanager import DatabaseManager
from src.common.windows.update.zviupdate import UpdateApp


from src.util.state.zvistate import State
from src.util.zviutil import getResource, strtobool

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class ZVIApp(MainWindow):
    """ZVI App class"""
    saveSettings = QSettings("zvisave.ini", QSettings.IniFormat)
    userProps = QSettings("userProps.ini", QSettings.IniFormat)

    def __init__(self, parent=None):
        super(ZVIApp, self).__init__(parent)
        self.build()
        self.bind()

    def build(self):
        self.menu = QMenu(self)
        self.searchWidget = QWidget()
        self.toolBar = QToolBar("Main")
        self.searchToolBar = QToolBar("Main")
        self.searchAppText = QLineEdit()
        self.searchAppText.setPlaceholderText("Type to search...")
        self.searchAppButton = QToolButton()

        self.emailManager = EmailManager()
        self.themeManager = ThemeManager(self)
        self.databaseManager = DatabaseManager()
        self.setPreviousTheme()
        # self.timedSave = TimedCallBack(self.save, 900000)
        # self.timedUpdate = TimedCallBack(self.checkForUpdate, 3600000)
        self.state = State(self, self.saveSettings)
        self.accountLogin = ZVILogin(self.databaseManager, self.emailManager)
        self.accountSignup = ZVISignup(self.databaseManager, self.emailManager)
        self.zviHelp = ZVIHelp()
        self.zviReportBug = ZVIReportBug(self.emailManager)
        self.homeWindow = ZVIHome(self)
        self.mail = ZVIMail(self)
        self.browser = Browser(self)
        self.system = ZVISystemInfo()
        self.settingsWindow = ZVISettings(self)
        self.searchApp = ZVISearchApp(self)
        self.updateWindow = UpdateApp()
        self.systemTray = QSystemTrayIcon()
        self.flashMessage = False

        layout = QGridLayout(self.searchWidget)
        spacerBegin = QWidget()
        spacerBegin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.systemInfo = self.menu.addAction("System Information")
        self.restoreApp = self.menu.addAction("Restore Previous Session")
        self.showApp = self.menu.addAction("Show")
        self.quitApp = self.menu.addAction("Quit")
        self.systemTray.setContextMenu(self.menu)
        self.systemTray.setToolTip("ZVIApp")
        self.systemTray.setIcon(QIcon(getResource("zvilogo.ico")))

        self.searchWidget.setMaximumHeight(25)
        self.searchAppText.setToolTip("Search items in application.")
        self.searchAppText.setCompleter(QCompleter(["settings", "example program",
                                                    "msa", "mail", "themes", "variables"]))
        self.searchAppText.setFixedWidth(150)
        self.searchAppText.setMinimumHeight(15)
        self.searchAppText.setMinimumHeight(15)
        self.searchAppButton.setIcon(QIcon(getResource("search.ico")))
        layout.addWidget(self.searchAppText, 0, 0)
        layout.addWidget(self.searchAppButton, 0, 1)
        self.searchToolBar.setMovable(False)
        self.searchToolBar.setMaximumHeight(25)
        self.addToolBar(self.searchToolBar)
        self.searchToolBar.addWidget(spacerBegin)
        self.searchToolBar.addWidget(self.searchAppText)
        self.searchToolBar.addWidget(self.searchAppButton)

        self.settingsAction = QAction(QIcon(getResource("settings.ico")), 'Settings, Shift+S', self)
        self.settingsAction.setShortcut('Shift+S')
        self.browserAction = QAction(QIcon(getResource("browser.ico")), 'Browser, Ctrl+Shift+B', self)
        self.browserAction.setShortcut('Ctrl+Shift+B')
        self.mailAction = QAction(QIcon(getResource("mail.ico")), 'Mail Address Book, Ctrl+Shift+M', self)
        self.mailAction.setShortcut('Ctrl+Shift+M')
        self.saveAction = QAction(QIcon(getResource("save.ico")), 'Save Session, F1', self)
        self.saveAction.setShortcut('F1')
        self.restoreAction = QAction(QIcon(getResource("refresh.ico")), 'Restore Session, F2', self)
        self.restoreAction.setShortcut('F2')
        self.logoutAction = QAction(QIcon(getResource("exit.ico")), 'Logout, F10', self)
        self.logoutAction.setShortcut('F10')
        self.screenAction = QAction(QIcon(getResource("screenshot.ico")), 'Screenshot, F12', self)
        self.screenAction.setShortcut('F12')
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)
        self.toolBar.addAction(self.saveAction)
        self.toolBar.addAction(self.restoreAction)
        self.toolBar.addSeparator()
		#private
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.screenAction)
        self.toolBar.addAction(self.browserAction)
        self.toolBar.addAction(self.mailAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.settingsAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.logoutAction)
        self.flashTimer = QTimer()
        self.flashTimer.timeout.connect(self.setFlashMessage)
        self.flashLabel = QLabel("")
        font = QFont()
        font.setBold(True)
        self.flashLabel.setStyleSheet("color: #db3939;")
        self.flashLabel.setFont(font)
        self.statusbar.addPermanentWidget(self.flashLabel)
        self.toggleToolIcons(False)
        screen_rect = QApplication.instance().desktop().screenGeometry()
        self.setMinimumSize(self.minimumSizeHint())
        self.resize(screen_rect.width() - 200, screen_rect.height() - 200)
        self.setWindowIcon(QIcon(QPixmap(getResource("logo.ico"))))

        self.systemTray.show()
        # self.timedSave.start()
        # self.timedUpdate.start()
        self.checkForUpdate()
        self.setupApp()

    def bind(self):
        self.systemInfo.triggered.connect(self.system.showNormal)
        self.showApp.triggered.connect(self.showNormal)
        self.restoreApp.triggered.connect(self.restore)
        self.quitApp.triggered.connect(QApplication.quit)
        self.searchAppButton.clicked.connect(self.findAll)
        # Toolbar items
        self.actionLogOut.triggered.connect(self.logoutSession)
        self.actionSettings.triggered.connect(self.showSettings)
        self.actionMSA.triggered.connect(self.startMSA)
        # Menu Items - view->show
        self.actionshowHW.triggered.connect(self.showHome)
        self.actionCascade.triggered.connect(self.mdiArea.cascadeSubWindows)
        self.actionTile.triggered.connect(self.mdiArea.tileSubWindows)
        self.actionCloseAll.triggered.connect(self.resetSubWindows)
        # misc
        self.actionHelp.triggered.connect(self.zviHelp.showNormal)
        self.actionReport.triggered.connect(self.zviReportBug.showNormal)
        self.logoutAction.triggered.connect(self.logoutSession)
        self.settingsAction.triggered.connect(self.showSettings)
        self.screenAction.triggered.connect(self.screenshot)
        self.browserAction.triggered.connect(self.showBrowser)
        self.mailAction.triggered.connect(self.showMail)
        self.actionUpdate.triggered.connect(self.updateWindow.show)
        self.saveAction.triggered.connect(self.save)
        self.restoreAction.triggered.connect(self.restore)
        self.actionExit.triggered.connect(self.close)

    def findAll(self):
        searchText = self.searchAppText.text()
        self.searchApp.find(searchText)

    def setPreviousTheme(self):
        if not os.path.exists(self.userProps.fileName()):
            self.userProps.setValue("theme/themeList", list(self.themeManager.paletteColorDict.keys()))
            self.userProps.setValue("theme/themePalettes", "")
        else:
            if self.userProps.value("theme/theme"):
                themeName = self.userProps.value("theme/themeName")
                if themeName and "Dark" in themeName:
                    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--blink-settings=forceDarkModeEnabled=true"
                self.themeManager.setTheme(self.userProps.value("theme/theme"))

    def configure(self):
        constants.isLoggedIn = True
        if constants.isFirstStart:
            constants.isFirstStart = False
            self.createHome()
            self.createSettings()
            self.createBrowser()
            self.createMail()
        self.resetSubWindows()
        self.toggleToolIcons(True)
        self.statusbar.showMessage("WD directory: {0}".format(constants.directory["WD"]), 15000)
        os.chdir(constants.fileDialogPath)

    def resetSubWindows(self):
        self.showOnlySubWindow(ZVIHome)

    def toggleToolIcons(self, isToggled):
        self.toolBar.setEnabled(isToggled)
        for act in [self.actionSettings, self.actionView, self.menuProgramsExcel,
                    self.actionHelp, self.actionReport, self.menuShow, self.actionLogOut, self.searchToolBar]:
            act.setEnabled(isToggled)

    def setupApp(self):
        if constants.isConnected:
            self.createSignup()
            self.createLogin()
        else:
            dialog = QInputDialog()
            path, ok = dialog.getText(self, 'Server Error',
                                      """You will now be logged in as a guest.

Enter your WD workspace path:
Example: C:\\Workspace\\WD""")
            if ok:
                if path != "":
                    constants.directory["WD"] = path
                self.configure()
            else:
                sys.exit()
        self.center()
        self.show()

    def updateCredentials(self, credentials):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        password = fernet.encrypt(credentials[1].encode())
        self.userProps.setValue("credentials/rememberMe", credentials[2])
        self.userProps.setValue("credentials/username", credentials[0].lower())
        self.userProps.setValue("credentials/key", key)
        self.userProps.setValue("credentials/password", password)

    def center(self):
        if constants.system == "Windows":
            self.centerToPosition(0)
        else:  # some reason linux systems are offset
            self.centerToPosition(-50)

    def centerToPosition(self, yPoint):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center() - QPoint(0, yPoint))
        self.move(qr.topLeft())

    def save(self):
        if constants.isLoggedIn:
            self.example.guiSave() #unusable removed for company

    def restore(self):
        if constants.isLoggedIn:
            self.example.guiRestore() #unusable removed for company

    def screenshot(self):
        directory = QFileDialog.getSaveFileName(self, caption='Save Screenshot', directory='c:\\',
                                                filter="PNG (*.png)",
                                                options=QFileDialog.DontUseNativeDialog)
        if directory[0] != "":
            QApplication.primaryScreen().grabWindow(self.winId()).save("{0}".format(directory[0]))

    def centerSubwindow(self, subwindow):
        """center subwindow inside mdiarea """
        center = self.mdiArea.viewport().rect().center()
        geo = subwindow.geometry()
        geo.moveCenter(center)
        subwindow.setGeometry(geo)

    def centerSubwindowList(self, subwindowList):
        """center each subwindow inside list """
        for subwindow in subwindowList:
            window = self.getSubWindow(subwindow)
            if window:
                self.centerSubwindow(window)

    def setActiveSubWindow(self, subWindow):
        window = self.getSubWindow(subWindow)
        window.show()
        window.widget().show()
        self.centerSubwindow(window)
        self.mdiArea.setActiveSubWindow(window)

    def showOnlySubWindow(self, subWindow):
        for window in self.mdiArea.subWindowList():
            if isinstance(window.widget(), subWindow):
                window.show()
            else:
                window.hide()

    def showSubWindow(self, subWindow):
        for window in self.mdiArea.subWindowList():
            if isinstance(window.widget(), subWindow):
                window.show()
                window.widget().showNormal()

    def closeSubWindow(self, subWindow):
        for window in self.mdiArea.subWindowList():
            if isinstance(window.widget(), subWindow):
                window.hide()

    def getSubWindow(self, subWindow):
        for window in self.mdiArea.subWindowList():
            if isinstance(window.widget(), subWindow):
                return window

    def addSubWindow(self, window, isFixed=False,
                     flags=Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint):
        subwindow = QMdiSubWindow()
        subwindow.setWidget(window)
        compare = window.minimumSize() - window.minimumSizeHint()
        size = window.minimumSizeHint()if not compare.isValid() else window.minimumSize()
        if isFixed:
            subwindow.setFixedSize(size + QSize(10, 20))
        else:
            subwindow.setMinimumSize(size + QSize(270, 0) if size.width() < 250 else size + QSize(5, 5))
        subwindow.setWindowFlags(flags)
        self.mdiArea.addSubWindow(subwindow)
        self.centerSubwindow(subwindow)
        return subwindow

    def processObj(self, obj):
        if obj["type"] == ZVI.WINDOW:
            if obj["description"] == WINDOW.RESIZE:
                self.resizeSubWindow(obj["value"]["size"], obj["value"]["window"])
            elif obj["description"] == WINDOW.CENTER:
                if obj["value"] == "vs":
                    self.centerSubwindow(self.getSubWindow(type(self.valveSizing)))
            elif obj["description"] == WINDOW.SHOW:
                self.showSubWindow(obj["value"])
            elif obj["description"] == WINDOW.CLOSE:
                self.closeSubWindow(obj["value"])

    def resizeSubWindow(self, size, subWindow):
        window = self.getSubWindow(subWindow)
        window.resize(QSize(max(window.width(), (size + QSize(100, 0)).width()),
                            max(window.height(), self.height() - 75)))

    def checkForUpdate(self):
        if constants.checkConnection():
            if self.updateWindow.checkVersion():
                if self.flashTimer.isActive():
                    self.flashTimer.quit()
                    self.flashLabel.clear()
            else:
                if not self.flashTimer.isActive():
                    self.flashTimer.start(1500)

    def setFlashMessage(self):
        if not self.flashMessage:
            self.flashLabel.clear()
            self.flashMessage = True
        else:
            self.flashLabel.setText("New version available!")
            self.flashMessage = False

    def loginSession(self, username, location):
        constants.directory["WD"] = location
        self.searchWidget.setEnabled(True)
        self.actionLogOut.setEnabled(True)
        self.setWindowTitle("ZVIApp: {0}".format(username))
        self.configure()
        constants.username = username
        self.zviReportBug.setUsername(username)

    def logoutSession(self):
        reply = QMessageBox.question(self, 'Session', "Are you sure to leave session?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if constants.isLoggedIn:
                constants.isLoggedIn = False
                self.save()
                self.setWindowTitle("ZVI")
                self.toggleToolIcons(False)
                self.showOnlySubWindow(ZVILogin)
                self.actionLogOut.setDisabled(True)

    def fillLoginOnStartup(self):
        if os.path.exists(self.userProps.fileName()):
            username = self.userProps.value("credentials/username")
            remember = strtobool(self.userProps.value("credentials/rememberMe"))
            key = self.userProps.value("credentials/key")
            if key:
                fernet = Fernet(key)
                password = fernet.decrypt(self.userProps.value("credentials/password")).decode()
                if remember:
                    self.accountLogin.rememberMe.setChecked(True)
                    self.accountLogin.passwordEdit.setText(password)
            if username:
                self.accountLogin.usernameEdit.setText(username)

    def createLogin(self):
        """create login window """
        self.fillLoginOnStartup()
        self.accountLogin.sendCredentials.connect(self.updateCredentials)
        self.accountLogin.performLogin.connect(self.loginSession)
        self.accountLogin.showSignup.connect(self.showSignup)
        self.addSubWindow(self.accountLogin, isFixed=True, flags=Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.SubWindow)

    def createSignup(self):
        """create signup """
        subwindow = self.addSubWindow(self.accountSignup, isFixed=True, flags=Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint)
        self.accountSignup.hideWindow.connect(subwindow.hide)
        subwindow.hide()


    def createSettings(self):
        """create settings window """
        flags = Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        self.addSubWindow(self.settingsWindow, flags=flags)

    def createBrowser(self):
        """create Browser window """
        flags = Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        self.addSubWindow(self.browser, flags=flags)

    def createMail(self):
        """create mail window """
        self.addSubWindow(self.mail)

    def createHome(self):
        """create home window """
        self.addSubWindow(self.homeWindow, isFixed=True, flags=Qt.CustomizeWindowHint | Qt.Tool)

    def startMSA(self):
        """Open MSA excel"""
        if os.path.exists(os.path.join(constants.jsons["Paths"]['Template'], constants.jsons["Paths"]['MSA'])):
            if constants.system == "Windows":
                os.system('start excel.exe "{0}/{1}"'.format(constants.jsons["Paths"]['Template'],
                                                             constants.jsons["Paths"]['MSA']))
            else:
                os.system('libreoffice "{0}/{1}"'.format(constants.jsons["Paths"]['Template'],
                                                         constants.jsons["Paths"]['MSA']))
        else:
            self.statusbar.showMessage("Unable to open MSA. Directory or file not found.", 20000)

    def startModuleProgram(self):
        """Open module program """
        if os.path.exists(constants.jsons["Paths"]['Example']):
            os.startfile(r'{0}'.format(constants.jsons["Paths"]['Example']))
        else:
            self.statusbar.showMessage("Unable to open module program. Not connected to server.", 20000)

    def showSignup(self):
        """Show signup window"""
        self.setActiveSubWindow(ZVISignup)

    def showHome(self):
        """Show home window"""
        self.setActiveSubWindow(ZVIHome)


    def showSettings(self):
        """Show settings window"""
        self.setActiveSubWindow(ZVISettings)

    def showBrowser(self):
        """Show browser window"""
        self.setActiveSubWindow(Browser)

    def showMail(self):
        """Show mail window"""
        self.setActiveSubWindow(ZVIMail)


    def resizeEvent(self, event):
        self.centerSubwindowList([ZVILogin, ZVIHome, ZVISignup])
        super(ZVIApp, self).resizeEvent(event)

    def changeEvent(self, event):
        if self.windowState() == Qt.WindowNoState:
            self.centerSubwindowList([ZVILogin, ZVIHome, ZVISignup])
        super(ZVIApp, self).changeEvent(event)

    def closeEvent(self, event):
        """Close event for main window"""
        reply = QMessageBox.question(self, 'Quit', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if constants.isLoggedIn:
                reply = QMessageBox.question(self, 'Save', "Save current session?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.save()
            event.accept()
            QApplication.instance().closeAllWindows()
        else:
            event.ignore()
