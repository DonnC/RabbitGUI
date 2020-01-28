# main GUI call
import PySimpleGUI as pg
from datetime import datetime as dtime
import pyperclip
import os
from utils import ReadBorrowTable, WriteBorrowTable, get_image, check_alert
from settings import *

from pprint import pprint

# use dark mode instead
#pg.ChangeLookAndFeel('Dark')

# borrow tab design
borrow_tab = [
    [pg.Text(" "*100), pg.Image(BORROW_RABBIT_IMAGE1), pg.Text(" New Information\n Borrowed Rabbit", font=("Impact", 30), relief=pg.RELIEF_SUNKEN), pg.Image(BORROW_RABBIT_IMAGE1)],
    [pg.Text(" ")],
    [pg.Text("Owner Name   ", font=("Helvetica", 15)), pg.Text(" "*30), pg.InputText(tooltip="rabbit Owner name", size=(80, 2), font=("Bradley Hand ITC", 15), key="_OWNER_")],
    [pg.Text("Rabbit sex   ", font=("Helvetica", 15)), pg.Text(" "*36), pg.Radio("Male", "rabbit_sex", default=True, key="_RABBIT_SEX_MALE_", size=(30, 1), font=("Helvetica", 15)), pg.Radio("Female", "rabbit_sex", size=(30, 1), font=("Helvetica", 15), key="_RABBIT_SEX_FEMALE_")],
    [pg.Text("Rabbit color ", font=("Helvetica", 15)), pg.Text(" "*36), pg.InputText(tooltip="Rabbit color description", size=(80, 2), font=("Bradley Hand ITC", 15), key="_RABBIT_COLOR_")],
    [pg.Text("Rabbit breed ", font=("Helvetica", 15)), pg.Text(" "*34), pg.InputCombo(['New Zealand White', 'Germany'], size=(32, 2), font=("Helvetica", 15), key="_RABBIT_BREED_")],
    [pg.Text("Quantity     ", font=("Helvetica", 15)), pg.Text(" "*38), pg.Spin(values=[1,2,3,4,5,6,7,8,9,10], initial_value=1, size=(33, 2), font=("Helvetica", 15), key="_RABBIT_QUANTITY_")],
    [pg.Text("Location     ", font=("Helvetica", 15)), pg.Text(" "*38), pg.InputText(tooltip="where the rabbit is kept", font=("Bradley Hand ITC", 15), size=(80, 2), key="_RABBIT_LOCATION_")],
    [pg.Text("Borrowed     ", font=("Helvetica", 15)), pg.Text(" "*35), pg.CalendarButton("Select Borrowed Date", key="_BORROW_DATE_", close_when_date_chosen=False, size=(30, 2), font=("Helvetica", 11)), pg.Button("Show Date", button_color=("white","springgreen4"), key="_BORROW_DATE_OK_")],
    [pg.Text("Return Date  ", font=("Helvetica", 15)), pg.Text(" "*35), pg.CalendarButton("Select Return Date", key="_RETURN_DATE_", close_when_date_chosen=False, size=(30, 2), font=("Helvetica", 11)), pg.Button("Show Date", button_color=("white","springgreen4"), key="_RETURN_DATE_OK_")],
    [pg.Text("Rabbit Image ", font=("Helvetica", 15)), pg.Text(" "*33), pg.Input(font=("Bradley Hand ITC", 15), key="_RABBIT_IMAGE_CHANGE_", size=(60, 2)), pg.FileBrowse(button_text="Browse Images", size=(15, 1))],
    [pg.Text("Notes        ", font=("Helvetica", 15)), pg.Text(" "*39), pg.Multiline(default_text="Note", font=("Bradley Hand ITC", 15), tooltip="additional notes", enter_submits=True, autoscroll=True, auto_size_text=True,key="_ADDITIONAL_NOTES_")],
    [pg.Text("")],
    [pg.Text(" ")],
    [pg.Button(button_text="Save", button_color=("white", "springgreen4"), size=(23, 1), key="_BORROW_SAVE_"), pg.Button("Cancel", size=(23, 1), button_color=("white", "firebrick3"), key="_BORROW_CANCEL_")]
]

# FIXME:: Use tempfile than list duplicates
matrix, frame, org_matrix = ReadBorrowTable()
matrixx = matrix[1:]

# right-click operations
table_right_click_opt = [
    '&Right',
    [
        'Copy',
        'Delete',
        'Undo Delete'
    ]
]

