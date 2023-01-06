from pystray import Menu, MenuItem, Icon
import os
import sys
import winshell
from PIL import Image
import threading

image = Image.open("assets/favicon.ico")


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


def show_window(icon, item):
    global app
    icon.stop()
    app.deiconify()


def quit_window(icon, item):
    global app
    icon.stop()
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


def init_icon():
    global icon
    get_paths()
    icon = Icon('test', image, menu=Menu(MenuItem(
        'Show window',
        show_window)
        , MenuItem(
            'Run on startup',
            Menu(
                MenuItem(
                    'Enable',
                    on_clicked1,
                    checked=lambda item1: state1),
                MenuItem(
                    'Disable',
                    on_clicked2,
                    checked=lambda item2: state2))),
        MenuItem(
            'Exit the program',
            quit_window)))


def run_icon():
    icon.run_detached()
