import PySimpleGUI as sg
import os, sys

layout = [
    [sg.Text("Aplicación Desktop - Sociedad Científica")],
    [sg.Text("Nombre:"), sg.Input(key="NOMBRE")],
    [sg.Button("Saludar"), sg.Button("Abrir web (local)"), sg.Button("Salir")]
]

window = sg.Window("Sociedad Científica - Desktop", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Salir"):
        break
    if event == "Saludar":
        sg.popup(f"Hola {values.get('NOMBRE') or 'amig@'} 👋")
    if event == "Abrir web (local)":
        # intenta abrir run.py (requiere que estéis en entorno con GUI)
        if sys.platform.startswith("win"):
            os.system("start python run.py")
        else:
            os.system("python run.py &")
window.close()
