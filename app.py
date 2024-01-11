import curses
import os
import shutil
import subprocess
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression

from curses.textpad import Textbox, rectangle
from paths import temporalPath, dataBasesDir, predictions_folder, models_folder

featuresm1 = ['NPlayers', 'Glsp90', 'Astp90', 'CrdR']
featuresm2 = ['NPlayers', 'Gls', 'Ast', 'CrdR']

def make_predictions(file_path):
    if os.path.getsize(file_path) != 0:
        try:
            data = pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
            return
        except pd.errors.ParserError:
            print("Error: Unable to parse the file. Check the file format.")
            return
        
    else:
        data = pd.read_csv(os.path.join(predictions_folder, "fib_input.csv"))
    
    columns_to_drop = ['team_code', 'Age', 'Poss', 'PKatt', 'CrdY', 'advanced']
    test_X = data.drop(columns=columns_to_drop, axis=1)
    
    test_columns = test_X.columns.tolist()
    
    if test_columns == featuresm1:
        m1 = joblib.load(os.path.join(models_folder, "m1_best.pkl"))
        predm1 = m1.predict(test_X)
        # Metrics m1
        file_path1 = predictions_folder + 'm1_results.txt'
        with open(file_path1, 'w') as f:
            f.write(str(test_X))
            f.write('\n')
            f.write(str(predm1))
        print(f"Results report saved to {file_path1}")
        
    elif test_columns == featuresm2:
        m2 = joblib.load(os.path.join(models_folder, "m2_best.pkl"))
        predm2 = m2.predict(test_X)
        # Metrics m2
        file_path1 = predictions_folder + 'm2_results.txt'
        with open(file_path1, 'w') as f:
            f.write(str(test_X))
            f.write('\n')
            f.write(str(predm2))
        print(f"Results report saved to {file_path1}")
        
def predictions(stdscr, y_title, x_title, y_options, x_options):
    stdscr.clear()
    stdscr.refresh()
    while True:
        stdscr.addstr(y_title, x_title + 5, "- Prediction Zone -", curses.A_BOLD)
        stdscr.addstr(y_title + 1, x_title - 30, "Press 1 to execute the default predictions, Press 2 if you added a new file for predictions", curses.A_BOLD)
        stdscr.addstr(y_title + 2, x_title - 20, "A message will appear when the code finalizes its execution! Wait :)")
        stdscr.addstr(y_title + 3, x_title - 32, "CAREFUL: Make sure there is only one csv in the Predictions folder, and that is the one you want to use!")
        key = stdscr.getch()
        if key == ord('1'):  # Enter key
            file_path = predictions_folder + 'fib_input.csv'
            make_predictions(file_path)
            stdscr.addstr(y_title + 5, x_title - 14, "Predictions done! Check the predictions folder!")
        if key == ord('2'):
            csv_files = [file for file in os.listdir(predictions_folder) if file.endswith(".csv") and file != "input_fib.csv"]
            file_path = predictions_folder + csv_files[0]
            make_predictions(file_path)
            stdscr.addstr(y_title + 5, x_title - 14, "Predictions done! Check the predictions folder!")
        elif key == 27:  # Check for the Esc key
            break

    stdscr.clear()
    stdscr.refresh()

    welcome_message = " - WELCOME TO THE WORLDCUP PROJECT - "
    stdscr.addstr(y_title, x_title + 6, welcome_message, curses.A_BOLD)
    stdscr.addstr(y_title + 1, x_title + 2, " - DEVELOPED BY GABRIEL VAYÀ & MARC FALCÓN - ", curses.COLOR_RED)
    stdscr.addstr(y_title + 2, x_title + 2, " - --------------------------------------- - ")
    stdscr.addstr(y_title + 3, x_title + 3, "      --- DATA ANALYSIS BACKBONE ---    ")
    stdscr.refresh()
    

def add_file(stdscr, analysis_folder, y_title, x_title, y_options, x_options):
    stdscr.clear()
    stdscr.addstr(y_title, x_title - 6, "Enter the path of the file you want to add", curses.A_BOLD)
    stdscr.addstr(y_title + 10, x_title - 2, "[ Esc to return to the main menu ]")
    stdscr.addstr(y_title + 1, x_title - 8, "Be careful with the '/' before the inital path")
    stdscr.addstr(y_title + 2, x_title - 14, "Input a file with same structure as the ones in the project!")
    stdscr.addstr(y_title + 3, x_title - 13, "Press Enter once you write the path to add it to the folder")
    stdscr.addstr(y_title + 4, x_title - 20, "Now go to the Main menu and go to the Predictions Zone to get your results")
    rectangle(stdscr, y_title + 6, x_title - 39, y_title + 8, x_title + 70)
    stdscr.refresh()


    while True:
        key = stdscr.getch()
        if key == "":
            continue
        if key == curses.KEY_BACKSPACE:  # Backspace key pressed
            box.edit()
        elif key == 27:
            break
        editwin = curses.newwin(1, 100, y_title + 8, x_title - 30)
        stdscr.refresh()

        box = Textbox(editwin)
        box.edit()

        file_path = box.gather().strip()  # Use gather to get the user-entered text
        try:
            filename = os.path.basename(file_path)
            new_path = os.path.join(analysis_folder, filename)
            os.rename(file_path, new_path)
            stdscr.addstr(y_options + 7, x_options - 8, f"The file {filename} has been added correctly!")
            stdscr.refresh()
            stdscr.getch()
            if stdscr.getch() == 27:
                break
        except FileNotFoundError:
            stdscr.addstr(y_options + 7, x_options - 8, "Error: The file was not found.")
            stdscr.refresh()
            stdscr.getch()
            if stdscr.getch() == 27:
                break
        except Exception as e:
            stdscr.addstr(y_options + 7, x_options - 8, f"Error: {str(e)}")
            stdscr.refresh()
            stdscr.getch()
            if stdscr.getch() == 27:
                break
    
    stdscr.clear()
    stdscr.refresh()

    welcome_message = " - WELCOME TO THE WORLDCUP PROJECT - "
    stdscr.addstr(y_title, x_title + 6, welcome_message, curses.A_BOLD)
    stdscr.addstr(y_title + 1, x_title + 2, " - DEVELOPED BY GABRIEL VAYÀ & MARC FALCÓN - ", curses.COLOR_RED)
    stdscr.addstr(y_title + 2, x_title + 2, " - --------------------------------------- - ")
    stdscr.addstr(y_title + 3, x_title + 3, "      --- DATA ANALYSIS BACKBONE ---    ")
    stdscr.refresh()