# data table frame design
table_frame = [
    [
        pg.Table(values=matrixx,
           headings=matrix[0],
           num_rows=10,
           display_row_numbers=True,
           enable_events=True,
           font=("Berlin Sans FB", 11),
           alternating_row_color='lightblue',
           key='_BORROW_TABLE_',
           vertical_scroll_only=False,
           size=(800, 500),
           right_click_menu=table_right_click_opt,
           tooltip="right click for more options")
    ]
]

# default data on borrowed data frame - design
default_image_frame_layout = [
    [pg.Image(filename=DEFAULT_RABBIT_PIC, size=(300, 250), tooltip="rabbit identification image", key="_RABBIT_IMAGE_")]
]

# developer / about us image frame - design
dev_column_image = [
    [pg.Text(" "*80), pg.Frame("", layout=[[pg.Image(filename=DEV_IMAGE, size=(300, 450))]], size=(200, 200))]
]

# developer / about us info frame - design
dev_column_text = [
    [pg.Multiline(DEV_INFO, disabled=True, autoscroll=True, font=("Courier New", 13))]
]

table_tab = [
    [pg.Text("_" * 160)],
    [pg.Frame('Borrowed Rabbits Data', table_frame, title_color='grey', font=("Elephant", 15))]
]

# developer / about us tab frame - design
dev_tab = [
    [pg.Text(" "*120), pg.Text("The Developer", font=("Broadway", 15))],
    [pg.Text("_"*170)],
    [pg.Text("")],
    [pg.Column(dev_column_text), pg.Column(dev_column_image)]
]

# borrowed data tab - design
column_text = [
    [pg.Text(" "*30), pg.Text("INFORMATION DISPLAY", font=("Elephant", 20), text_color="grey")],
    [pg.Text("Rabbit Owner", font=("Comic Sans MS", 15)), pg.Text(" "*20), pg.Input("Owner Name", disabled=True, font=("Ink Free", 11), key="_R_OWNER_")],
    [pg.Text("Rabbit Location", font=("Comic Sans MS", 15)), pg.Text(" "*16), pg.Input("Where rabbit is kept", disabled=True, font=("Ink Free", 11), key="_LOCATION_")],
    [pg.Text("Days kept", font=("Comic Sans MS", 15)), pg.Text(" "*30), pg.Input("?", disabled=True, font=("Ink Free", 11), key="_DAYS_KEPT_")],
    [pg.Text("Days left", font=("Comic Sans MS", 15)), pg.Text(" "*31), pg.Input("?", disabled=True, font=("Ink Free", 11), key="_DAYS_LEFT_")],
    [pg.Text("Alert", font=("Comic Sans MS", 15)), pg.Text(" "*41), pg.Input("???", disabled=True, font=("Ink Free", 11), key="_DAYS_LEFT_ALERT_")],
    [pg.Text("Notes", font=("Comic Sans MS", 15)), pg.Text(" "*40), pg.Multiline(default_text="Additional\nNotes", background_color="lightgrey", size=(20, 5),autoscroll=True, disabled=True, font=("Ink Free", 11), key="_NOTES_")]
]

column_image = [
    [pg.Text(" "*80), pg.Frame("", layout=default_image_frame_layout, size=(200, 200), key="_RABBIT_IMAGE_FRAME_")]
]

layout1 = [
    [pg.Column(column_text), pg.Column(column_image)],
    [pg.Text("_" * 180)],
    [
        pg.Column([[pg.Frame('Borrowed Rabbits Data', table_frame, title_color='grey', font=("Elephant", 15))]]),
        pg.Column([[pg.Text(" "*10), pg.Button("Save Changes", button_color=("white", "springgreen4"), key="_TABLE_CHANGES_")]])
    ]
]

# main layout of UI - design
MAIN_LAYOUT = [
    [
        pg.TabGroup([
            [
                pg.Tab("Borrow a Rabbit", borrow_tab),
                pg.Tab("Borrowed Rabbits Records", layout1),
                pg.Tab("About the developer", dev_tab)
            ]],font=("Agency FB", 30), background_color="white", selected_title_color="green", title_color="brown")
    ]
]

# main window
window = pg.Window("MyRabbitGUI", MAIN_LAYOUT, grab_anywhere=True, resizable=True, icon=pg.DEFAULT_BASE64_ICON)

