# main GUI call
import PySimpleGUI as pg
from datetime import datetime as dtime
import pyperclip
import os
from utils import ReadBorrowTable, WriteBorrowTable, get_image
from settings import *
import time

from pprint import pprint

layout = [
    [pg.Image(BANNER_GIF, key="_BANNER_GIF_")],
    [pg.Text("Hello there")],
    [pg.Button("Update GIF", key='_UPDATE_GIF_')],
    [pg.Button("Release button", key="_RELEASE_GIF_")]
]

window = pg.Window("MyGUI", layout, grab_anywhere=True, resizable=True)

# The Event Loop
while True:
    event, values = window.Read()

    if event is None or event == "Exit":
        break

    # update GIF play
    window.Element("_UPDATE_GIF_")._ClickHandler("_UPDATE_GIF_")
    print("click")
    time.sleep(2)
    window.Element('_UPDATE_GIF_')._ClickHandler("_RELEASE_GIF_")
    print("release")
    window.Element("_BANNER_GIF_").UpdateAnimation(BANNER_GIF, time_between_frames=10)
    print("update gif")

    print(event, values)