def execute_analasyis(stdscr, y_title, x_title, y_options, x_options):
    stdscr.clear()
    stdscr.refresh()
    main_path = dataBasesDir + 'main.py'
    while True:
        stdscr.addstr(y_title, x_title - 13, "Press Enter to execute the code or Esc to return to the Main menu", curses.A_BOLD)
        stdscr.addstr(y_title + 1, x_title - 14, "A message will appear when the code finalizes its execution! Wait :)")
        key = stdscr.getch()
        if key == ord('\n'):  # Enter key
            try:
                subprocess.run(['python3', main_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdscr.addstr(y_options + 2, x_options - 30, """CODE EXECUTED CORRECTLY! CHECK RESULTS IN EACH OF THE FOLDERS OF THE DIFFERENT ZONES""", curses.A_BOLD)
            except subprocess.CalledProcessError as e:
                stdscr.addstr(y_options + 2, x_options, f"Error: {e.stderr}")
                stdscr.refresh()
                stdscr.getch()
        elif key == 27:  # Check for the Esc key
            break

    stdscr.clear()
    stdscr.refresh()

    welcome_message = " - WELCOME TO THE WORLDCUP PROJECT - "
    stdscr.addstr(y_title, x_title + 6, welcome_message, curses.A_BOLD)
    stdscr.addstr(y_title + 1, x_title + 2, " - DEVELOPED BY GABRIEL VAYÀ & MARC FALCÓN - ", curses.COLOR_RED)
    stdscr.addstr(y_title + 2, x_title + 2, " - --------------------------------------- - ")
    stdscr.addstr(y_title + 3, x_title + 3, "      --- DATA ANALYSIS BACKBONE ---    ")
    stdscr.refresh()


def main(stdscr):
    # Initialize the curses library
    stdscr.clear()
    curses.curs_set(0)  # Hide the cursor
    stdscr.refresh()

    # Enable cbreak mode for text input
    curses.cbreak()

    # Get the size of the terminal window
    max_y, max_x = stdscr.getmaxyx()

    # Configure colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Folder for analysis
    analysis_folder = predictions_folder

    if not os.path.exists(analysis_folder):
        os.makedirs(analysis_folder)

    # Welcome message
    welcome_message = " - WELCOME TO THE WORLDCUP PROJECT - "

    # Calculate the center position for the welcome message
    y_title = max_y // 2
    x_title = (max_x - len(welcome_message)) // 2

    stdscr.addstr(y_title, x_title + 6, welcome_message, curses.A_BOLD)
    stdscr.addstr(y_title + 1, x_title + 2, " - DEVELOPED BY GABRIEL VAYÀ & MARC FALCÓN - ", curses.COLOR_RED)
    stdscr.addstr(y_title + 2, x_title + 2, " - --------------------------------------- - ")
    stdscr.addstr(y_title + 3, x_title + 3, "      --- DATA ANALYSIS BACKBONE ---    ")
    stdscr.refresh()

    while True:
        # Calculate center position for options
        y_options = y_title + 4  # Adjust the vertical position
        x_options = (max_x - 22) // 2

        # Show options
        stdscr.addstr(y_options + 2, x_options, "[ 1. Add a new file for prediction ]", curses.A_BOLD)
        stdscr.addstr(y_options + 4, x_options + 6, "[ 2. Execute analysis ]", curses.A_BOLD)
        stdscr.addstr(y_options + 6, x_options + 5, "[ 3. Execute predictions ]", curses.A_BOLD)
        stdscr.addstr(y_options + 8, x_options + 6, "[ 4. Quit application ]")
        stdscr.refresh()

        # Wait for user input
        key = stdscr.getch()

        # Handle user input
        if key == ord('1'):
            add_file(stdscr, analysis_folder, y_title, x_title, y_options, x_options)

        if key == ord('2'):
            execute_analasyis(stdscr, y_title, x_title, y_options, x_options)
            
        if key == ord('3'):
            predictions(stdscr, y_title, x_title, y_options, x_options)

        elif key == ord('4'):
            break

if __name__ == "__main__":
    curses.wrapper(main)

