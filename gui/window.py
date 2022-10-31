from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import customtkinter
from PIL import Image, ImageTk

from gui import settings

window = customtkinter.CTk()
resources_path = 'resources/'


def set_settings():
    window.title(settings.window_title())
    window.geometry(settings.window_size())
    window.iconbitmap(resources_path + settings.icon())


def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.xml*')
    )

    filename = fd.askopenfilename(
        title=settings.open_button_label(),
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title=settings.show_info_label(),
        message=filename
    )


def select_file_button():
    select_file_image = ImageTk.PhotoImage(
        Image.open(resources_path + settings.select_file_image()).resize((20, 20), Image.ANTIALIAS))
    open_button = customtkinter.CTkButton(
        master=window,
        image=select_file_image,
        text=settings.open_button_label(),
        command=select_file
    )
    open_button.grid(column=0, row=0, sticky='w', padx=5, pady=5)


def start_simulation_button():
    start_simulation_image = ImageTk.PhotoImage(
        Image.open(resources_path + settings.start_simulation_image()).resize((20, 20), Image.ANTIALIAS))
    simulation_button = customtkinter.CTkButton(
        master=window,
        image=start_simulation_image,
        text=settings.start_simulation_label(),
    )
    simulation_button.grid(column=1, row=0, sticky='w', padx=5, pady=5)


def pause_simulation_button():
    pause_simulation_image = ImageTk.PhotoImage(
        Image.open(resources_path + settings.pause_simulation_image()).resize((20, 20), Image.ANTIALIAS))
    simulation_button = customtkinter.CTkButton(
        master=window,
        image=pause_simulation_image,
        text=settings.pause_simulation_label(),
    )
    simulation_button.grid(column=2, row=0, sticky='w', padx=5, pady=5)


def initialize_window():
    set_settings()
    select_file_button()
    start_simulation_button()
    pause_simulation_button()
    window.mainloop()
