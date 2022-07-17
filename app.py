import PySimpleGUI as sg
from Factories.Factories import Factories

## FUNCIONES

#Metodo que comprueba si se tiene que cerrar la ejecución
def runWindow():
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        elif event == "WindowEvent":
            print(window.size)

        elif event == "btnSync":
            factorie.Sorteos.Sync()
            

## LAYOUT

layout = [[
    sg.Text("Prueba simple de sincronización"),
    sg.Button('Sincronizar', key='btnSync')
]]

## WINDOWS

factorie = Factories()
factorie.Migrations.Upgrade()

window = sg.Window("Euromillones estadísticas", layout, default_element_size=(12,1), resizable=True, finalize=True)
window.bind('<Configure>', "WindowEvent")

runWindow()

window.close()

