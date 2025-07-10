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

class Stats(QFrame):
    def __init__(self):
        super().__init__()
