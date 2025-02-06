# Class for opening, saving and saving as for plain text files.
# Also handles choosing a directory and the creation of blank files.

from pathlib import Path
from datetime import datetime
import os


class FileManager:
    def __init__(self, filepath):
        # Set the filepath and create the directories if needed
        self.filepath = Path.cwd() / filepath
        self.filepath.mkdir(parents=True, exist_ok=True)
        os.chmod(self.filepath, 0o775)  # Update permissions on Linux for Read/Write access for all users
        self.filename = ""

    def set_filename(self, filename):
        '''update the current filename'''
        self.filename = filename

        # If the file doesn't exist already then create it and update permissions.
        self.append_file(data="", overwrite=False)
        self.update_file_permissions()

    def get_fullpath(self):
        '''Returns fullpath from filepath and filename'''
        return self.filepath / self.filename

    def generate_daily_filename(self):
        '''generate filename for daily note file'''
        return datetime.now().date().strftime("%Y-%m-%d") + ".txt"

    def generate_timestamp(self):
        '''Generate a timestamp, e.g. 21:23:08'''
        return datetime.now().time().strftime("%H:%M:%S")

    def append_file(self, data, overwrite):
        '''Add to the end of the file'''
        file_access = "w" if overwrite else "a"
        with open(self.filepath / self.filename, file_access, encoding='utf-8') as f:
            f.write(data)

    def load_file(self):
        '''return the current file contents'''
        with open(self.get_fullpath(), "r", encoding="utf-8") as f:
            file_data = f.read()
        return file_data

    def update_file_permissions(self):
        '''update file permissions on Linux so file can be opened by
           other users. Keyboard module has to be used as root so this
           is the workaround...'''
        os.chmod(self.get_fullpath(), 0o666)
