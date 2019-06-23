# main GUI call
import PySimpleGUI as pg
from faker import Faker
import os
from settings import *

fake = Faker()
img = "donn.png"

tabs_layout = [pg.Button('Refresh'), pg.Btn('New Batch'), pg.Btn('Add Female'), pg.Btn('Add Male'), pg.Btn('Borrowed')]

image_frame_layout = [
    [pg.Text("Rabbit image")],
    [pg.Image(filename=img, size=RABBIT_IMAGE_SIZE, tooltip="rabbit identification image", key="_RABBIT_IMAGE_")],
    [pg.Input("Change rabbit image", key="_RABBIT_IMAGE_CHANGE_"), pg.FileBrowse()],
    [pg.OK(key="_OK_BUTTON_"), pg.Cancel()]
]

layout = [
    tabs_layout,
    [pg.Text("\t\t"), pg.CalendarButton("Choose Date", bind_return_key=True, auto_size_button=True), pg.OK(), pg.Cancel()],
    [pg.Text("\t\t\t\t"), pg.Frame("", layout=image_frame_layout, size=FRAME_SIZE)]
]

window = pg.Window("MyGUI", layout, auto_size_buttons=True, grab_anywhere=True, resizable=True)

# The Event Loop
while True:
    event, values = window.Read()

    if event is None:
        break

    if event == '_OK_BUTTON_':
        # update rabbit image
        new_image_file = values['_RABBIT_IMAGE_CHANGE_']
        if os.path.isfile(new_image_file):
            if new_image_file.endswith(".png"):
                window.Element('_RABBIT_IMAGE_').Update(new_image_file, size=RABBIT_IMAGE_SIZE)
            else:
                pg.PopupError("Image file unsupported", "Please choose .png file", title="Unsupported file" ,auto_close=True, auto_close_duration=5)
        else:
            pg.PopupAutoClose("An image file is expected!", title="No file found")

    print(event, values)