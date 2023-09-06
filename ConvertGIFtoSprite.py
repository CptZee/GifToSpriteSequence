# ------------------------------------------------------------------------------------------
# Copyright (C) 2023 Aaron James R. Mission
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------


import os
import tkinter as tk
from tkinter import filedialog, Toplevel, Label, PhotoImage
from PIL import Image, ImageTk

# ------------------------------------------------------------------------------------------
# $$___$$_ $$$$$$$_ $$______ __$$$$_ __$$$___ $$___$$_ $$$$$$$_ $$_
# $$___$$_ $$______ $$______ _$$____ _$$_$$__ $$$_$$$_ $$______ $$_
# $$_$_$$_ $$$$$___ $$______ $$_____ $$___$$_ $$$$$$$_ $$$$$___ $$_
# $$$$$$$_ $$______ $$______ $$_____ $$___$$_ $$_$_$$_ $$______ $$_
# $$$_$$$_ $$______ $$____$_ _$$____ _$$_$$__ $$___$$_ $$______ ___
# $$___$$_ $$$$$$$_ $$$$$$$_ __$$$$_ __$$$___ $$___$$_ $$$$$$$_ $$_
# ------------------------------------------------------------------------------------------

def main():
    global output_folder
    global root
    global img_label
    global output_folder_label
    global convert_button
    output_folder = None
    root = tk.Tk()
    root.title("GIF to Sprite Sequence Converter | CptZ")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (600 // 2)
    root.geometry(f'400x600+{x}+{y}')

    img_label = Label(root, bg='grey')
    img_label.grid(row=0, column=0, columnspan=2, pady=20, sticky='nsew')

    open_file_button = tk.Button(root, text="Open GIF", command=open_file_dialog)
    open_file_button.grid(row=1, column=0, pady=20, padx=50, sticky='ew')

    select_folder_button = tk.Button(root, text="Select Output Folder", command=select_output_folder)
    select_folder_button.grid(row=1, column=1, pady=20, padx=50, sticky='ew')

    output_folder_label = Label(root, text="Output Folder: Not Selected", bg='red') 
    output_folder_label.grid(row=3, column=0, columnspan=2, pady=20, sticky='nsew')

    convert_button = tk.Button(root, text="Convert", command=convert_gif, bg='red', state=tk.DISABLED)
    convert_button.grid(row=2, column=0, columnspan=2, pady=20, sticky='nsew')

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    root.mainloop()


dialog_open = tk.BooleanVar(value=True)
def on_dialog_close():
    dialog_open.set(False)
def gif_to_sprite_sequence(gif_path, output_folder):
    global loading_dialog
    image = Image.open(gif_path)
    frame_number = 0

    loading_dialog = Toplevel(root)
    loading_dialog.title("Processing")
    loading_dialog.transient(root)
    loading_dialog.grab_set() 
    Label(loading_dialog, text="Converting GIF to Sprite Sequence...").pack()

    root_x, root_y = root.winfo_x(), root.winfo_y()
    root_width, root_height = root.winfo_width(), root.winfo_height()

    # Update the loading_dialog window before calculating its dimensions
    loading_dialog.update()

    # Get the loading_dialog window's dimensions
    dialog_width = loading_dialog.winfo_width()
    dialog_height = loading_dialog.winfo_height()

    # Calculate position to center loading_dialog within root
    x = root_x + (root_width // 2) - (dialog_width // 2)
    y = root_y + (root_height // 2) - (dialog_height // 2)

    # Set the loading_dialog's position
    loading_dialog.geometry(f'+{x}+{y}')

    loading_dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)

    while image and dialog_open.get():
        image.save(os.path.join(output_folder, f"frame_{frame_number}.png"))
        
        frame_number += 1
        try:
            image.seek(frame_number)
        except EOFError:
            show_success_message()
            break
        root.update_idletasks()
        root.update()

def show_success_message():
    for widget in loading_dialog.winfo_children():
        widget.destroy()  # Remove existing widgets
    Label(loading_dialog, text="Conversion Successful!").pack()
    ok_button = tk.Button(loading_dialog, text="Okay", command=loading_dialog.destroy)
    ok_button.pack()

def open_file_dialog():
    global filepath
    filepath = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if filepath:
        img = Image.open(filepath)
        animate_label(img)
    update_button_status()

def animate_label(image, frame=0):
    try:
        image.seek(frame)
    except EOFError:
        frame = 0  
        image.seek(frame)
        
    tk_img = ImageTk.PhotoImage(image.resize((300, 300)))
    
    img_label.config(image=tk_img)
    img_label.image = tk_img

    frame += 1
    root.after(100, animate_label, image, frame)


def convert_gif():
    if filepath and output_folder:
        convert_button.config(bg='green')
        gif_to_sprite_sequence(filepath, output_folder)
    else:
        convert_button.config(bg='red')

def select_output_folder():
    global output_folder
    global output_folder_label 
    output_folder = filedialog.askdirectory()
    if not output_folder:
        output_folder = None
        output_folder_label.config(text="Output Folder: Not Selected", bg='red') 
    else:
        output_folder_label.config(text=f"Output Folder: {output_folder}", bg='yellow')
    update_button_status()

def update_button_status():
    if filepath and output_folder:
        convert_button.config(state=tk.NORMAL, bg='green')
    else:
        convert_button.config(state=tk.DISABLED, bg='red')

main()