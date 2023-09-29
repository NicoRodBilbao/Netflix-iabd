import image_listbox as ilb
import PySimpleGUI as sg
import os.path

my_ilb = ilb.ImageListBox(
    ["test1", ["test2", (os.path.dirname(__file__)+"\logo.png")]],
    headings=["tree_myilb"],
    num_rows=25,
    size=(24 * 9, 10 * 10),
    #select_mode=ilb.SELECT_MODE_SINGLE,
    enable_events=True,
    key="tree_myilb",
    default_icon=ilb.icon_folder,
)
my_layout = [[sg.Image(filename=(os.path.dirname(__file__)+"\logo.png"), key="-LOGO-",size=(50,50))],[sg.VSeparator()],[my_ilb.element]]
window = sg.Window("a",my_layout)

while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            break