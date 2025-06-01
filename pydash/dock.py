from PySide6.QtCore import  QSize, Qt, QTime
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QGridLayout,
    QMainWindow,
    QWidget,
    QStackedWidget,
)

from pydash.widgets.workspaces import Workspaces
from pydash.widgets.pomodoro import Pomodoro
from pydash.widgets.clock import Clock
from pydash.widgets.controls import Controls
from pydash.widgets.button import MusicButton, KaliButton, WindowsButton, BugButton
from pydash.controller import LofiPlayer

class Dock(QMainWindow):
    def __init__(self, geometry):
        super().__init__()
        
        self.setObjectName("Dock")
        self.setWindowTitle("PyDashDock")
        self.setGeometry(geometry)
        self.initCentralWidget()

    def initCentralWidget(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 0)
        self.layout.setColumnStretch(2, 1)

        self.layout.addWidget(LeftSide(), 0, 0, alignment=Qt.AlignLeft)
        self.clock = Clock("yellow")
        self.layout.addWidget(self.clock, 0, 1, alignment=Qt.AlignCenter)
        self.layout.addWidget(Controls(), 0, 2, alignment=Qt.AlignRight)

        self.central = QWidget()
        self.central.setLayout(self.layout)

        self.setCentralWidget(self.central)

class LeftSide(QFrame):
    def __init__(self):
        super().__init__()
        self.player = LofiPlayer()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        layout.addWidget(Workspaces(10))

        separator = QWidget()
        separator.setFixedSize(10, 30)
        layout.addWidget(separator)

        layout.addWidget(Pomodoro(1500, 300))

        separator = QWidget()
        separator.setFixedSize(10, 30)
        layout.addWidget(separator)
        
        self.music = MusicButton()
        self.music.clicked_left.connect(self.player.togglePlaying)
        self.music.clicked_right.connect(self.player.nextTrack)
        layout.addWidget(self.music)

        self.kali = KaliButton()
        layout.addWidget(self.kali)

        self.windows = WindowsButton()
        layout.addWidget(self.windows)

        self.malware = BugButton()
        layout.addWidget(self.malware)

        self.setLayout(layout)
