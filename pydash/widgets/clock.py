from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QGridLayout,
    QMainWindow,
    QWidget,
    QStackedWidget,
)

from datetime import datetime
from pydash.widgets.button import LabelButton

class Clock(LabelButton):
    def __init__(self, color):
        super().__init__(self.getDateTime(), color, "medium")
        self.setMaximumHeight(30)

    def getDateTime(self):
        return datetime.now().strftime(" %H:%M   %d-%m ")

    def updateDateTime(self):
        self.setLabel(self.getDateTime())
        self.adjustSize()
