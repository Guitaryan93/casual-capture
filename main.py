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
        

class NotesInput(Text):
    '''Text widget child class -- This ONLY handles things related to the
       text input and Text widget data'''
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Set font
        font = Font(family="courier", size=11)
        tab_size = font.measure("    ")

        # Set configurations for Text widget
        self.config(font=font)
        self.config(wrap="word")
        self.config(padx=5, pady=5)
        self.config(undo=True)
        self.config(tabs=(tab_size,))

        self.hr_string = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        self.fm_images = FileManager("CasualCapture/assets")

        # Store references to the image objects here to avoid them being
        # garbage collected by mistake...
        self.image_list = []
        
        # Hotkeys
        keyboard.add_hotkey("ctrl+alt+-", self.insert_hr)
        self.bind("<Control-v>", self.handle_paste)
        self.bind("<Shift-Insert>", self.handle_paste)
        self.bind("<Control-BackSpace>", self.delete_word_backward)
        self.bind("<Control-Delete>", self.delete_word_forward)

    def get_text_content(self):
        '''Return all text from inside the Text widget'''
        return self.get("1.0", "end")

    def clear(self):
        self.delete("1.0", "end")

    def insert_hr(self):
        self.insert("insert", self.hr_string)

    def delete_word_backward(self, event):
        ''' *** THIS NEEDS WORK *** '''
        self.delete("insert wordstart", "insert")

    def delete_word_forward(self, event):
        self.delete("insert", "insert wordend")

    def handle_paste(self, event):
        '''Handle paste manually so we can account for images being
           pasted into the Text widget'''
        image = grabclipboard()

        if image:
            try:
                # Save the image to default location
                image_filename = datetime.now().time().strftime("%H%M%S") + ".png"
                self.fm_images.set_filename(image_filename)
                image.save(self.fm_images.get_fullpath(), "PNG")

                # Open image with PIL
                pil_image = Image.open(self.fm_images.get_fullpath())

                # Convert to Tkinter compatible image
                tk_image = ImageTk.PhotoImage(pil_image)

                # Store a reference to the image to avoid it being garbage collected
                self.image_list.append(tk_image)

                # Insert a Markdown style reference to the image into the Text widget
                # similar to how Obsidian behaves
                self.tag_config("hidden", elide=True)
                self.insert("insert", f"![{self.fm_images.filename}]({self.fm_images.get_fullpath()})")
                self.tag_add("hidden", "insert linestart", "insert lineend")

                # Insert the image into Text widget
                self.image_create("insert", image=tk_image)
                self.insert("insert", "\n")  # Add a newline to place cursor under the image

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

