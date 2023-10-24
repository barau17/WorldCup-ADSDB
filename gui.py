import PySimpleGUI as sg
import subprocess
import os
import shutil
import pandas as pd
import pathlib

from paths import temporalPath
from Utilities.os_utilities import getBaseAndExtensionOfFile

#------------- Functionality Definition -------------#

def isValidPath(file_path):
    if file_path and pathlib.Path(file_path).exists():
        return True
    sg.popup_error("Filepath not correct!")
    return False

def executeMain():
    try:
        # Replace 'main.py' with the path to your Python script.
        result = subprocess.run(['python3', 'main.py'], capture_output=True, text=True, check=True)

        # Print the standard output of the executed script.
        print("Script Output:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        # The executed script returned a non-zero exit code (indicating an error).
        print("Error occurred while executing main.py:")
        print(e.stderr)
    except FileNotFoundError:
        # The 'main.py' script was not found.
        print("main.py not found.")
    except Exception as e:
        # Other exceptions.
        print("An error occurred:", e)

def saveFile(file_path, destination_folder):
    if file_path:
        base, extension = getBaseAndExtensionOfFile(file_path)
        if extension == ".xslx":
            try:
                df = pd.read_excel(file_path)
                csv_file_path = os.path.splitext(file_path)[0] + ".csv"
                df.to_csv(csv_file_path, index=True)
                file_path = csv_file_path
            except Exception as e:
                sg.popup_error(f'Error converting XLSX to CSV: {str(e)}')
        if destination_folder:
            try:
                file_name = os.path.basename(file_path)
                destination_path = os.path.join(destination_folder, file_name)
                shutil.copy(file_path, destination_path)
                sg.popup(f'File "{file_name}" copied to {destination_folder}')
            except Exception as e:
                sg.popup_error(f'Error: {str(e)}')

def displayFile(file_path):
    df = pd.read_csv(file_path)
    file_name = os.path.basename(file_path)
    sg.popup_scrolled(df.dtypes, "=" * 50, df, title=file_name)

#------------- GUI Definition -------------#

layout = [
            [sg.Text("Input File:"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=(("CSV Files", "*.csv*"),("Excel Files", "*.xlsx*"),))],
            [sg.Exit(), sg.Button("Display File"), sg.Button("Save File"), sg.Button("Analyze")],
]

window = sg.Window("WorldCup Data Management Backbone", layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    if event == "Save File":
        file_path = values["-IN-"]
        if isValidPath(file_path):
            saveFile(file_path, temporalPath)
    if event == "Display File":
        file_path = values["-IN-"]
        if isValidPath(file_path):
            displayFile(file_path)
    if event == "Analyze":
        executeMain()
window.close()