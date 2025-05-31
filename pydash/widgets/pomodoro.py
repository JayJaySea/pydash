import os
from PySide6.QtCore import  QSize, Qt, QTime, QTimer
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QFrame
)

from pydash.widgets.button import IconButton, LabelButton
from pydash.controller import AwesomeWM
from pydash.data import DATA_DIR

class Pomodoro(QFrame):
    def __init__(self, work_time, break_time, parent=None):
        super().__init__(parent)
        self.work = True
        self.running = False

        self.work_time = work_time
        self.break_time = break_time

        self.time = self.work_time

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start()

        self.setObjectName("LabelButton")
        self.setFixedHeight(30)
        self.setFixedWidth(110)
        self.setProperty("color", "red")
        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.switch_button = PomodoroSwitchButton()
        self.switch_button.clicked.connect(self.switchMode)
        layout.addWidget(self.switch_button)

        self.timer_button = TimerButton(self.time)
        self.timer_button.clicked.connect(self.switchRunning)
        layout.addWidget(self.timer_button)

        self.setLayout(layout)

    def updateTime(self):
        if not self.running:
            return

        self.time = self.time - 1
        self.timer_button.setTime(self.time)

        if self.time < 0:
            self.switchMode()

    def switchMode(self):
        self.work = not self.work
        if self.work:
            self.time = self.work_time
            self.switch_button.setWork()
            self.timer_button.setColor("red")
            self.setProperty("color", "red")
            self.refreshStyle()
        else:
            self.time = self.break_time
            self.switch_button.setBreak()
            self.timer_button.setColor("blue")
            self.setProperty("color", "blue")
            self.refreshStyle()
        self.timer_button.setTime(self.time)

    def switchRunning(self):
        self.running = not self.running

    def refreshStyle(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

class PomodoroSwitchButton(IconButton):
    def __init__(self, size="medium", parent=None, id=None):
        super().__init__("cogs", "red", size=size, parent=parent, id=id)
        self.icons = {
            "break": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "cup.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "cup-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "cup-active.png"))
            },
            "work": {
                "default": QPixmap(os.path.join(DATA_DIR, "icons", "cogs.png")),
                "hover":  QPixmap(os.path.join(DATA_DIR, "icons", "cogs-hover.png")),
                "active":   QPixmap(os.path.join(DATA_DIR, "icons", "cogs-active.png"))
            }
        }
        self.setObjectName("BorderlessButton")
        self.setFixedSize(22, 22)

    def setWork(self):
        self.icon_default = self.icons["work"]["default"]
        self.icon_hover =   self.icons["work"]["hover"]
        self.icon_active =  self.icons["work"]["active"]
        self.setColor("red")
        self.updateIcon()

    def setBreak(self):
        self.icon_default = self.icons["break"]["default"]
        self.icon_hover =   self.icons["break"]["hover"]
        self.icon_active =  self.icons["break"]["active"]
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

class TimerButton(LabelButton):
    def __init__(self, seconds):
        super().__init__(" 00:00 ", "red", "medium")
        self.setTime(seconds)
        self.setObjectName("BorderlessButton")

    def setColor(self, color):
        self.color = color

    def setTime(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60

        self.setLabel(" {:02d}:{:02d} ".format(minutes, seconds))
