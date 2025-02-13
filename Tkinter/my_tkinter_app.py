import tkinter as tk
from tkinter import ttk

# Function to add the text from the entry widget to the listbox
def add_to_list(event=None):
    text = entry.get()  # Get the text from the entry widget
    if text:  # Check if the entry is not empty
        text_list.insert(tk.END, text)  # Insert the text at the end of the listbox
        entry.delete(0, tk.END)  # Clear the entry widget

# Initialize the main application window
root = tk.Tk()
root.title("Simple App")

# Configure the main window's grid to adjust with window resizing
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a frame to hold the entry, button, and listbox
frame = ttk.Frame(root, padding=5)
frame.grid(row=0, column=0, sticky="nsew")

# Configure the frame's grid to adjust with window resizing
frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)

# Create an entry widget for user input
entry = ttk.Entry(frame)
entry.grid(row=0, column=0, sticky="ew")
entry.bind("<Return>", add_to_list)  # Bind the Enter key to the add_to_list function

# Create a button to add the entry text to the listbox
entry_btn = ttk.Button(frame, text="Add", command=add_to_list)
entry_btn.grid(row=0, column=1, padx=(5, 0))  # Add horizontal padding between entry and button

# Create a listbox to display the added items
text_list = tk.Listbox(frame)
text_list.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(5, 0))

# Start the Tkinter event loop
root.mainloop()
