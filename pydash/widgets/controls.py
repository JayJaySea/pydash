import os
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QTimer, QSize, Qt, QObject, Signal
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QGridLayout,
    QMainWindow,
    QWidget,
    QStackedWidget,
    QFrame,
    QSlider
)

from datetime import datetime
from pydash.data import DATA_DIR, MUSIC_DIR
from pydash.controller import System, AwesomeWM
from pydash.widgets.button import LabelButton, ShutdownButton, RebootButton, RefreshButton, IconButton, MusicButton, FirefoxButton, MailButton, TeamsButton, RobotButton

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

        self.cryptomator = RobotButton()
        self.cryptomator.clicked.connect(self.system.launchCryptomator)
        layout.addWidget(self.cryptomator)

        self.teams = TeamsButton()
        self.teams.clicked.connect(self.system.launchTeams)
        layout.addWidget(self.teams)

        self.mail = MailButton()
        self.mail.clicked.connect(self.system.launchThunderbird)
        layout.addWidget(self.mail)

        self.firefox = FirefoxButton()
        self.firefox.clicked.connect(self.system.launchFirefox)
        layout.addWidget(self.firefox)

        separator = QWidget()
        separator.setFixedSize(10, 30)
        layout.addWidget(separator)

        self.microphone = MicrophoneControl()
        layout.addWidget(self.microphone)

        self.audio = AudioControl()
        layout.addWidget(self.audio)

        separator = QWidget()
        separator.setFixedSize(10, 30)
        layout.addWidget(separator)

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

class AudioControl(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.system = System()

        self.audio_timer = QTimer()
        self.audio_timer.timeout.connect(self.getFirstAudioVolume)
        self.audio_timer.start(250)

        self.current_volume = 0
        self.mute = False

        self.controller = AwesomeWM()
        self.controller.audio_volume_changed.connect(lambda _: self.updateVolumeInfo(self.system.getCurrentAudioVolume(), self.mute))

        self.setObjectName("BorderedContainer")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setFixedSize(70, 26)

        self.slider.valueChanged.connect(self.changeVolume)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 5, 0)
        layout.setSpacing(2)
        self.button = AudioButton()
        self.button.clicked.connect(self.toggleMute)
        layout.addWidget(self.button)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def getFirstAudioVolume(self):
        volume = self.system.getCurrentAudioVolume()
        mute = self.system.getAudioMute()

        if volume is not None and mute is not None:
            self.current_volume = volume
            self.mute = mute
            self.updateVolumeInfo(self.current_volume, self.mute)

            self.audio_timer.stop()

    def changeVolume(self, value):
        self.system.setAudioVolume(value)
        self.updateVolumeInfo(value, self.mute)

    def updateVolumeInfo(self, volume, mute):
        volume = max(0, volume)
        self.current_volume = min(100, volume)
        self.mute = mute

        self.slider.setValue(self.current_volume)

        if self.mute:
            self.button.setAudioMute()
            self.setColor("red")
            return
        elif self.current_volume >= 66:
            self.button.setAudioHigh()
        elif self.current_volume >= 33:
            self.button.setAudioMedium()
        else:
            self.button.setAudioLow()

        self.setColor("green")

    def toggleMute(self):
        self.mute = not self.mute
        self.system.setAudioMute(self.mute)
        self.updateVolumeInfo(self.current_volume, self.mute)

    def setColor(self, color):
        self.color = color
        self.slider.setProperty("color", color)
        self.setProperty("color", color)
        self.refreshStyle()

    def refreshStyle(self):
        self.slider.style().unpolish(self.slider)
        self.slider.style().polish(self.slider)
        self.slider.update()
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

