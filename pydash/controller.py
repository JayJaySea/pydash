import os
import vlc
import sys
import random
import socket
import subprocess
import psutil
import pulsectl
import json
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QSocketNotifier, QIODevice, Signal, QObject, QTimer, QRunnable, QThreadPool
from PySide6.QtConcurrent import QtConcurrent
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from pydash.data import DATA_DIR, MUSIC_DIR, VMS_DATA, VM_KEY

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
        return 0

    def getCurrentAudioVolume(self):
        sink = self.getDefaultSink()
        if sink:
            return int(sink.volume.value_flat * 100)
        
        return None

    def setAudioVolume(self, value):
        sink = self.getDefaultSink()
        if sink:
            self.pulse.volume_set_all_chans(sink, value/100)

    def getAudioMute(self):
        sink = self.getDefaultSink()
        if sink:
            return sink.mute
        
        return None

    def setAudioMute(self, mute):
        sink = self.getDefaultSink()
        if sink:
            self.pulse.mute(sink, mute)

    def getDefaultSink(self):
        try:
            sink = self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)
            return sink
        except BaseException:
            return None

    def getCurrentMicrophoneVolume(self):
        source = self.getDefaultSource()
        if source:
            return int(source.volume.value_flat * 100)
        
        return None

    def setMicrophoneVolume(self, value):
        source = self.getDefaultSource()
        if source:
            self.pulse.volume_set_all_chans(source, value/100)

    def getMicrophoneMute(self):
        source = self.getDefaultSource()
        if source:
            return source.mute

        return None

    def setMicrophoneMute(self, mute):
        source = self.getDefaultSource()
        if source:
            self.pulse.mute(source, mute)

    def getDefaultSource(self):
        try:
            source = self.pulse.get_source_by_name(self.pulse.server_info().default_source_name)
            return source
        except BaseException:
            return None

    def launchFirefox(self):
        subprocess.Popen("firefox")

    def launchThunderbird(self):
        subprocess.Popen("thunderbird")

    def launchTeams(self):
        subprocess.Popen("teams-for-linux")

    def launchCryptomator(self):
        subprocess.Popen("cryptomator")

class LofiPlayer(QObject):
    track_end = Signal()

    def __init__(self):
        super().__init__()
        self.instance = vlc.Instance()
        self.tracks = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav', '.ogg'))]
        self.track_end.connect(self.nextTrack)
        self.player = self.instance.media_player_new()
        self.playing = False
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, lambda _: self.track_end.emit())

        self.player.set_media(self.selectRandom())
        self.preloaded = self.selectRandom()

    def selectRandom(self):
        if not self.tracks:
            return

        track = os.path.join(MUSIC_DIR, random.choice(self.tracks))
        media = self.instance.media_new(track)
        return media

    def togglePlaying(self):
        if self.player.is_playing():
            self.player.pause()
            self.playing = False
        else:
            self.player.play()
            self.playing = True

    def nextTrack(self):
        self.player.set_media(self.preloaded)
        if self.playing:
            self.player.play()

        self.preloaded = self.selectRandom()

class VMController(QObject):
    update_alive = Signal(set, set)

    def __init__(self):
        super().__init__()
        self.data = None
        with open(VMS_DATA) as vms_file:
            self.data = json.load(vms_file)

        if not self.data:
            return

        self.executor = ThreadPoolExecutor()
        self.alive = set()
        self.prev_alive = set()

        self.timers = {}
        self.futures = []

        self.initAliveCheck()

    def initAliveCheck(self):
        for vm_name in self.data.get("vms"):
            vm = self.data["vms"][vm_name]

            self.startVMCheck(vm)
            self.timers[vm_name] = QTimer()
            self.timers[vm_name].timeout.connect(lambda vm=vm: self.startVMCheck(vm))
            self.timers[vm_name].start(30000)

    def targetedAliveCheck(self, vm_name):
        vm = self.data["vms"][vm_name]

        if not self.timers.get(vm_name):
            return

        self.timers[vm_name].stop()
        self.timers[vm_name].start(1000)

    def stopTargetedCheck(self, vm_name):
        self.timers[vm_name].stop()
        self.timers[vm_name].start(30000)

    def startVMCheck(self, vm, targeted=False):
        future = self.executor.submit(self.checkVMState, vm)
        future.add_done_callback(lambda future: self.updateVMState(future))

        self.futures.append(future) 

    def checkVMState(self, vm, targeted=False):
        error = subprocess.run(['ssh', '-i', VM_KEY,'-q', '-o', 'ConnectTimeout=1',  f"{vm['ssh_username']}@{vm['ip']}", 'echo ready'], capture_output=True).returncode

        if error:
            return (vm["vm_name"], False, targeted)

        return (vm["vm_name"], True, targeted)

    def updateVMState(self, future):
        vm_name, state, targeted = future.result()
        if not targeted:
            self.prev_alive = self.alive.copy()
        if state:
            self.alive.add(vm_name)
        else:
            self.alive.discard(vm_name)

        if self.alive.difference(self.prev_alive) or self.prev_alive.difference(self.alive):
            self.update_alive.emit(self.alive, self.prev_alive)

        self.futures.remove(future)

    def toggleVM(self, vm_name):
        if any(vm_name in alive_vm for alive_vm in self.alive):
            self.poweroff(vm_name)
        else:
            self.launch(vm_name)

    def launch(self, vm_name):
        vm = self.data["vms"][vm_name]

        command = self.data["commands"]["launch"] if not vm.get("commands", {}).get("launch") else vm["commands"]["launch"]
        command = command.format(
            vm_name=vm["vm_name"]
        )
        subprocess.run(command, shell=True).returncode

    def poweroff(self, vm_name):
        vm = self.data["vms"][vm_name]
        command = self.data["commands"]["poweroff"] if not vm.get("commands", {}).get("poweroff") else vm["commands"]["poweroff"]
        command = command.format(
            vm_name=vm["vm_name"]
        )
        subprocess.run(command, shell=True).returncode

    def getVms(self):
        if not self.data:
            return None
        
        vms = []
        for vm_name in self.data.get("vms"):
            vms.append(vm_name)

        return vms

    def isAlive(self, vm_name):
        if any(vm_name in alive_vm for alive_vm in self.alive):
            return True
        return False

