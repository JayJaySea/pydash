from PySide6 import QtGui
from PySide6.QtCore import QSize, Qt, QPoint, Signal, QEvent
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QPushButton, QStyleOption, QStyle, QFrame, QLabel, QHBoxLayout
import os
from pydash.data import DATA_DIR

class LabelButton(QFrame):
    clicked = Signal(str)

    def __init__(self, label, color, font_size=None, parent=None):
        super().__init__(parent)
        self.setObjectName("LabelButton")
        self.label = label
        self.hovering = False
        self.active = False
        self.color = color

        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setProperty("color", color)

        self.indicator = QLabel(label, self)
        self.indicator.setAlignment(Qt.AlignCenter)
        self.indicator.setObjectName("LabelButtonIndicator")
        self.indicator.setProperty(font_size, True)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.indicator)

        self.setLayout(layout)

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        self.hoverStyle()

    def mouseMoveEvent(self, event):
        mouse_pos = event.globalPosition().toPoint()
        button_rect = self.rect().translated(self.mapToGlobal(QPoint(0, 0)))

        if button_rect.contains(mouse_pos):
            if not self.hovering:
                self.hovering = True
        else:
            if self.hovering:
                self.hovering = False

        if not self.hovering:
            self.unsetCursor()
            self.defaultStyle()
        elif self.active:
            self.activeStyle()

    def leaveEvent(self, event):
        self.defaultStyle()

    def mousePressEvent(self, event):
        self.active = True
        self.activeStyle()

    def mouseReleaseEvent(self, event):
        self.active = False
        self.defaultStyle()
        if self.hovering:
            self.clicked.emit(self.label)

    def defaultStyle(self):
        self.indicator.setProperty("hover", False)
        self.indicator.setProperty("color", False)
        self.refreshStyle()

    def hoverStyle(self):
        self.indicator.setProperty("hover", True)
        self.refreshStyle()

    def activeStyle(self):
        self.indicator.setProperty("color", self.color)
        self.refreshStyle()

    def refreshStyle(self):
        self.indicator.style().unpolish(self.indicator)
        self.indicator.style().polish(self.indicator)
        self.indicator.update()

    def setLabel(self, label):
        self.indicator.setText(label)

class WorkspaceButton(LabelButton):
    clicked = Signal(str)

    def __init__(self, label, color, index, parent=None):
        super().__init__(label, color, "medium", parent)
        self.setFixedSize(30, 30)

        self.index = index
        self.occupied = False
        self.indicator.setObjectName("WorkspaceButtonIndicator")

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        self.hoverStyle()

    def mouseMoveEvent(self, event):
        pass

    def leaveEvent(self, event):
        if not self.active:
            self.defaultStyle()

    def mousePressEvent(self, event):
        self.active = True
        self.clicked.emit(self.index)

    def mouseReleaseEvent(self, event):
        pass

    def setInactive(self):
        self.active = False
        self.defaultStyle()

    def setActive(self):
        self.active = True
        self.activeStyle()

    def setOccupied(self):
        self.occupied = True
        self.indicator.setProperty("occupied", True)
        self.refreshStyle()

    def setUnoccupied(self):
        self.occupied = False
        self.indicator.setProperty("occupied", False)
        self.refreshStyle()


class IconButton(QPushButton):
    clicked = Signal(str)

    def __init__(self, icon_name, color, size="large", parent=None, id=None):
        super().__init__(parent)
        self.setObjectName("IconButton")
        self.icon_default = QPixmap(os.path.join(DATA_DIR, "icons", icon_name+".png"))
        self.icon_hover = QPixmap(os.path.join(DATA_DIR, "icons", icon_name+"-hover.png"))
        self.icon_active = QPixmap(os.path.join(DATA_DIR, "icons", icon_name+"-active.png"))
        self.hovering = False
        self.active = False
        self.id = id
        self.color = color

        self.setMouseTracking(True)
        self.setProperty("color", color)

        self.indicator = QPushButton(self)
        self.indicator.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.indicator.setObjectName("LabelButtonIndicator")
        self.indicator.setProperty(size, True)
        self.indicator.setIcon(self.icon_default)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.indicator)

        self.setLayout(layout)

        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setSize(size)

    def setSize(self, size):
        if size == "small":
            self.setFixedSize(20, 20)
            self.setIconSize(QSize(6, 6))
        elif size == "medium":
            self.setFixedSize(30, 30)
            self.indicator.setFixedSize(22, 22)
            self.indicator.setIconSize(QSize(18, 18))
        else:
            self.setFixedSize(40, 40)
            self.setIconSize(QSize(26, 26))

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        self.hoverStyle()

    def mouseMoveEvent(self, event):
        mouse_pos = event.globalPosition().toPoint()
        button_rect = self.rect().translated(self.mapToGlobal(QPoint(0, 0)))

        if button_rect.contains(mouse_pos):
            if not self.hovering:
                self.hovering = True
        else:
            if self.hovering:
                self.hovering = False

        if not self.hovering:
            self.defaultStyle()
        elif self.active:
            self.activeStyle()

    def leaveEvent(self, event):
        self.unsetCursor()
        self.defaultStyle()

    def mousePressEvent(self, event):
        self.active = True
        self.activeStyle()

    def mouseReleaseEvent(self, event):
        self.active = False
        self.defaultStyle()
        if self.hovering:
            self.clicked.emit(self.id)

    def defaultStyle(self):
        self.indicator.setProperty("hover", False)
        self.indicator.setProperty("color", False)
        self.indicator.setIcon(self.icon_default)
        self.refreshStyle()

    def hoverStyle(self):
        self.indicator.setProperty("hover", True)
        self.indicator.setIcon(self.icon_hover)
        self.refreshStyle()

    def activeStyle(self):
        self.indicator.setProperty("color", self.color)
        self.indicator.setIcon(self.icon_active)
        self.refreshStyle()

    def refreshStyle(self):
        self.indicator.style().unpolish(self.indicator)
        self.indicator.style().polish(self.indicator)
        self.indicator.update()
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

class ShutdownButton(IconButton):
    def __init__(self, size="medium", parent=None, id=None):
        super().__init__("shutdown", "red", size=size, parent=parent, id=id)

class RebootButton(IconButton):
    def __init__(self, size="medium", parent=None, id=None):
        super().__init__("reboot", "yellow", size=size, parent=parent, id=id)

class RefreshButton(IconButton):
    def __init__(self, size="medium", parent=None, id=None):
        super().__init__("refresh", "purple", size=size, parent=parent, id=id)
