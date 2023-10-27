import curses
import os
import shutil
import subprocess

from curses.textpad import Textbox, rectangle
from paths import temporalPath, dataBasesDir

def add_file(stdscr, analysis_folder, y_title, x_title, y_options, x_options):
    stdscr.clear()
    stdscr.addstr(y_title, x_title - 6, "Enter the path of the file you want to add")
    stdscr.addstr(y_title + 10, x_title - 2, "[ Esc to return to the main menu ]")
    stdscr.addstr(y_title + 1, x_title - 8, "Be careful with the '/' before the inital path")
    rectangle(stdscr, y_title + 2, x_title - 25, y_title + 4, x_title + 70)
    stdscr.refresh()


    while True:
        key = stdscr.getch()
        if key == "":
            continue
        elif key == 27:
            break
        editwin = curses.newwin(1, 100, y_title + 3, x_title - 9)
        stdscr.refresh()

        box = Textbox(editwin)
        box.edit()

        file_path = box.gather().strip()  # Use gather to get the user-entered text
        try:
            filename = os.path.basename(file_path)
            new_path = os.path.join(analysis_folder, filename)
            os.rename(file_path, new_path)
            stdscr.addstr(y_options + 2, x_options - 10, f"The file {filename} has been added correctly!")
            stdscr.refresh()
            stdscr.getch()
            if stdscr.getch() == 27:
                break
        except FileNotFoundError:
            stdscr.addstr(y_options + 2, x_options - 10, "Error: The file was not found.")
            stdscr.refresh()
            stdscr.getch()
            if stdscr.getch() == 27:
                break
        except Exception as e:
            stdscr.addstr(y_options + 2, x_options - 10, f"Error: {str(e)}")
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
    stdscr.addstr(y_title + 3, x_title + 3, "      --- DATA MANAGEMENT BACKBONE ---    ")
    stdscr.refresh()

def execute_analasyis(stdscr, y_title, x_title, y_options, x_options):
    stdscr.clear()
    stdscr.refresh()
    main_path = dataBasesDir + 'main.py'
    while True:
        stdscr.addstr(y_title, x_title - 13, "Press Enter to execute the code or Esc to return to the main menu")
        key = stdscr.getch()
        if key == ord('\n'):  # Enter key
            try:
                subprocess.run(['python3', main_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdscr.addstr(y_options + 2, x_options, "Code executed successfully!")
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
    stdscr.addstr(y_title + 3, x_title + 3, "      --- DATA MANAGEMENT BACKBONE ---    ")
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
    analysis_folder = temporalPath

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
    stdscr.addstr(y_title + 3, x_title + 3, "      --- DATA MANAGEMENT BACKBONE ---    ")
    stdscr.refresh()

    while True:
        # Calculate center position for options
        y_options = y_title + 4  # Adjust the vertical position
        x_options = (max_x - 22) // 2

        # Show options
        stdscr.addstr(y_options + 2, x_options + 1, "[ Add a new file for analysis ]", curses.A_BOLD)
        stdscr.addstr(y_options + 4, x_options + 7, "[ Execute analysis ]", curses.A_BOLD)
        stdscr.addstr(y_options + 6, x_options + 7, "[ Quit application ]")
        stdscr.refresh()

        # Wait for user input
        key = stdscr.getch()

        # Handle user input
        if key == ord('1'):
            add_file(stdscr, analysis_folder, y_title, x_title, y_options, x_options)

        if key == ord('2'):
            execute_analasyis(stdscr, y_title, x_title, y_options, x_options)

        elif key == ord('3'):
            break

if __name__ == "__main__":
    curses.wrapper(main)

