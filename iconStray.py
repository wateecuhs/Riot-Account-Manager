import PIL.Image
import customtkinter
import json
import logging
import requests
import time
import winshell
import os
import sys
import threading
import PIL
import base64
from pystray import Menu, MenuItem, Icon
from win32gui import FindWindow, GetWindowRect
from pystray import Menu, MenuItem, Icon
import winshell
import win32com.client
from ico import get_icon

ICON_PATH = get_icon()
image = PIL.Image.open(ICON_PATH)



def on_clicked1(item):
    global state1, state2
    if os.path.exists(path):
        return
    else:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        print(os.path.abspath(sys.argv[0]))
        shortcut.Targetpath = os.path.abspath(sys.argv[0])
        shortcut.IconLocation = os.path.abspath(sys.argv[0])
        shortcut.save()
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



def quit_window():
    global app, process
    print('exiting..')
    icon.stop()
    os._exit(1)


def get_paths():
    global path, pathfile, python_path, state1, state2

    appdata_path = os.path.join(os.getenv('APPDATA')[:-8], 'Local', 'Riot Account Manager')
    if not os.path.exists(appdata_path):
        os.makedirs(appdata_path)

    path = winshell.startup()
    path = os.path.join(path, 'Riot Account Manager.lnk')
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
    icon = IconThread('Riot Account Manager', image, menu=Menu(
        MenuItem('Run on startup', Menu(
            MenuItem('Enable', on_clicked1, checked=lambda item1: state1),
            MenuItem('Disable', on_clicked2, checked=lambda item2: state2))),
        MenuItem('Exit the program', quit_window)))


def run_icon():
    if not icon.is_alive():
        icon.start()

