# table of available rabbit data in the database
from PySimpleGUI import *
from pprint import pprint

def main():
    from random import randint

    ChangeLookAndFeel('GreenTan')
    # ------ Menu Definition ------ #
    menu_def = [['&File', ['!&Open', '&Save::savekey', '---', '&Properties', 'E&xit']],
                ['!&Edit', ['!&Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Debugger', ['Popout', 'Launch Debugger']],
                ['&Toolbar', ['Command &1', 'Command &2', 'Command &3', 'Command &4']],
                ['&Help', '&About...'], ]

    treedata = TreeData()

    treedata.Insert("", '_A_', 'Tree Item 1', [1, 2, 3], )
    treedata.Insert("", '_B_', 'B', [4, 5, 6], )
    treedata.Insert("_A_", '_A1_', 'Sub Item 1', ['can', 'be', 'anything'], )
    treedata.Insert("", '_C_', 'C', [], )
    treedata.Insert("_C_", '_C1_', 'C1', ['or'], )
    treedata.Insert("_A_", '_A2_', 'Sub Item 2', [None, None])
    treedata.Insert("_A1_", '_A3_', 'A30', ['getting deep'])
    treedata.Insert("_C_", '_C2_', 'C2', ['nothing', 'at', 'all'])

    for i in range(100):
        treedata.Insert('_C_', i, i, [])

    frame1 = [
        [Input('Input Text', size=(25, 1)), ],
        [Multiline(size=(30, 5), default_text='Multiline Input')],
    ]

    frame2 = [
        [Listbox(['Listbox 1', 'Listbox 2', 'Listbox 3'], size=(20, 5))],
        [Combo(['Combo item 1', ], size=(20, 3), text_color='red', background_color='red')],
        [Combo(['Combo item 1', ], size=(20, 3), text_color='red', background_color='red')],
        [Spin([1, 2, 3], size=(4, 3))],
    ]

    frame3 = [
        [Checkbox('Checkbox1', True), Checkbox('Checkbox1')],
        [Radio('Radio Button1', 1), Radio('Radio Button2', 1, default=True, tooltip='Radio 2')],
        [T('', size=(1, 4))],
    ]

    frame4 = [
        [Slider(range=(0, 100), orientation='v', size=(7, 15), default_value=40),
         Slider(range=(0, 100), orientation='h', size=(11, 15), default_value=40), ],
    ]
    #matrix = [[str(x * y) for x in range(4)] for y in range(8)]
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
    pprint(matrix)

    frame5 = [
        [Table(values=matrix,
               headings=head,
               auto_size_columns=False,
               display_row_numbers=True,
               change_submits=False,
               justification='right',
               num_rows=10,
               alternating_row_color='lightblue',
               key='_table_',
               text_color='black',
               size=(400, 200)),
         T(' '),
         Tree(data=treedata, headings=['col1', 'col2', 'col3'], change_submits=True, auto_size_columns=True,
              num_rows=10, col0_width=10, key='_TREE_', show_expanded=True, )],
    ]

    graph_elem = Graph((800, 150), (0, 0), (800, 300), key='+GRAPH+')

    frame6 = [
        [graph_elem],
    ]

    tab1 = Tab('Graph Number 1', frame6, tooltip='tab 1')
    tab2 = Tab('Graph Number 2', [[]])

    layout1 = [
        [Menu(menu_def)],
        [Image(data=DEFAULT_BASE64_ICON)],
        [Text('You are running the py file itself', font='ANY 15', tooltip='My tooltip', key='_TEXT1_')],
        [Text('You should be importing it rather than running it', font='ANY 15')],
        [Frame('Input Text Group', frame1, title_color='red'),
         Image(data=DEFAULT_BASE64_LOADING_GIF, key='_IMAGE_')],
        [Frame('Multiple Choice Group', frame2, title_color='green'),
         Frame('Binary Choice Group', frame3, title_color='purple', tooltip='Binary Choice'),
         Frame('Variable Choice Group', frame4, title_color='blue')],
        [Frame('Structured Data Group', frame5, title_color='red'), ],
        # [Frame('Graphing Group', frame6)],
        [TabGroup([[tab1, tab2]])],
        [ProgressBar(max_value=800, size=(60, 25), key='+PROGRESS+'), Button('Button'), B('Normal'),
         Button('Exit', tooltip='Exit button')],
    ]

    layout = [[Column(layout1)]]

    window = Window('Window Title', layout,
                    font=('Helvetica', 13),
                    # background_color='black',
                    right_click_menu=['&Right', ['Right', '!&Click', '&Menu', 'E&xit', 'Properties']],
                    # transparent_color= '#9FB8AD',
                    resizable=True,
                    ).Finalize()
    graph_elem.DrawCircle((200, 200), 50, 'blue')
    i = 0
    while True:  # Event Loop
        # TimerStart()
        event, values = window.Read(timeout=0)
        if event != TIMEOUT_KEY:
            print(event, values)
        if event is None or event == 'Exit':
            break
        if i < 800:
            graph_elem.DrawLine((i, 0), (i, randint(0, 300)), width=1, color='#{:06x}'.format(randint(0, 0xffffff)))
        else:
            graph_elem.Move(-1, 0)
            graph_elem.DrawLine((i, 0), (i, randint(0, 300)), width=1, color='#{:06x}'.format(randint(0, 0xffffff)))

        window.FindElement('+PROGRESS+').UpdateBar(i % 800)
        window.Element('_IMAGE_').UpdateAnimation(DEFAULT_BASE64_LOADING_GIF, time_between_frames=50)
        i += 1
        if event == 'Button':
            window.Element('_TEXT1_').SetTooltip('NEW TEXT')
            window.SetTransparentColor('#9FB8AD')
            window.Maximize()
        elif event == 'Normal':
            window.Normal()
        elif event == 'Popout':
            show_debugger_popout_window()
        elif event == 'Launch Debugger':
            show_debugger_window()
        # TimerStop()
    window.Close()
    
if __name__ == '__main__':
    main()
    exit(69)