from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEnginePage

from PyQt5.QtWidgets import (QMainWindow, QApplication, QTabWidget, QToolBar, QAction, QLabel, QLineEdit, QFileDialog,
                             QToolButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QUrl, Qt

from src.util.zviutil import getResource


class Browser(QMainWindow):
    """ZVI browser"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.build()

    def build(self):
        self.setObjectName("Internet_Browser")
        self.tabs = QTabWidget()
        self.addSheetButton = QToolButton()
        self.addSheetButton.setText("+")
        self.addSheetButton.clicked.connect(lambda _: self.addNewTab())
        self.tabs.setCornerWidget(self.addSheetButton, Qt.TopLeftCorner)

        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tabOpenDoubleClick)
        self.tabs.currentChanged.connect(self.updateCurrentTabInfo)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeCurrentTab)
        self.setCentralWidget(self.tabs)

        navBar = QToolBar("Navigation")
        navBar.setIconSize(QSize(16, 16))
        self.addToolBar(navBar)

        back_btn = QAction(QIcon(getResource('browser_arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navBar.addAction(back_btn)

        next_btn = QAction(QIcon(getResource('browser_arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navBar.addAction(next_btn)

        reload_btn = QAction(QIcon(getResource('browser_arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navBar.addAction(reload_btn)

        home_btn = QAction(QIcon(getResource('browser_home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigateHome)
        navBar.addAction(home_btn)

        navBar.addSeparator()

        self.httpsIcon = QLabel()  # Yes, really!
        self.httpsIcon.setPixmap(getResource('browser_lock-nossl.png'))
        navBar.addWidget(self.httpsIcon)

        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.navigateToURL)
        navBar.addWidget(self.urlBar)

        stop_btn = QAction(QIcon(getResource('browser_cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navBar.addAction(stop_btn)

        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon(getResource('browser_ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.addNewTab())
        file_menu.addAction(new_tab_action)

        self.addNewTab(QUrl('https://app.asana.com/-/login'), 'Homepage')

        self.setWindowTitle("Browser")
        self.setWindowIcon(QIcon(getResource('browser.ico')))

    def addNewTab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('http://www.google.com')

        browser = QtWebEngineWidgets.QWebEngineView()
        browser.setUrl(qurl)
        browser
        browser.pageAction(QWebEnginePage.WebAction.InspectElement).setVisible(False)
        browser.pageAction(QWebEnginePage.WebAction.SavePage).setVisible(False)
        browser.pageAction(QWebEnginePage.WebAction.ViewSource).setVisible(False)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.updateURLBar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def tabOpenDoubleClick(self, i):
        if i == -1:  # No tab under the click
            self.addNewTab()

    def updateCurrentTabInfo(self, i):
        qurl = self.tabs.currentWidget().url()
        self.updateURLBar(qurl, self.tabs.currentWidget())
        self.updateTitle(self.tabs.currentWidget())

    def closeCurrentTab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def updateTitle(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Browser" % title)

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")
        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlBar.setText(filename)

    def navigateHome(self):
        self.tabs.currentWidget().setUrl(QUrl("https://app.asana.com/-/login"))

    def navigateToURL(self):  # Does not receive the Url
        q = QUrl(self.urlBar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def updateURLBar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == 'https':
            self.httpsIcon.setPixmap(getResource('browser_lock-ssl.png'))
        else:
            self.httpsIcon.setPixmap(getResource('browser_lock-nossl.png'))

        self.urlBar.setText(q.toString())
        self.urlBar.setCursorPosition(0)


def main():
    import sys
    app = QApplication(sys.argv)
    gaswindow = Browser()
    gaswindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
