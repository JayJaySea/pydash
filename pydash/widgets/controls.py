from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer
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
from pydash.controller import System
from pydash.widgets.button import LabelButton, ShutdownButton

class Controls(QFrame):
    def __init__(self):
        super().__init__()
        self.system = System()
        self.setMaximumHeight(30)
        
        self.initLayout()

    def initLayout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        shutdown = ShutdownButton()
        shutdown.clicked.connect(self.shutdown)
        layout.addWidget(shutdown)
        
        self.setLayout(layout)

    def shutdown(self):
        self.system.shutdown()
