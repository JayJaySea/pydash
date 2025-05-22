from pathlib import Path
import subprocess
import os
import shutil
from pydash.scripts.color_icons import color_icons, parse_scss_variables, load_icons

DEBUG=os.getenv("DEBUG")
DATA_DIR=os.path.join(Path.home(), ".local", "share", "pydash")
PIDFILE = "/tmp/pydash.pid"

if DEBUG:
    DATA_DIR=os.path.join(Path.cwd(), "data")

def init():
    if os.path.exists(DATA_DIR) and not DEBUG:
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "icons/"), exist_ok=True)
    root_dir = Path(__file__).resolve().parent

    fonts_src = os.path.join(root_dir, "fonts")
    fonts_dest = os.path.join(DATA_DIR, "fonts")
    shutil.copytree(fonts_src, fonts_dest, dirs_exist_ok=True)

    style_src = os.path.join(root_dir, "style", "main.scss")
    style_dest = os.path.join(DATA_DIR, "style.css")
    command = ["sassc", style_src, style_dest]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        print(result.returncode)
        exit(result.returncode)

    colors = parse_scss_variables(os.path.join(root_dir, "style", "colors.scss"))
    icons = load_icons(os.path.join(root_dir, "icons"))
    recolor = "#ffffff"
    output_dir = os.path.join(DATA_DIR, "icons")

    color_icons(icons, colors, recolor, output_dir)

def kill_existing_instance():
    if os.path.isfile(PIDFILE):
        try:
            with open(PIDFILE, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)  # Or SIGKILL if you're savage
        except Exception:
            pass  # If something goes wrong, assume the process is already dead
        os.remove(PIDFILE)

def write_pid():
    with open(PIDFILE, "w") as f:
        f.write(str(os.getpid()))
