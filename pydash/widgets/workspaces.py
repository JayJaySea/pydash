from PySide6.QtCore import  QSize, Qt, QTime
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QFrame
)

from pydash.widgets.button import WorkspaceButton
from pydash.controller import AwesomeWM

class Workspaces(QFrame):
    def __init__(self, number, vertical=False, parent=None):
        super().__init__(parent)
        self.number = number
        self.vertical = vertical
        self.controller = AwesomeWM()
        self.controller.workspace_changed.connect(self.workspaceChanged)
        self.controller.occupied_workspaces_status.connect(self.setOccupiedStatus)
        self.current_workspace = "1"

        self.initLayout()
        self.workspaceChanged(self.current_workspace)

    def initLayout(self):
        layout = QVBoxLayout() if self.vertical else QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.workspaces = {}
        for i in range(0, self.number):
            label = str((i + 1)%10)
            index = str(i + 1)
            button = WorkspaceButton(label, "green", index)
            button.clicked.connect(self.controller.goToWorkspace)
            self.workspaces[index] = button
            layout.addWidget(button)
            
        self.setLayout(layout)

    def workspaceChanged(self, index):
        self.workspaces[self.current_workspace].setInactive()
        self.current_workspace = index
        self.workspaces[index].setActive()

    def setOccupiedStatus(self, occupied):
        for index in self.workspaces:
            workspace = self.workspaces[index]
            if index in occupied:
                workspace.setOccupied()
            else:
                workspace.setUnoccupied()

