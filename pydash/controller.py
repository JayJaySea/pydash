import os
import sys
import socket
import subprocess
from PySide6.QtCore import QSocketNotifier, QIODevice, Signal, QObject
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class AwesomeWM(QObject):
    workspace_changed = Signal(str)
    occupied_workspaces_status = Signal(list)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AwesomeWM, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True

        super().__init__()
        socket_path = "/tmp/awesome.sock"

        if os.path.exists(socket_path):
            os.remove(socket_path)

        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_socket.bind(socket_path)
        self.server_socket.listen(1)
        self.server_socket.setblocking(False)

        self.notifier = QSocketNotifier(self.server_socket.fileno(), QSocketNotifier.Read)
        self.notifier.activated.connect(self.acceptConnection)

    def acceptConnection(self):
        try:
            client_socket, _ = self.server_socket.accept()
            data = client_socket.recv(1024).decode().strip()
            signal, args = self.parseData(data)
            if signal == "workspace-changed":
                self.workspace_changed.emit(args)
            elif signal == "occupied-workspaces":
                self.occupied_workspaces_status.emit(args)

            client_socket.close()
        except BlockingIOError:
            pass

    def parseData(self, data):
        signal, args = data.split(":")
        if signal == "workspace-changed":
            return signal, args
        elif signal == "occupied-workspaces":
            return signal, args.split(",")

    def goToWorkspace(self, index):
        lua_code = f"require('awful').screen.focused().tags[{index}]:view_only()"
        subprocess.run(["awesome-client"], input=lua_code.encode())
        self.workspace_changed.emit(index)
    
    def refresh(self):
        lua_code = f"awesome.restart()"
        subprocess.run(["awesome-client"], input=lua_code.encode())

class System():
    def reboot(self):
        os.system("reboot")

    def shutdown(self):
        os.system("poweroff")
