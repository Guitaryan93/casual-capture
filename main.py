# Python GUI that can be called upon at any time in order to save ideas, links, any text really
# to a file saved in a vault. Each day a new file is made and the user then has a living journal
# following them around when they need it.
#
# Organization can be done with tags on paragraphs that are sorted into topic files saved under
# the same name as the tags.

# MUST INCLUDE A SETTINGS SCREEN!!!
# Or at least a settings/config file in JSON or YAML or something...
#
# Settings:
# - light and dark mode (of course)
# - choice of 2 or 3 fonts
# - font size
# - Set window size
# - Set window popup location - top left | top right | bottom left | bottom right | center | at mouse cursor
# - Choose whether timestamps should be added or not
# - Choose whether to auto add horizontal rule before each new file write
# - Choose which hotkey to bind the program to

from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
from tkinter import PhotoImage
from file_manager import FileManager
import keyboard
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageTk
from PIL.ImageGrab import grabclipboard
import pyperclip


class App(Tk):
    def __init__(self):
        super().__init__()
        #self.geometry("500x400")
        self.attributes("-topmost", True)
        keyboard.add_hotkey("ctrl+alt+n", self.show_hide_window)  # Set up a global hotkey to unwithdraw the window

        # Set the default directory and filename for saving note files. Make the directories if necessary
        self.fm_notes = FileManager("CasualCapture")
        
        # Open/Create the file for today
        self.fm_notes.set_filename(self.fm_notes.generate_daily_filename())

        # Text widget and scrollbar setup
        self.notes_frame = Frame(self)
        self.notes_input = NotesInput(self.notes_frame)
        self.notes_scrollbar = ttk.Scrollbar(self.notes_frame, orient="vertical", command=self.notes_input.yview)
        self.notes_input["yscrollcommand"] = self.notes_scrollbar.set

        # Geometry management
        self.notes_input.grid(column=0, row=0, sticky="nesw")
        self.notes_scrollbar.grid(column=1, row=0, sticky="nesw")
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        
        self.notes_frame.grid(column=0, row=0, sticky="nesw")

        self.notes_input.focus()
        
    
    def show_hide_window(self):
        '''Show/hide the program window. When hiding the window append the text
           to todays file'''
        if self.state() == "normal":
            self.withdraw()
            self.append_file()
        else:
            self.deiconify()
            self.focus()              # Focus program window first to grab focus from current program
            self.notes_input.focus()  # Move focus to the Text widget now that this program is in focus


    def append_file(self):
        '''Open the day's file, append the Text widget data, then save the file'''
        text_data = f"\n{self.fm_notes.generate_timestamp()}\n{self.notes_input.get_text_content()}" 

        self.fm_notes.append_file(text_data)

        # Clear the Text widget contents ready for the next note
        self.notes_input.clear()
        

if __name__ == "__main__":
    app = App()
    app.mainloop()