class AudioButton(IconButton):
    def __init__(self, size="medium", parent=None, id=None):
        super().__init__("audio_mute", "red", size=size, parent=parent, id=id)
        self.setObjectName("BorderlessButton")
        self.setFixedSize(26, 26)
        self.icons = {
            "audio_mute": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "audio_mute.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "audio_mute-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "audio_mute-active.png"))
            },
            "audio_low": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "audio_low.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "audio_low-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "audio_low-active.png")),
            },
            "audio_medium": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "audio_medium.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "audio_medium-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "audio_medium-active.png"))
            },
            "audio_high": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "audio_high.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "audio_high-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "audio_high-active.png"))
            }
        }
        self.indicator.setIconSize(QSize(18, 18))
        
    def setAudioMute(self):
        self.icon_default = self.icons["audio_mute"]["default"]
        self.icon_hover =   self.icons["audio_mute"]["hover"]
        self.icon_active =  self.icons["audio_mute"]["active"]
        self.setColor("red")
        self.updateIcon()

    def setAudioLow(self):
        self.icon_default = self.icons["audio_low"]["default"]
        self.icon_hover =   self.icons["audio_low"]["hover"]
        self.icon_active =  self.icons["audio_low"]["active"]
        self.setColor("green")
        self.updateIcon()

    def setAudioMedium(self):
        self.icon_default = self.icons["audio_medium"]["default"]
        self.icon_hover =   self.icons["audio_medium"]["hover"]
        self.icon_active =  self.icons["audio_medium"]["active"]
        self.setColor("green")
        self.updateIcon()

    def setAudioHigh(self):
        self.icon_default = self.icons["audio_high"]["default"]
        self.icon_hover =   self.icons["audio_high"]["hover"]
        self.icon_active =  self.icons["audio_high"]["active"]
        self.setColor("green")
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

class MicrophoneControl(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.system = System()

        self.current_volume = self.system.getCurrentMicrophoneVolume()
        self.mute = self.system.getMicrophoneMute()

        self.setObjectName("BorderedContainer")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setFixedSize(70, 26)
        self.slider.setValue(self.current_volume)
        self.slider.valueChanged.connect(self.changeVolume)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 5, 0)
        layout.setSpacing(2)
        self.button = MicrophoneButton()
        self.button.clicked.connect(self.toggleMute)
        layout.addWidget(self.button)
        layout.addWidget(self.slider)

        self.setLayout(layout)
        self.updateVolumeInfo(self.current_volume, self.mute)

    def changeVolume(self, value):
        self.system.setMicrophoneVolume(value)
        self.updateVolumeInfo(value, self.mute)

    def updateVolumeInfo(self, volume, mute):
        volume = max(0, volume)
        self.current_volume = min(100, volume)
        self.mute = mute

        if self.mute:
            self.button.setMicrophoneMute()
            self.setColor("red")
        else:
            self.button.setMicrophoneDefault()
            self.setColor("purple")

    def toggleMute(self):
        self.mute = not self.mute
        self.system.setMicrophoneMute(self.mute)
        self.updateVolumeInfo(self.current_volume, self.mute)

    def setColor(self, color):
        self.color = color
        self.slider.setProperty("color", color)
        self.setProperty("color", color)
        self.refreshStyle()

    def refreshStyle(self):
        self.slider.style().unpolish(self.slider)
        self.slider.style().polish(self.slider)
        self.slider.update()
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

class MicrophoneButton(IconButton):
    def __init__(self, size="medium", parent=None, id=None):
        super().__init__("microphone_mute", "red", size=size, parent=parent, id=id)
        self.setObjectName("BorderlessButton")
        self.setFixedSize(26, 26)
        self.icons = {
            "microphone_mute": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "microphone_mute.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "microphone_mute-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "microphone_mute-active.png"))
            },
            "microphone": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "microphone.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "microphone-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "microphone-active.png")),
            }
        }
        self.indicator.setIconSize(QSize(18, 18))
        
    def setMicrophoneMute(self):
        self.icon_default = self.icons["microphone_mute"]["default"]
        self.icon_hover =   self.icons["microphone_mute"]["hover"]
        self.icon_active =  self.icons["microphone_mute"]["active"]
        self.setColor("red")
        self.updateIcon()

    def setMicrophoneDefault(self):
        self.icon_default = self.icons["microphone"]["default"]
        self.icon_hover =   self.icons["microphone"]["hover"]
        self.icon_active =  self.icons["microphone"]["active"]
        self.setColor("purple")
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
