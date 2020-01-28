# global constants
import os
from os import path
from psutil import users

comp_users = users()[0]
uname = comp_users.name

# Assume its Windows Environment
top_level = r"C:\Users"

root_dir  = path.dirname(__file__)
data      = path.join(root_dir, "data")
image_dir = path.join(root_dir, "images")
images    = path.join(data, "images")

# sqlite3 database
DATABASE_NAME = "rabbit_db.db"

# csv files
csv_borrowed  = "borrowed_rabbits.csv"
females       = "females.csv"
males         = "males.csv"
just_born     = "new born batch.csv"

RABBIT_IMAGE_SIZE    = (300, 300)
FRAME_SIZE           = (300, 300)
RESIZE_IMAGE         = (200, 200)

# images
DEFAULT_RABBIT_IMAGE = path.join(image_dir, "default.png")
BORROW_RABBIT_IMAGE1 = path.join(image_dir, "borrow rabbit image s.png")
CALENDAR_IMAGE1      = path.join(image_dir, "date.png")
ICON                 = path.join(image_dir, "default-icon.ico")
SAVE_IMAGE           = path.join(image_dir, "save1.png")
DEFAULT_RABBIT_PIC   = path.join(images, "default-rabbit-pic.png")
BANNER_GIF           = path.join(image_dir, "banner.gif")
DEV_IMAGE            = path.join(images, "donn.png")

# database handler
DATABASE_URI         = path.join(data, DATABASE_NAME)

# file handlers
BORROWED_CSV         = path.join(data, csv_borrowed)
FEMALES_CSV          = path.join(data, females)
MALES_CSV            = path.join(data, females)
NEW_BORN_BATCH_CSV   = path.join(data, just_born)

def img_folder():
    if uname in os.listdir(top_level):
        INIT_IMAGE_FOLDER = f"C:\\Users\\{uname}\\Pictures"
        if path.isdir(INIT_IMAGE_FOLDER):
            pass

        else:
            INIT_IMAGE_FOLDER = f"C:\\Users\\{uname}\\My Pictures"

        return INIT_IMAGE_FOLDER

DEV_INFO = '''
Add About us / About Developer here :)

# Contact: +263778060126
# Github : @DonnC

__version__ 0.0.1
@2019
'''