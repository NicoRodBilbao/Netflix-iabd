import PySimpleGUI as sg
from mainHome import * 

def openSignUp():
    sg.theme('DarkRed2')
    layout = [  [sg.Text('Iniciar sesión')],
                [sg.Text('Usuario'), sg.InputText("Usuario")],
                [sg.Text('Contraseña'), sg.InputText("Usuario", password_char='*')],
                [sg.Button('Ok')]]
    
    window = sg.Window('Window Title', layout)
    
    """while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            window.close()
            break
        if values[0] == "nico" and values[1] == "nico":
            print("A")
            mainHome()
            #window.close()
            #break"""