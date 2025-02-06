# Settings and SettingsWindow classes. Used to load, store, and save settings.

from tkinter import *
from tkinter import ttk, font
import json

class Settings:
    '''Settings object that loads data from the settings.json file.
       - This object is created by the main app on startup 
       - It is refreshed when the settings.json file is updated from 
         saving the SettingsWindow changes
       - It is also passed to the SettingsWindow to set the defaults for
         that objects GUI.'''
    def __init__(self, filepath):
        self.filepath = filepath
        self.settings = self.load_settings()

    def assign_settings(self):
        '''set the properties of the object based on the settings data'''
        self.dark_mode = self.settings["dark_mode"]
        self.insert_timestamps = self.settings["insert_timestamps"]
        self.add_horizontal_rule = self.settings["add_horizontal_rule"]
        self.app_position = self.settings["app_position"]
        self.win_width = self.settings["win_width"]
        self.win_height = self.settings["win_height"]
        self.font_choice = self.settings["font_choice"]
        self.font_size = self.settings["font_size"]
        self.hr_char = self.settings["hr_char"]
        self.hotkey = self.settings["hotkey"]
        self.word_wrap = self.settings["word_wrap"]

    def update_settings(self):
        '''build Python dict from settings to save as JSON'''
        self.settings = {"dark_mode": self.dark_mode,
                         "insert_timestamps": self.insert_timestamps,
                         "add_horizontal_rule": self.add_horizontal_rule,
                         "app_position": self.app_position,
                         "win_width": self.win_width,
                         "win_height": self.win_height,
                         "font_choice": self.font_choice,
                         "font_size": self.font_size,
                         "hr_char": self.hr_char,
                         "hotkey": self.hotkey,
                         "word_wrap": self.word_wrap
                         }

    def load_settings(self):
        '''load data from settings.json'''
        with open(self.filepath, "r") as f:
            self.settings = json.load(f)
        self.assign_settings()

    def save_settings(self):
        '''save data to settings.json'''
        with open(self.filepath, "w") as f:
            json.dump(self.settings, f)


class SettingsWindow(Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("300x500")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.focus()
        
        # Settings object data stored here
        self.data = data

        # Setting initial options
        self.dark_mode = BooleanVar(value=self.data.dark_mode)
        self.insert_timestamps = BooleanVar(value=self.data.insert_timestamps)
        self.add_horizontal_rule = BooleanVar(value=self.data.add_horizontal_rule)
        self.app_position = StringVar(value=self.data.app_position)
        self.win_width = IntVar(value=self.data.win_width)
        self.win_height = IntVar(value=self.data.win_height)
        self.font_choice = StringVar(value=self.data.font_choice)
        self.font_size = IntVar(value=self.data.font_size)
        self.hr_char = StringVar(value=self.data.hr_char)
        self.hotkey = StringVar(value=self.data.hotkey)
        self.word_wrap = BooleanVar(value=self.data.word_wrap)

        # Dark/Light mode toggle
        ttk.Checkbutton(self, text="Dark Mode", variable=self.dark_mode).pack(anchor="w", padx=10, pady=5)

        # Timestamp options
        ttk.Checkbutton(self, text="Insert Timestamps", variable=self.insert_timestamps).pack(anchor="w", padx=10, pady=5)
        ttk.Checkbutton(self, text="Add Horizontal Rule", variable=self.add_horizontal_rule).pack(anchor="w", padx=10, pady=5)

        # Window popup position
        ttk.Label(self, text="Window Position:").pack(anchor="w", padx=10, pady=5)
        positions = ["top left", "top right", "bottom left", "bottom right", "center", "at mouse pointer"]
        position_index = positions.index(self.app_position.get())
        position_menu = ttk.OptionMenu(self, self.app_position, positions[position_index], *positions)
        position_menu.pack(anchor="w", padx=10)

        # Window dimensions
        ttk.Label(self, text="Window Width:").pack(anchor="w", padx=10)
        ttk.Entry(self, textvariable=self.win_width).pack(anchor="w", padx=10)

        ttk.Label(self, text="Window Height:").pack(anchor="w", padx=10)
        ttk.Entry(self, textvariable=self.win_height).pack(anchor="w", padx=10)

        # Font choice
        ttk.Label(self, text="Font Choice:").pack(anchor="w", padx=10)
        available_fonts = list(font.families())
        font_menu = ttk.Combobox(self, textvariable=self.font_choice, values=available_fonts)
        font_menu.pack(anchor="w", padx=10)

        # Font size input
        ttk.Label(self, text="Font Size:").pack(anchor="w", padx=10)
        ttk.Entry(self, textvariable=self.font_size).pack(anchor="w", padx=10)
        
        # word wrap preference
        ttk.Checkbutton(self, text="Word Wrap", variable=self.word_wrap).pack(anchor="w", padx=10, pady=5)

        # Single character input for Horizontal Rule
        ttk.Label(self, text="Horizontal Rule Character:").pack(anchor="w", padx=10)
        hr_char_entry = ttk.Entry(self, textvariable=self.hr_char, width=3)
        hr_char_entry.pack(anchor="w", padx=10)

        # Hotkey used to minimize/iconify the UI
        ttk.Label(self, text="Popup Hotkey:").pack(anchor="w", padx=10)
        hotkey_entry = ttk.Entry(self, textvariable=self.hotkey, width=16)
        hotkey_entry.pack(anchor="w", padx=10)
        default_hotkey_button = ttk.Button(self, text="Reset Default Hotkey", command=self.default_hotkey)
        default_hotkey_button.pack(anchor="w", padx=10)

        # Save and Cancel buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        save_button = ttk.Button(button_frame, text="Save", command=self.save_settings)
        save_button.grid(row=0, column=0, padx=5)
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.grid(row=0, column=1, padx=5)

    def default_hotkey(self):
        '''restore default hotkey just in case!'''
        self.hotkey.set("ctrl+alt+n")

    def save_settings(self):
        '''Updates the settings and destroys the window.'''
        self.data.dark_mode = self.dark_mode.get()
        self.data.insert_timestamps = self.insert_timestamps.get()
        self.data.add_horizontal_rule = self.add_horizontal_rule.get()
        self.data.app_position = self.app_position.get()
        self.data.win_width = self.win_width.get()
        self.data.win_height = self.win_height.get()
        self.data.font_choice = self.font_choice.get()
        self.data.font_size = self.font_size.get()
        self.data.hr_char = self.hr_char.get()
        self.data.hotkey = self.hotkey.get()
        self.data.word_wrap = self.word_wrap.get()
        self.data.update_settings()
        self.data.save_settings()
        self.data.load_settings()
        self.destroy()
