import threading
from pystray import Menu, MenuItem, Icon
import os
import sys
import winshell
from PIL import Image
from main import show_app

image = Image.open("assets/favicon.ico")
icon_started = False


def on_clicked1(item):
    global state1, state2
    if os.path.exists(path):
        return
    else:
        with open(path, 'w') as file:
            file.write(f"@echo off \n{python_path} {pathfile} \npause")

    state1 = True
    state2 = False


def on_clicked2(item):
    global state1, state2
    if not os.path.exists(path):
        return
    else:
        os.remove(path)
    state1 = False
    state2 = True


def show_window():
    global window_text
    show_app()
    window_text = "Minimize app"


def quit_window():
    global app, process
    icon.stop()
    process.kill()
    app.destroy()
    os._exit(1)


def get_paths():
    global path, pathfile, python_path, state1, state2
    path = winshell.startup()
    path = os.path.join(path, 'test.bat')
    pathfile = f"\"{os.path.abspath(sys.argv[0])}\""
    python_path = f"\"{sys.executable}\""
    if os.path.exists(path):
        state1 = True
        state2 = False
    else:
        state1 = False
        state2 = True


class IconThread(threading.Thread):

    def __init__(self, *icon_args, **icon_kwargs):
        self.icon = None
        self._icon_args = icon_args
        self._icon_kwargs = icon_kwargs

        threading.Thread.__init__(self, daemon=True)

    def run(self):
        self.icon = Icon(*self._icon_args, **self._icon_kwargs)
        self.icon.run()

    def stop(self):
        if self.icon:
            self.icon.stop()


def init_icon():
    global icon
    get_paths()
    window_text = 'idk yet lole'
    icon = IconThread('Riot Account Manager', image, menu=Menu(
        MenuItem((lambda text: window_text), show_window),
        MenuItem('Run on startup', Menu(
            MenuItem('Enable', on_clicked1, checked=lambda item1: state1),
            MenuItem('Disable', on_clicked2, checked=lambda item2: state2))),
        MenuItem('Exit the program', quit_window)))


def run_icon():
    global window_text
    if not icon.is_alive():
        icon.start()
