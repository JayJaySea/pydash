import os
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QTimer, QSize
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QGridLayout,
    QMainWindow,
    QWidget,
    QStackedWidget,
    QFrame
)

from datetime import datetime
from pydash.data import DATA_DIR
from pydash.controller import System, AwesomeWM
from pydash.widgets.button import LabelButton, ShutdownButton, RebootButton, RefreshButton, IconButton

class Controls(QFrame):
    def __init__(self):
        super().__init__()
        self.system = System()
        self.system.connection_status.connect(self.updateConnectionStatus)
        self.controller = AwesomeWM()
        self.setMaximumHeight(30)
        
        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.network = NetworkButton()
        self.network.clicked.connect(self.launchNetworkManager)
        layout.addWidget(self.network)

        refresh = RefreshButton()
        refresh.clicked.connect(self.refreshWM)
        layout.addWidget(refresh)

        reboot = RebootButton()
        reboot.clicked.connect(self.reboot)
        layout.addWidget(reboot)

        shutdown = ShutdownButton()
        shutdown.clicked.connect(self.shutdown)
        layout.addWidget(shutdown)
        
        self.setLayout(layout)

    def launchNetworkManager(self):
        self.network.disconnected()

    def shutdown(self):
        self.system.shutdown()

    def reboot(self):
        self.system.reboot()

    def refreshWM(self):
        self.controller.refresh()

    def updateConnectionStatus(self, connection):
        if connection["status"] == "wired":
            self.network.setWired()
        elif connection["status"] == "wifi":
            if connection["strength"] > 66:
                self.network.setWifiHigh()
            elif connection["strength"] > 33:
                self.network.setWifiMedium()
            else:
                self.network.setWifiLow()
        else:
            self.network.setDisconnected()

class NetworkButton(IconButton):
    def __init__(self, size="medium", parent=None, id=None):
        super().__init__("disconnected", "red", size=size, parent=parent, id=id)
        self.icons = {
            "disconnected": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "disconnected.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "disconnected-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "disconnected-active.png"))
            },
            "wired": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "wired.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "wired-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "wired-active.png"))
            },
            "wifi_low": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "wifi_low.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "wifi_low-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "wifi_low-active.png")),
            },
            "wifi_medium": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "wifi_medium.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "wifi_medium-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "wifi_medium-active.png"))
            },
            "wifi_high": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "wifi_high.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "wifi_high-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "wifi_high-active.png"))
            }
        }
        self.indicator.setIconSize(QSize(20, 20))
        
    def setDisconnected(self):
        self.icon_default = self.icons["disconnected"]["default"]
        self.icon_hover =   self.icons["disconnected"]["hover"]
        self.icon_active =  self.icons["disconnected"]["active"]
        self.setColor("red")
        self.updateIcon()

    def setWired(self):
        self.icon_default = self.icons["wired"]["default"]
        self.icon_hover =   self.icons["wired"]["hover"]
        self.icon_active =  self.icons["wired"]["active"]
        self.setColor("blue")
        self.updateIcon()

    def setWifiLow(self):
        self.icon_default = self.icons["wifi_low"]["default"]
        self.icon_hover =   self.icons["wifi_low"]["hover"]
        self.icon_active =  self.icons["wifi_low"]["active"]
        self.setColor("blue")
        self.updateIcon()

    def setWifiMedium(self):
        self.icon_default = self.icons["wifi_medium"]["default"]
        self.icon_hover =   self.icons["wifi_medium"]["hover"]
        self.icon_active =  self.icons["wifi_medium"]["active"]
        self.setColor("blue")
        self.updateIcon()

    def setWifiHigh(self):
        self.icon_default = self.icons["wifi_high"]["default"]
        self.icon_hover =   self.icons["wifi_high"]["hover"]
        self.icon_active =  self.icons["wifi_high"]["active"]
        self.setColor("blue")
        self.updateIcon()

    def updateIcon(self):
        if self.active:
            self.indicator.setIcon(self.icon_active)
        elif self.hovering:
            self.indicator.setIcon(self.icon_hover)
        else:
            self.indicator.setIcon(self.icon_default)

    def setColor(self, color):
        self.color = color
        self.setProperty("color", color)
        self.refreshStyle()
