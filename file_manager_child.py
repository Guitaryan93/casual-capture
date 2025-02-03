# Class for opening, saving and saving as for plain text files.
# Also handles choosing a directory and the creation of blank files.

from pathlib import Path, PosixPath, WindowsPath
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory

# Determine correct base class based on OS
BasePath = WindowsPath if os.name == "nt" else PosixPath

class FileManager(BasePath):
    def __init__(self, filepath):
        __super__.__init__()
        self.filepath = Path.cwd() / filepath   # Full filepath and filename

    def set_filepath(self, filepath):
        '''Update current absolute filepath'''
        self.filepath = Path(filepath).resolve()

    def get_filepath(self):
        '''Returns the full filepath for the current file saved in the object properties'''
        return self.filepath

    def create_file(self, filepath):
        '''Check if a file exists. If it doesn't then create it'''
        new_file = Path(filepath).resolve()
        if not new_file.exists():
            new_file.write_text("")

    def open(self, filepath=""):
        '''Open a file and return it's contents'''
        # Check filepath exists and use Open File Dialog if needed
        if filepath == "" or not os.path.exists(filepath):
            filepath = askopenfilename()

        # Check if the filepath is valid and open the file
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                file_contents = f.read()

            self.set_filepath(filepath)
            return file_contents
        
    def save(self, file_content, filepath="", save_dialog=False):
        '''Save file, ask for save location if not specified'''
        if save_dialog or filepath == "" or not os.path.exists(filepath):
            filepath = self.save_as()

        if filepath != "":
            with open(filepath, "w") as f:
                f.write(file_content)

            self.set_filepath(filepath)

    def save_as(self):
        '''Open SaveAs dialog and get user to choose a filepath'''
        filepath = asksaveasfilename()
        return filepath

    def select_directory(self):
        return askdirectory()
        
