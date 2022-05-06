import os
from pathlib import Path
import platform

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QMainWindow, QApplication, QLabel, QLineEdit, QTextEdit, QPushButton

from src.util.zviutil import getResource
from src.constants.zviconstants import constants


class ZVIReportBug(QMainWindow):
    def __init__(self, emailManager, parent=None):
        super().__init__(parent)
        self.emailManager = emailManager
        self.build()

    def build(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        uLabel = QLabel("Username:")
        uLabel.setMaximumWidth(70)
        layout.addWidget(uLabel, 0, 0, 1, 1)
        self.username = QLineEdit()
        self.username.setMaximumWidth(150)
        self.username.setDisabled(True)
        layout.addWidget(self.username, 0, 1, 1, 2)
        sLabel = QLabel("System:")
        sLabel.setMaximumWidth(70)
        layout.addWidget(sLabel, 1, 0, 1, 1)
        system = QLineEdit()
        system.setMaximumWidth(150)
        self.systemName = platform.system() + " " + platform.version()
        system.setText(self.systemName)
        system.setDisabled(True)
        layout.addWidget(system, 1, 1, 1, 2)
        layout.addWidget(QLabel("Description:"), 2, 0, 1, 1)
        self.bugDescription = QTextEdit()
        layout.addWidget(self.bugDescription, 3, 0, 1, 3)
        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.submitBug)
        layout.addWidget(self.submit, 4, 0, 1, 3)
        self.setCentralWidget(widget)
        self.setWindowIcon(QIcon(getResource("report-bug.ico")))
        self.setWindowTitle("Report Bug")
        self.setObjectName("Report A Bug")
        self.setMinimumSize(300, 200)
        self.resize(300, 200)

    def setUsername(self, username):
        self.username.setText(username)

    def submitBug(self):
        self.emailManager.sendEmail("drees@zahroofvalves.com",
                                    "ZVIApp Report Bug - User: {0}, {1}".format(self.username.text(), self.systemName),
                                    self.bugDescription.toPlainText(),
                                    os.path.join(constants.path["Local"], Path(constants.logger.handlers[0].baseFilename).name))
        self.bugDescription.clear()
        self.close()

    def closeEvent(self, event):
        self.bugDescription.clear()
        event.accept()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = ZVIReportBug(None)
    w.show()
    sys.exit(app.exec_())