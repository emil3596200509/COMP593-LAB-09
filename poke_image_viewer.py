"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from tkinter import *
from tkinter import ttk
import os
import poke_api
import image_lib
import ctypes
import inspect
from PIL import Image, ImageTk


# Get the script and images directory
script_name = inspect.getfile(inspect.currentframe())
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

# Create the images directory if it does not exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Create the main window
root = Tk()
root.title("Pokemon Viewer")
root.geometry('600x600')
root.minsize(500, 600)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set the icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
root.iconbitmap(os.path.join(script_dir, 'poke_ball.ico'))

# Create frames
frm = ttk.Frame(root)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)
frm.grid(sticky=NSEW)

# Populate frames with widgets and define event handler functions
image_path = os.path.join(script_dir, 'poke_ball.png')
pil_image = Image.open(image_path)
photo = ImageTk.PhotoImage(pil_image)

lbl_image = ttk.Label(frm, image=photo)
lbl_image.image = photo
lbl_image.grid(row=0, column=0, padx=0)

# Create button to set desktop background
def handle_set_desktop():
    pokemon_name = cbox_poke_sel.get()
    image_path = os.path.join(images_dir, f'{pokemon_name}.png')
    print(f"Setting desktop to {image_path}...", end='')
    SPI_SETDESKWALLPAPER = 20
    try:
        if ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0):
            print("success")
            return True
        else:
            print("failure")
    except:
        print("failure")
    return False

btn_set_desktop = ttk.Button(frm, text="Set as Desktop Image", command=handle_set_desktop, state=DISABLED)
btn_set_desktop.grid(row=2, column=0, padx=0, pady=10)

def handle_poke_sel(event):
    pokemon_name = cbox_poke_sel.get()
    image_url = poke_api.get_pokemon_image_url(pokemon_name)
    image_data = image_lib.download_image(image_url)
    image_path = os.path.join(images_dir, f'{pokemon_name}.png')
    image_lib.save_image_file(image_data, image_path)
    photo = PhotoImage(file=image_path)
    lbl_image.config(image=photo)
    lbl_image.image = photo
    btn_set_desktop.config(state=NORMAL)

pokemon_names = poke_api.get_pokemon_names()
cbox_poke_sel = ttk.Combobox(frm, values=pokemon_names)
cbox_poke_sel.grid(row=1, column=0, pady=10)
cbox_poke_sel.bind('<<ComboboxSelected>>', handle_poke_sel)

root.mainloop()