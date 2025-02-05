import tkinter as tk

def show_settings():
    print("Settings clicked!")

    root = tk.Tk()
    root.geometry("400x300")

    # Frame to contain the Text widget and floating button
    container = tk.Frame(root)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Create the Text widget
    text_widget = tk.Text(container, wrap="word")
    text_widget.pack(fill="both", expand=True)

    # Create the floating button
    settings_button = tk.Button(container, text="⚙", command=show_settings, cursor="hand2")

    # Position the button in the top-right corner
    settings_button.place(in_=text_widget, relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")

    root.mainloop()
    
show_settings()
