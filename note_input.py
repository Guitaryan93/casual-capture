# Text widget child class -- This ONLY handles things related to the
# text input and Text widget data

class NotesInput(Text):
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
