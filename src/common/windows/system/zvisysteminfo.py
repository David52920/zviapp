import socket
import platform
import getpass
import logging

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QApplication

from src.constants.zviconstants import constants
from src.common.windows.system.ui.zvisysteminfo_ui import Ui_System_Info


class ZVISystemInfo(QMainWindow, Ui_System_Info):
    """System Information Window setup class"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.getSystemInfo()

    def getSystemInfo(self):
        """Fill computer information based on operating system"""
        OperatingSystem = platform.platform()
        ComputerName = socket.gethostname()
        UserName = getpass.getuser()
        Domain = socket.getfqdn()
        if "." in Domain:
            Domain = socket.getfqdn().split('.', 1)[1]
        logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
        if constants.system == "Windows":
            from scapy.arch.windows import get_windows_if_list
            NetworkType = get_windows_if_list()[1]['name']
            NetworkDescription = get_windows_if_list()[1]['description']
            NetworkMac = get_windows_if_list()[1]['mac']
            NetworkIP = get_windows_if_list()[1]['ips'][1]

        else:
            from scapy.all import get_if_hwaddr, get_if_addr, get_if_list
            NetworkType = "Ethernet" if str(get_if_list()[0]).startswith("e") else "Wi-Fi"
            NetworkDescription = get_if_list()[0]
            NetworkMac = get_if_hwaddr(get_if_list()[0])
            NetworkIP = get_if_addr(get_if_list()[0])
        self.setItems(OperatingSystem, ComputerName, UserName, Domain, NetworkType, NetworkDescription,
                      NetworkMac, NetworkIP)

    def setItems(self, OperatingSystem, ComputerName, UserName, Domain, NetworkType, NetworkDescription,
                 NetworkMac, NetworkIP):
        """Sets table items for system info"""
        self.tableWidget.setItem(0, 0, QTableWidgetItem(ComputerName))
        self.tableWidget.setItem(1, 0, QTableWidgetItem(Domain))
        self.tableWidget.setItem(2, 0, QTableWidgetItem(UserName))
        #self.tableWidget.setItem(3, 0, QTableWidgetItem(constants.directory["WD"]))
        self.tableWidget.setItem(6, 0, QTableWidgetItem(OperatingSystem))
        self.tableWidget.setItem(9, 0, QTableWidgetItem(NetworkType))
        self.tableWidget.setItem(10, 0, QTableWidgetItem(NetworkDescription))
        self.tableWidget.setItem(11, 0, QTableWidgetItem(NetworkMac))
        self.tableWidget.setItem(12, 0, QTableWidgetItem(NetworkIP))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = ZVISystem()
    w.show()
    sys.exit(app.exec())
