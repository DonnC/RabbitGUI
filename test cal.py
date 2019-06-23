import PySimpleGUI as sg
import os, io
from PIL import Image

def get_image_as_data(filename, width=None, height=None):
    # from PIL import Image         # use `pip install Pillow` to install PIL
    # import io
    im = Image.open(filename)
    if isinstance(width, int) and isinstance(height, int): # Resize if dimensions provided
        im = im.resize((width, height))
    im_bytes = io.BytesIO()
    im.save(im_bytes, format="GIF")
    return im_bytes.getvalue()

def get_image_files_list(folder):
    all_files = os.listdir(folder)
    image_files = []
    for file in all_files:
        extension = file.lower().split(".")[-1]
        print(file, extension)
        if extension in ["jpg", "png", "jpeg", "jpe", "gif"]:
            image_files.append(file)
    image_files.sort()
    return image_files

def demo_photo_picker3(default_folder, default_pic):
    folder = default_folder
    files_listing = get_image_files_list(folder)
    column1 = [
        [
            sg.Listbox(values=files_listing,
                change_submits=True, # trigger an event whenever an item is selected
                size=(25, 30),
                font=("Helvetica", 12),
                key="files_listbox")
        ]
    ]
    column2 = [
        [
            sg.Image( data=get_image_as_data(default_pic, 500, 500),
                key="image", size=(500,500))
        ]
    ]
    layout = [
        [
            sg.Text("Select your photos folder"),
            sg.InputText(key="photo_folder", change_submits=True), # trigger an event whenever the item is changed
            sg.FolderBrowse(target="photo_folder")
        ], [
            sg.Column( column1 ),
            sg.Column( column2 )
        ], [
            sg.Button(button_text="Exit")
        ]
    ]
    window = sg.Window('Pick a photo').Layout(layout)
    while True:
        event, values = window.Read()
        print(event)
        print(values)
        if event == "photo_folder":
            if values["photo_folder"] != "":
                if os.path.isdir(values["photo_folder"]):
                    folder = values["photo_folder"]
                    image_files = get_image_files_list(values["photo_folder"])
                    window.FindElement("files_listbox").Update(values=image_files)
                    if len(image_files) > 0:
                        full_filename = os.path.join(folder,image_files[0])
                        window.FindElement("image").Update(data=get_image_as_data(full_filename, 500, 500))
        if event == "files_listbox":
            full_filename = os.path.join(folder,values["files_listbox"][0])
            window.FindElement("image").UpdateAnimation(get_image_as_data(full_filename, 500, 500))
        if event is None or event == 'Exit':
            return None

if __name__ == "__main__":
    default_pic = "kof.png"
    result = demo_photo_picker3(".", default_pic)
    print(result)