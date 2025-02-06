# Python GUI that can be called upon at any time in order to save ideas, links, any text really
# to a file saved in a vault. Each day a new file is made and the user then has a living journal
# following them around when they need it.

# Program Icon By -- Freepik
# https://www.flaticon.com/free-icons/concert

from tkinter import *
from file_manager import FileManager
from note_input import NotesInput
from settings_objects import Settings, SettingsWindow
import keyboard
from pathlib import Path


class App(Tk):
    def __init__(self):
        super().__init__()
        # Load the program settings
        self.settings = Settings("settings.json")

        # JANKY CODE ALERT!!!!
        if self.settings.app_position.lower() == "center":
            x_pos = (self.winfo_screenwidth() / 2) - (self.settings.win_width / 2)
            y_pos = (self.winfo_screenheight() / 2) - (self.settings.win_height / 2)
        else:
            screen_pos = self.settings.app_position.split(" ")
            x_offset = 30
            y_offset = 50
            if screen_pos[0].lower() == "bottom":
                y_pos = self.winfo_screenheight() - (self.settings.win_height + y_offset)
            else:
                y_pos = 0

            if screen_pos[1].lower() == "right":
                x_pos = self.winfo_screenwidth() - (self.settings.win_width + x_offset)
            else:
                x_pos = 0

        self.geometry(f"{self.settings.win_width}x{self.settings.win_height}+{int(x_pos)}+{int(y_pos)}")
        self.attributes("-topmost", True)
        self.title("Casual Capture")

        icon = PhotoImage(file="casual-capture-icon.png")
        self.iconphoto(True, icon)
        
        self.whole_feed = False  # Show whole file in Text widget

        keyboard.add_hotkey(self.settings.hotkey, self.show_hide_window)  # Set up a global hotkey to unwithdraw the window

        # Set the default directory and filename for saving note files. Make the directories if necessary
        self.fm_notes = FileManager("CasualCapture")
        
        # Open/Create the file for today
        self.fm_notes.set_filename(self.fm_notes.generate_daily_filename())

        # Create Text widget and frame
        self.notes_frame = Frame(self)
        self.notes_input = NotesInput(self.notes_frame)
        self.notes_input.toggle_dark_mode(self.settings.dark_mode)
        self.notes_input.set_font(self.settings.font_choice, self.settings.font_size)
        wrap_setting = "word" if self.settings.word_wrap else "none"
        self.notes_input.config(wrap=wrap_setting)

        self.btn_frame = Frame(self.notes_frame)
        # Match the frame background to the Text Widget background to hide it
        if self.settings.dark_mode:
            self.btn_frame.config(bg="#111111")
        else:
            self.btn_frame.config(bg="white")

        # Current file data button -- lives inside Text widget with Settings button
        self.feed_btn = Button(self.btn_frame, text="📰", cursor="hand2", command=self.insert_feed)
        self.feed_btn.configure(width=2, height=1, padx=0, pady=0, font=("Arial", 8), relief="flat", bd=0)

        # Settings Button widget -- This lives inside the Text widget, bottom right corner
        self.settings_btn = Button(self.btn_frame, text="⚙", cursor="hand2", command=self.show_settings)
        self.settings_btn.configure(width=2, height=1, padx=0, pady=0, font=("Arial", 8), relief="flat", bd=0)

        # Geometry management
        self.notes_frame.pack(fill="both", expand=True)
        self.notes_input.pack(fill="both", expand=True)

        # Pack the buttons into a frame and place the frame absolutely in the Text widget.
        self.btn_frame.place(in_=self.notes_input, relx=1.0, rely=1.0, anchor="se")
        #self.feed_btn.pack(fill="both", expand=True)
        #self.settings_btn.pack(fill="both", expand=True)
        self.feed_btn.pack(pady=5)
        self.settings_btn.pack()

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

    def insert_feed(self):
        '''insert the current file data into the Text widget'''
        if self.whole_feed == False:
            file_data = self.fm_notes.load_file()
            self.notes_input.insert("1.0", file_data)
            self.whole_feed = True
        else:
            self.append_file()
            self.whole_feed = False

    def append_file(self):
        '''Open the day's file, append the Text widget data, then save the file'''
        text_data = ""
        if self.settings.insert_timestamps and not self.whole_feed:
            text_data = f"{self.fm_notes.generate_timestamp()}"
            if self.settings.add_horizontal_rule:
                text_data += " " + (self.settings.hr_char * 60)
            text_data += "\n"
        
        text_data += f"{self.notes_input.get_text_content()}\n" 

        self.fm_notes.append_file(text_data, self.whole_feed)

        # Clear the Text widget contents ready for the next note
        self.notes_input.clear()

    def show_settings(self):
        '''Show the settings toplevel UI'''
        SettingsWindow(self, self.settings)


if __name__ == "__main__":
    app = App()
    app.mainloop()

