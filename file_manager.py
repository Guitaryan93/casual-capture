# Class for opening, saving and saving as for plain text files.
# Also handles choosing a directory and the creation of blank files.

from pathlib import Path
from datetime import datetime
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory


class FileManager:
    def __init__(self, filepath):
        # Set the filepath and create the directories if needed
        self.filepath = Path.cwd() / filepath
        self.filepath.mkdir(parents=True, exist_ok=True)
        self.filename = ""

    def set_filepath(self, filepath):
        '''Update current absolute filepath'''
        self.filepath = Path(filepath).resolve()

    def get_filepath(self):
        '''Returns the full filepath for the current file saved in the object properties'''
        return self.filepath

    def get_fullpath(self):
        '''Returns fullpath from filepath and filename'''
        return self.filepath / self.filename

    def generate_daily_filename(self):
        '''generate filename for daily note file'''
        return datetime.now().date().strftime("%Y-%m-%d") + ".txt"

    def generate_timestamp(self):
        '''Generate a timestamp, e.g. 21:23:08'''
        return datetime.now().time().strftime("%H:%M:%S")

    def set_filename(self, filename):
        '''update the current filename'''
        self.filename = filename

    def create_file(self, filepath):
        '''Check if a file exists. If it doesn't then create it'''
        new_file = Path(filepath).resolve()
        if not new_file.exists():
            new_file.write_text("")

    def append_file(self, data):
        '''Add to the end of the file'''
        with open(self.filepath / self.filename, "a") as f:
            f.write(data)
