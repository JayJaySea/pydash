from PySide6.QtCore import  QSize, Qt, QTime
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QGridLayout,
    QMainWindow,
    QWidget,
    QStackedWidget,
)

from pydash.widgets.workspaces import Workspaces
from pydash.widgets.clock import Clock
from pydash.widgets.controls import Controls

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

        self.layout.addWidget(Workspaces(10), 0, 0, alignment=Qt.AlignLeft)
        self.layout.addWidget(Clock("yellow"), 0, 1, alignment=Qt.AlignCenter)
        self.layout.addWidget(Controls(), 0, 2, alignment=Qt.AlignRight)

        self.central = QWidget()
        self.central.setLayout(self.layout)

        self.setCentralWidget(self.central)
