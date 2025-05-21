from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRect
from PySide6.QtGui import QFontDatabase
from sys import argv
import signal
from pydash.dock import Dock
import pydash.data as data
from pydash.data import DATA_DIR
import os


def main():
    data.init()
    app = QApplication(argv)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    with open(os.path.join(DATA_DIR, "style.css")) as style:
        app.setStyleSheet(style.read())

    font_path = os.path.join(DATA_DIR, "fonts", "Orbitron-Regular.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)

    dock = Dock(QRect(0, 0, 2550, 30))
    dock.show()

    app.exec()


if __name__ == "__main__":
    main()

