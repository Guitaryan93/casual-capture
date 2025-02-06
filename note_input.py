# Text widget child class -- This ONLY handles things related to the
# text input and Text widget data

from tkinter import Text
from tkinter.font import Font

class NotesInput(Text):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Set font
        font = Font(family="courier", size=11)
        tab_size = font.measure("    ")

        # Set configurations for Text widget
        self.config(font=font)
        self.config(padx=7, pady=5)
        self.config(undo=True)
        self.config(tabs=(tab_size,))

        self.hr_string = ("-" * 80) + "\n"

        # Hotkeys
        #keyboard.add_hotkey("ctrl+alt+-", self.insert_hr)
        self.bind("<Control-Alt-minus>", self.insert_hr)
        self.bind("<Control-BackSpace>", self.delete_word_backward)
        self.bind("<Control-Delete>", self.delete_word_forward)

    def get_text_content(self):
        '''Return all text from inside the Text widget'''
        return self.get("1.0", "end")

    def clear(self):
        self.delete("1.0", "end")

    def insert_hr(self, event):
        self.insert("insert", self.hr_string)

    def delete_word_backward(self, event):
        ''' *** THIS NEEDS WORK *** '''
        self.delete("insert wordstart", "insert")

    def delete_word_forward(self, event):
        self.delete("insert", "insert wordend")

    def toggle_dark_mode(self, dark_mode):
        if dark_mode:
            self.config(bg="#111111", fg="white", insertbackground="white")
        else:
            self.config(bg="white", fg="black", insertbackground="black")

    def set_font(self, font_choice, font_size):
        self.config(font=(font_choice, font_size))
