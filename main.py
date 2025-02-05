# Python GUI that can be called upon at any time in order to save ideas, links, any text really
# to a file saved in a vault. Each day a new file is made and the user then has a living journal
# following them around when they need it.

# MUST INCLUDE A SETTINGS SCREEN!!!
# Or at least a settings/config file in JSON or YAML or something...
#
# Settings:
# - light and dark mode (of course)
# - choice of 2 or 3 fonts
# - font size
# - Choose character for horizontal rules
# - Set window size
# - Set window popup location - top left | top right | bottom left | bottom right | center | at mouse cursor
# - Choose whether timestamps should be added or not
# - Choose whether to auto add horizontal rule before each new file write
# - Choose which hotkey to bind the program to

from tkinter import *
from tkinter import ttk, font
from file_manager import FileManager
from note_input import NotesInput
import keyboard


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

        # Create Text widget and frame
        self.notes_frame = Frame(self)
        self.notes_input = NotesInput(self.notes_frame)

        # Settings Button widget -- This lives inside the Text widget, bottom right corner
        self.settings_btn = Button(self.notes_frame, text="⚙", cursor="hand2", command=self.show_settings)
        self.settings_btn.configure(width=2, height=1, padx=0, pady=0, font=("Arial", 8), relief="flat", bd=0)

        # Geometry management
        self.notes_frame.pack(fill="both", expand=True)
        self.notes_input.pack(fill="both", expand=True)
        self.settings_btn.place(in_=self.notes_input, relx=1.0, rely=1.0, anchor="se")

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
        text_data = f"{self.fm_notes.generate_timestamp()}\n{self.notes_input.get_text_content()}\n" 

        self.fm_notes.append_file(text_data)

        # Clear the Text widget contents ready for the next note
        self.notes_input.clear()

    def show_settings(self):
        '''Show the settings toplevel UI'''
        SettingsWindow(self)


class SettingsWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("300x400")
        self.resizable(False, False)

        # Setting initial options
        self.dark_mode = BooleanVar(value=False)
        self.insert_timestamps = BooleanVar(value=False)
        self.add_horizontal_rule = BooleanVar(value=False)
        self.app_position = StringVar(value="center")
        self.width = IntVar(value=400)
        self.height = IntVar(value=300)
        self.font_choice = StringVar(value="Arial")
        self.font_size = IntVar(value=12)
        self.hr_char = StringVar(value="-")

        ttk.Checkbutton(self, text="Dark Mode", variable=self.dark_mode).pack(anchor="w", padx=10, pady=5)

        ttk.Checkbutton(self, text="Insert Timestamps", variable=self.insert_timestamps).pack(anchor="w", padx=10, pady=5)
        ttk.Checkbutton(self, text="Add Horizontal Rule", variable=self.add_horizontal_rule).pack(anchor="w", padx=10, pady=5)

        ttk.Label(self, text="App Position:").pack(anchor="w", padx=10, pady=5)
        positions = ["top left", "top right", "bottom left", "bottom right", "center", "at mouse pointer"]
        position_menu = ttk.OptionMenu(self, self.app_position, positions[4], *positions)
        position_menu.pack(anchor="w", padx=10)

        ttk.Label(self, text="Window Width:").pack(anchor="w", padx=10)
        ttk.Entry(self, textvariable=self.width).pack(anchor="w", padx=10)

        ttk.Label(self, text="Window Height:").pack(anchor="w", padx=10)
        ttk.Entry(self, textvariable=self.height).pack(anchor="w", padx=10)

        ttk.Label(self, text="Font Choice:").pack(anchor="w", padx=10)
        available_fonts = list(font.families())
        font_menu = ttk.Combobox(self, textvariable=self.font_choice, values=available_fonts)
        font_menu.pack(anchor="w", padx=10)

        # Font size input
        ttk.Label(self, text="Font Size:").pack(anchor="w", padx=10)
        ttk.Entry(self, textvariable=self.font_size).pack(anchor="w", padx=10)

        # Single character input for Horizontal Rule
        ttk.Label(self, text="Horizontal Rule Character:").pack(anchor="w", padx=10)
        hr_char_entry = ttk.Entry(self, textvariable=self.hr_char, width=3)
        hr_char_entry.pack(anchor="w", padx=10)

        # Save and Cancel buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        save_button = ttk.Button(button_frame, text="Save", command=self.save_settings)
        save_button.grid(row=0, column=0, padx=5)
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.grid(row=0, column=1, padx=5)

    def save_settings(self):
        """Prints the settings and destroys the window."""
        print("Settings Saved:")
        print(f"Dark Mode: {self.dark_mode.get()}")
        print(f"Insert Timestamps: {self.insert_timestamps.get()}")
        print(f"Add Horizontal Rule: {self.add_horizontal_rule.get()}")
        print(f"App Position: {self.app_position.get()}")
        print(f"Window Size: {self.width.get()}x{self.height.get()}")
        print(f"Font: {self.font_choice.get()} {self.font_size.get()}")
        print(f"Horizontal Rule Character: {self.hr_char.get()}")
        self.destroy()
        


if __name__ == "__main__":
    app = App()
    app.mainloop()

