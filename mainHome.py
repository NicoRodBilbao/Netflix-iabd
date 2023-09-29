import image_listbox as ilb
import PySimpleGUI as sg
import os.path

def helloWorld(name):
    sg.Window(title="Hello World ".__add__(name), layout=[[sg.Text(name)]], margins=(200, 100)).read()
    
def mainHome():
    sg.theme('DarkRed2')
    firstColumn =  [[sg.Image(filename=(os.path.dirname(__file__)+"\logo.png"), key="-LOGO-",size=(50,50))],
                    [
                        sg.Listbox(
                        values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")
                    ]
                    ]
    secondColumn = [[ilb.ImageListBox(
        ["test1", ["test2", (os.path.dirname(__file__)+"\logo.png")]],
        headings=["tree_myilb"],
        num_rows=25,
        size=(24 * 9, 10 * 10),
        #select_mode=ilb.SELECT_MODE_SINGLE,
        enable_events=True,
        key="tree_myilb",
        default_icon=ilb.icon_folder,
    )]]

    layout = [[sg.Column(firstColumn),sg.VSeparator(),secondColumn]]
    
    window = sg.Window("Prueba", layout)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            break