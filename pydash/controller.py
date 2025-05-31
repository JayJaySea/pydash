import os
import sys
import socket
import subprocess
import psutil
import pulsectl
from PySide6.QtCore import QSocketNotifier, QIODevice, Signal, QObject, QTimer
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class AwesomeWM(QObject):
    workspace_changed = Signal(str)
    audio_volume_changed = Signal(int)
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
            elif signal == "audio-volume-increased":
                self.audio_volume_changed.emit(int(args))
            elif signal == "audio-volume-decreased":
                self.audio_volume_changed.emit(-int(args))

            client_socket.close()
        except BlockingIOError:
            pass

    def parseData(self, data):
        signal, args = data.split(":")
        if signal == "occupied-workspaces":
            return signal, args.split(",")
        else:
            return signal, args

    def goToWorkspace(self, index):
        lua_code = f"require('awful').screen.focused().tags[{index}]:view_only()"
        subprocess.run(["awesome-client"], input=lua_code.encode())
        self.workspace_changed.emit(index)
    
    def refresh(self):
        lua_code = f"awesome.restart()"
        subprocess.run(["awesome-client"], input=lua_code.encode())

class System(QObject):
    connection_status = Signal(dict)
    audio_changed = Signal(int)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(System, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        super().__init__()

        self.pulse = pulsectl.Pulse('volume-control')

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateConnectionStatus)
        self.timer.start(1000)

    def reboot(self):
        os.system("reboot")

    def shutdown(self):
        os.system("poweroff")

    def updateConnectionStatus(self):
        connection = {
            "status": self.getConnectionStatus()
        }
        if connection["status"] == "wifi":
            connection["strength"] = self.getWifiStrength()

        self.connection_status.emit(connection)

    def getConnectionStatus(self):
        wired_patterns = ['eth', 'en', 'lan', 'ethernet', 'em']
        wireless_patterns = ['wlan', 'wifi', 'wl', 'wireless', 'wi-fi', 'airport']

        for iface, stats in psutil.net_if_stats().items():
            if stats.isup:
                if any(pattern in iface.lower() for pattern in wired_patterns):
                    return "wired"
                if any(pattern in iface.lower() for pattern in wireless_patterns):
                    return "wifi"
        return "disconnected"
    
    def getWifiStrength(self):
        try:
            output = subprocess.check_output(["nmcli", "-t", "-f", "ACTIVE,SIGNAL", "dev", "wifi"]).decode()
            for line in output.strip().split("\n"):
                active, signal = line.split(":")
                if active == "yes":
                    return int(signal)
        except Exception:
            pass
        return None

    def getCurrentAudioVolume(self):
        sink = self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)
        return int(sink.volume.value_flat * 100)

    def setAudioVolume(self, value):
        sink = self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)
        self.pulse.volume_set_all_chans(sink, value/100)

    def getAudioMute(self):
        sink = self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)
        return sink.mute

    def setAudioMute(self, mute):
        sink = self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)
        self.pulse.mute(sink, mute)


