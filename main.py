# Python GUI that can be called upon at any time in order to save ideas, links, images (maybe), 
# to a file saved in a vault. Each day a new file is made and the user then has a living journal
# following them around when they need it.
#
# Organization can be done with tags on paragraphs that are sorted into topic files saved under
# the same name as the tags.

# MUST INCLUDE A SETTINGS SCREEN!!!
# Or at least a settings/config file in JSON or YAML or something...
#
# Settings:
# - Set directory where notes are saved -- NOPE. We are now going for a portable executable, so save to relative directory instead.
# - Set format of the saved daily notes, e.g. YYYY-MM-DD.txt -- Maybe...
# - Choose whether timestamps should be added or not
# - Decide how long between timestamps, e.g. 5 mins, 10 mins, etc...
#   to stop from spamming them in the daily files
# - Choose whether to auto add horizontal rule before each new file write
# - Choose which hotkey to bind the program to

# WE CAN ADD IMAGES TO OUR TEXT WIDGET?!?!?!?!?!?!?!??!!?!?!
# Now we need to add a little reference in the file to show where
# the image should be added when the file is opened for viewing.
# Could we make this a markdown style image reference so it is
# compatible with markdown files? Like ![[path/to/image/here.png]]
# Then the init of the Text widget, or the loading from the FileManager
# will look for these and use them to pull the images into the Text
# widget or something?!?!? This is AWESOME!!!!!!

from tkinter import *
from tkinter import ttk
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
        self.geometry("500x400")
        keyboard.add_hotkey("ctrl+alt+n", self.show_hide_window)  # Set up a global hotkey to unwithdraw the window

        # Set the default directory and filename for saving the files. Make the directories if necessary
        self.files_dir = Path.cwd() / "CasualCapture"
        self.files_dir.mkdir(parents=True, exist_ok=True)
        self.image_dir = self.files_dir / "assets"
        self.image_dir.mkdir(parents=True, exist_ok=True)

        # Open/Create the file for today
        self.todays_file = datetime.now().date().strftime("%Y-%m-%d") + ".txt"
        self.current_filepath = self.files_dir / self.todays_file
        if not self.current_filepath.exists():
            self.current_filepath.write_text("")

        # Setup timestamp preferences
        self.timestamp = ""
        self.add_timestamps = True
        self.timestamp_interval = 10

        # File Manager class handles creating, opening and saving of files
        self.fm = FileManager()
        self.fm.create_file(self.current_filepath)

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
            self.notes_input.focus()


    def append_file(self):
        '''Open the day's file, append the Text widget data, then save the file'''
        new_text = ""
        todays_file = self.fm.open(self.current_filepath)

        # Check to see if timestamp is needed
        #if self.add_timestamps and self.compare_timestamps() > self.timestamp_interval:
        #    new_text = self.generate_timestamp + "\n"

        # Add this for TESTING ONLY **************
        new_text = "\n" + self.generate_timestamp() + "\n"
        
        new_text += self.notes_input.get_text_content()

        # As long as the text is not blank or just a timestamp we will append it
        if new_text != "\n" and new_text != "" and new_text != self.timestamp + "\n":
            todays_file += new_text
            self.fm.save(todays_file, self.current_filepath, save_dialog=False)

        # Clear the Text widget contents ready for the next note
        self.notes_input.clear()
        
    def generate_timestamp(self):
        '''Generate a timestamp, e.g. 21:23:08'''
        self.timestamp = datetime.now().time().strftime("%H:%M:%S")
        return self.timestamp

    def compare_timestamps(self):
        '''Compare how much time has passed between now and the previously
           saved self.timestamp. Used to decide when to add a timestamp
           to the daily file (to avoid spamming with timestamps)'''
        time1_str = datetime.now().time().strftime("%H:%M:%S")
        if self.timestamp != "":
            time2_str = self.timestamp
        else:
            time2_str = time1_str
        
        time1 = datetime.strptime(time1_str, "%H:%M:%S").time()
        time2 = datetime.strptime(time2_str, "%H:%M:%S").time()

        # Need to subtract time2 from time1 to get difference, but this
        # needs more research into HOW in Python...
    

class NotesInput(Text):
    '''Text widget child class -- This ONLY handles things related to the
       text input and Text widget data'''
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.wrap = "word"
        self.hr_string = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"

        # Use this to store pasted images in.
        # There's probably a better way to separate this and the image
        # saving process into a different class, but this will do for now...
        self.img_dir = "C:\\Users\\ryanw\\Documents\\Python_Scripts\\casual_capture\\casual_capture_notes\\assets"

        # Store references to the image objects here to avoid them being
        # garbage collected by mistake...
        self.image_list = []
        
        # Hotkeys
        keyboard.add_hotkey("ctrl+alt+-", self.insert_hr)
        self.bind("<Control-v>", self.handle_paste)

    def get_text_content(self):
        '''Return all text from inside the Text widget'''
        return self.get("1.0", "end")

    def clear(self):
        self.delete("1.0", "end")

    def insert_hr(self):
        self.insert("insert", self.hr_string)

    def handle_paste(self, event):
        '''Handle paste manually so we can account for images being
           pasted into the Text widget'''
        image = grabclipboard()

        if image:
            try:
                # Save the image to default location
                image_filename = datetime.now().time().strftime("%H%M%S") + ".png"
                image_fullpath = os.path.join(self.img_dir, image_filename)
                image.save(image_fullpath, "PNG")

                # Open image with PIL
                pil_image = Image.open(image_fullpath)

                # Convert to Tkinter compatible image
                #tk_image = ImageTk.PhotoImage(pil_image.convert("RGB"))  # Convert to "RGB" i.e. GIF format
                tk_image = ImageTk.PhotoImage(pil_image)

                # Store a reference to the image to avoid it being garbage collected
                self.image_list.append(tk_image)

                # Insert the image into Text widget
                self.image_create("insert", image=tk_image)

                # Prevent default Ctrl-v behaviour
                return "break"
            except Exception as e:
                messagebox.showerror("Error", f"Failed to handle image: {e}")
        else:
            # If no image is available then try pasting text into the widget
            self.insert("insert", pyperclip.paste())

        return "break"


if __name__ == "__main__":
    app = App()
    app.mainloop()

