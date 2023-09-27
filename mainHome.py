import PySimpleGUI as sg

def helloWorld(name):
    sg.Window(title="Hello World ".__add__(name), layout=[[sg.Text(name)]], margins=(200, 100)).read()