# The Event Loop
while True:
    DELETED_FLAG = False
    UNDO_FLAG    = False

    event, values = window.Read()

    if event is None or event == "Exit":
        break

    if event == "_BORROW_DATE_OK_":
        if values["_BORROW_DATE_"]:
            borrow_date = values["_BORROW_DATE_"].strftime("%d %B %Y")
            window.Element(key="_BORROW_DATE_").Update(borrow_date)

    if event == "_RETURN_DATE_OK_":
        if values["_RETURN_DATE_"]:
            return_date = values["_RETURN_DATE_"].strftime("%d %B %Y")
            window.Element(key="_RETURN_DATE_").Update(return_date)

    if event == "_BORROW_SAVE_":
        status, err = WriteBorrowTable(values)
        if status:
            pg.PopupQuickMessage("INFORMATION SAVED!", title="Confirmation", text_color="darkgreen")
            window.FindElement("_BORROW_TABLE_").Update(values=ReadBorrowTable()[0][1:])
        else:
            # error
            pg.ScrolledTextBox(err, title="Error!")

    if event == "_BORROW_CANCEL_":
        pg.PopupQuickMessage("Cancelled", title="Abort", text_color="red", no_titlebar=False)

    # -------------------- TABLE OPERATIONS -----------------------------
    if event == 'Delete':
        # FIXME:: After row is deleted, sync the whole table frame
        # delete table row indicated
        del_index = values.get("_BORROW_TABLE_")
        if del_index:
            del_index = del_index[0]

            # delete same row in original matrix
            org_matrix.pop(del_index)

            # assign global for 'undo' action
            global deleted_row

            deleted_row = matrixx.pop(del_index)
            deleted_owner = deleted_row[0].title()
            window.Element("_BORROW_TABLE_").Update(values=matrixx)
            pg.PopupQuickMessage(f"{deleted_owner} deleted!")
            DELETED_FLAG = True

    if event == "Copy":
        copy_index = values.get("_BORROW_TABLE_")
        if len(copy_index) > 0:
            copy_index = copy_index[0]
            row_list = matrixx.pop(copy_index)
            copy_string = ""
            for info in row_list:
                copy_string += info + "\n"

            pyperclip.copy(copy_string)
            pg.PopupQuickMessage("Copied to Clipboard!")

    if event == "Undo Delete":
        # re-insert the last deleted entry in the table
        try:
            if deleted_row:
                # append to original matrix
                org_matrix.append(deleted_row)

                matrixx.append(deleted_row)
                window.Element("_BORROW_TABLE_").Update(values=matrixx)
                pg.PopupQuickMessage("Delete Operation revoked!")
                # avoid duplicates in the table
                deleted_row = None
                UNDO_FLAG = True

            else:
                pg.PopupQuickMessage("No action to 'UNDO'", font=("Calibri", 12))

        except NameError:
            pg.PopupQuickMessage("No action to 'UNDO'", font=("Calibri", 12))

    # show image frame based on user selected row in the table
    if event == "_BORROW_TABLE_":
        row_index = values.get("_BORROW_TABLE_")

        if row_index:
            try:
                # get the index currently highlighted by the user on the table
                index  = row_index[0]
                framme = ReadBorrowTable()[1][1:]

                # get the index row data highlighted
                row = framme[index]

                # TODO:: Add calculation of days left and days kept
                #owner, sex, color, breed, num, loc, b_date, r_date, image, notes, days_kept, days_left = row
                owner, sex, color, breed, num, loc, b_date, r_date, image, notes = row

                # update info
                window.Element("_RABBIT_IMAGE_").Update(filename=get_image(image))
                window.Element("_R_OWNER_").Update(str(owner))
                window.Element("_LOCATION_").Update(str(loc))
                #window.Element("_DAYS_LEFT_").Update(abs(days_left))
                #window.Element("_DAYS_KEPT_").Update(str(days_kept))
                #check_alert(days_left, window, pg)
                window.Element("_NOTES_").Update(str(notes))

            except Exception as e:
                pg.Popup("There was an exception", "Encountered in frame index", e)
                print("[ERROR] There was a problem, ", e)

    if event == "_TABLE_CHANGES_":
        # re-confirm
        ret_key = pg.PopupOKCancel("Save changes permanently?")

        if ret_key == "OK" and DELETED_FLAG and UNDO_FLAG:
            # save the row to csv file
            # FIXME add proper data and avoid duplicates
            WriteBorrowTable(org_matrix, all_rows=True)
            window.FindElement("_BORROW_TABLE_").Update(values=ReadBorrowTable()[0][1:])
            pg.PopupQuickMessage("Table refreshed", keep_on_top=True)

    print(f"\n{'-'*30}\nEvent name: `{event}`\nVALUES: \n{pprint(values)}")