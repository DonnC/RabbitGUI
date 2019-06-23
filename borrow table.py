# # table of available rabbit data in the database
from PySimpleGUI import *
import pyperclip
from pprint import pprint
from settings import *

matrix = [
["John", "Male", "grey-white pathces", "new zealand white", "1", "zimbabwe", "20 June 2019", "28 June 2019", "Healthy rabbit ready to mate"],
["VaMatema", "Female", "grey", "new zealand brown", "2", "russia", "01 June 2019", "18 June 2019", "Healthy rabbit"],
["Murambinda", "Male", "white pathces", "Germany", "3", "london", "18 June 2019", "20 June 2019", "need thorough inspection"],
["Farai", "Male", "brown", "new zealand", "2", "zimbabwe", "20 June 2019", "27 June 2019", "borrowed rabbit"],
["Mr Kudai", "Female", "white", "new zealand black", "1", "zimbabwe", "02 June 2019", "17 June 2019", "Healthy"],
["Mutambandiro", "Male", "black", "new zealand white", "2", "russia", "09 June 2019", "12 June 2019", "Healthy, need recheck"],
["Jangano Kufa", "Female", "black pathces", "new zealand white", "1", "london", "20 June 2019", "23 June 2019", "Healthy rabbit"],
["Lloyd Guru", "Female", "black-white pathces", "new zealand white", "1", "zimbabwe", "21 June 2019", "30 June 2019", "need to inspect"]]

head = ['Owner', 'Sex', 'Color', 'Breed', 'Quantity', 'Location', 'Borrowed', 'Return', 'Notes']
#pprint(matrix)
table_right_click_opt = [
    '&Right',
    [
        'Copy',
        'Delete',
        'Undo'
    ]
]

img = "donn.png"
image_frame_layout = [
    [Text("Rabbit image")],
    [Image(filename=DEFAULT_RABBIT_PIC, size=(300, 300), tooltip="rabbit identification image", key="_RABBIT_IMAGE_")]
]

table_frame = [
    [
        Table(values=matrix,
           headings=head,
           num_rows=10,
           display_row_numbers=True,
           enable_events=True,
           font=("Berlin Sans FB", 11),
           alternating_row_color='lightblue',
           key='_BORROW_TABLE_',
           size=(700, 100),
           vertical_scroll_only=False,
           right_click_menu=table_right_click_opt)
    ]
]

layout = [
    [Text("\t\t\t\t"), Frame("", layout=image_frame_layout, size=(200, 200), key="_RABBIT_IMAGE_FRAME_")],
    [Frame('Borrowed Rabbits Data', table_frame, title_color='grey', font=("Elephant", 15), size=(800, 200))]
]

#layout = [[Column(layout1)]]

window = Window('Borrowed Rabbits', layout,
                font=('Helvetica', 15),
                resizable=True,
                ).Finalize()

# The Event Loop
while True:
    event, values = window.Read()

    if event is None or event == "Exit":
        break

    if event == 'Delete':
        # delete table in row indicated
        del_index = values.get("_BORROW_TABLE_")
        if len(del_index) > 0:
            del_index = del_index[0]

            # assign global for 'undo' action
            global deleted_row

            deleted_row = matrix.pop(del_index)
            deleted_owner = deleted_row[0].title()
            print("delete: ", del_index)
            window.Element("_BORROW_TABLE_").Update(values=matrix)
            PopupAutoClose(f"{deleted_owner} deleted!")

    if event == "Copy":
        copy_index = values.get("_BORROW_TABLE_")
        if len(copy_index) > 0:
            copy_index = copy_index[0]
            row_list = matrix.pop(copy_index)
            copy_string = ""
            for info in row_list:
                copy_string += info + "\n"

            pyperclip.copy(copy_string)
            print("copied: ", copy_string)
            PopupAutoClose("Data copied to Clipboard!")

    if event == "Undo":
        # re-insert the last deleted entry in the table
        try:
            if deleted_row:
                matrix.append(deleted_row)
                window.Element("_BORROW_TABLE_").Update(values=matrix)
                PopupAutoClose("Delete Operation revoked!")
                # avoid duplicates in the table
                deleted_row = None

            else:
                PopupQuickMessage("No action to 'UNDO'", font=("Calibri", 12))

        except NameError:
            PopupQuickMessage("No action to 'UNDO'", font=("Calibri", 12))


    print(event, values)