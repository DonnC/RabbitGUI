# utilities
import csv
import os
import datetime
import logging
import shutil

from datetime import datetime as dtime
from timestring import Date

from os import path
from PIL import Image
from settings import *

from pprint import pprint

def copy_image(img_loc):
    # copy image to our working folder
    try:
        new_loc = shutil.copy(img_loc, images)
        return new_loc

    except Exception as e:
        pass

def convert_image(image_file):
    # convert the file in our folder
    try:
        img = path.basename(image_file)
        dir_name = path.dirname(image_file)
        img_n, ext = path.splitext(img)
        n_img = path.join(dir_name, img_n + ".png")
        img_f = Image.open(image_file)
        # resize image
        img_f1 = img_f.resize(RESIZE_IMAGE, Image.ANTIALIAS)
        img_f1.save(n_img)
        #send2trash.send2trash(image_file)
        return path.basename(n_img)

    except Exception as e:
        print("No Convert: ", e)
        return path.basename(image_file)

def check_alert(day, win_obj, pg=None):
    # TODO:: Improve this algo to function properly | check alert
    day = int(day)
    if day < -1:
        msg = "return date EXCEEDED!"
        pg.PopupOK("Days Exceeded", text_color="firebrick")

    elif day == -1:
        msg = "return date is TODAY"
        pg.PopupOK("Return today", text_color="springgreen")

    elif day == 0:
        msg = "return date is TOMORROW"
        pg.PopupAutoClose("Reminder, tommorow", grab_anywhere=True)

    else:
        msg = "Good!"

    return win_obj.FindElement("_DAYS_LEFT_ALERT_").Update(msg)

def get_image(img):
    # return path to image
    img = path.join(images, img)

    if path.isfile(img):
        return img

    return DEFAULT_RABBIT_PIC

def cleanBorrowData(data):
    # get data
    notes  = data.get("_ADDITIONAL_NOTES_")
    b_date = data.get('_BORROW_DATE_')
    owner  = data.get('_OWNER_')
    breed  = data.get('_RABBIT_BREED_')
    color  = data.get('_RABBIT_COLOR_')
    image  = data.get('_RABBIT_IMAGE_CHANGE_')
    loc    = data.get('_RABBIT_LOCATION_')
    num    = data.get('_RABBIT_QUANTITY_')
    Fsex   = data.get('_RABBIT_SEX_FEMALE_')
    r_date = data.get('_RETURN_DATE_')
    sex    = 'Male'

    if Fsex:
        sex = 'Female'

    if b_date:
        b_date = b_date.strftime("%B %d %Y")

    if r_date:
        r_date = r_date.strftime("%B %d %Y")

    image = convert_image(copy_image(image))

    row = [owner, sex, color, breed, num, loc, b_date, r_date, image, notes]
    return row

def check_borrow():
    # check if csv file exists with borrowed data. else create it with the headers given
    table_header = ['Owner', 'Sex', 'Color', 'Breed', 'Quantity', 'Location', 'Borrowed', 'Return', 'Image', 'Notes']
    if path.isfile(BORROWED_CSV) and path.exists(BORROWED_CSV):
        pass

    else:
        bhand = open(BORROWED_CSV, "w", newline="")
        writer = csv.writer(bhand)
        writer.writerow(table_header)
        bhand.close()

def frame(matrix_borrow):
    # create data for frame
    matrix_frame = []

    for the_row in matrix_borrow:
        added     = the_row[6]
        returning = the_row[7]
        if not added.startswith("Bor") and not returning.startswith("Ret"):
            date_obj     = Date(added).date
            ret_date_obj = Date(returning).date
            now          = dtime.now()
            days_kept    = now - date_obj
            days_left    = ret_date_obj - now
            new_row      = the_row
            new_row.append(days_kept.days)
            new_row.append(days_left.days)
            matrix_frame.append(new_row)

    return matrix_frame

def ReadBorrowTable():
    # dont include 'Image' & 'Notes' in the table
    check_borrow()
    borrowed      = open(BORROWED_CSV, "r")
    reader        = csv.reader(borrowed)
    matrix_borrow = list(reader)
    matrix_table  = []
    matrix_frame  = []

    for rows in matrix_borrow:
        matrix_table.append(rows[:-2])
        matrix_frame.append(rows[:-2])

    borrowed.close()

    if len(matrix_borrow) <= 1:
        # file is empty
        head = ['Owner', 'Sex', 'Color', 'Breed', 'Quantity', 'Location', 'Borrowed']
        matrix_table = [head, ['Null', 'Null', 'Null', 'Null', 'Null', 'Null', 'Null']]
        return matrix_table, [], matrix_frame

    return matrix_table, matrix_borrow, matrix_frame

def WriteBorrowTable(data, all_rows=False):
    check_borrow()
    table_header = ['Owner', 'Sex', 'Color', 'Breed', 'Quantity', 'Location', 'Borrowed', 'Return', 'Image', 'Notes']
    try:
        if all_rows:
            borrow_info = open(BORROWED_CSV, "w", newline="")
            writer      = csv.writer(borrow_info)
            data        = data.insert(0, table_header)
            writer.writerows(data)

        else:
            borrow_info = open(BORROWED_CSV, "a", newline="")
            writer      = csv.writer(borrow_info)
            row         = cleanBorrowData(data)
            writer.writerow(row)
            print("Info row added to file")

        print("[INFO] Data inserted in csv file")
        borrow_info.close()
        return (True, 1)

    except Exception as e:
        print("[ERROR] Could not write data to table. Error: ", e)
        return (None, e)