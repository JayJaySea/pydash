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
from pydash.controller import LofiPlayer, VMController

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
        self.vm_controller = VMController()
        self.vm_controller.update_alive.connect(self.updateAlive)

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

        self.initVMButtons(layout)

        self.setLayout(layout)

    def initVMButtons(self, layout):
        self.vms = {}
        vms = self.vm_controller.getVms()

        for vm_name in vms:
            if vm_name == "kali":
                self.vms["kali"] = KaliButton()
            elif vm_name == "windows":
                self.vms["windows"] = WindowsButton()
            elif vm_name == "malware":
                self.vms["malware"] = BugButton()
            else:
                continue

            self.vms[vm_name].clicked_left.connect(lambda name=vm_name: self.toggleVM(name))
            layout.addWidget(self.vms[vm_name])

    def updateAlive(self, alive, prev_alive):
        launched = alive.difference(prev_alive)
        powered_off = prev_alive.difference(alive)

        for vm_name in self.vms:
            if any(vm_name in alive_vm for alive_vm in alive):
                if any(vm_name in launched_vm for launched_vm in launched) and self.vms[vm_name].blinking:
                    self.vms[vm_name].stopBlinking()
                    self.vm_controller.stopTargetedCheck(vm_name)
                else:
                    self.vms[vm_name].setActive()
            else:
                if any(vm_name in powered_off_vm for powered_off_vm in powered_off) and self.vms[vm_name].blinking:
                    self.vms[vm_name].stopBlinking()
                    self.vm_controller.stopTargetedCheck(vm_name)
                else:
                    self.vms[vm_name].setInactive()

    def toggleVM(self, vm_name):
        self.vms[vm_name].startBlinking(not self.vm_controller.isAlive(vm_name))
        self.vm_controller.toggleVM(vm_name)
        self.vm_controller.targetedAliveCheck(vm_name)
