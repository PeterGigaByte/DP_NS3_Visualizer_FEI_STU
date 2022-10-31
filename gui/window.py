from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import Canvas
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
    open_button.grid(column=0, row=0, sticky='w', padx=5, pady=8)


def start_simulation_button():
    start_simulation_image = ImageTk.PhotoImage(
        Image.open(resources_path + settings.start_simulation_image()).resize((20, 20), Image.ANTIALIAS))
    simulation_button = customtkinter.CTkButton(
        master=window,
        image=start_simulation_image,
        text=settings.start_simulation_label(),
    )
    simulation_button.grid(column=1, row=0, sticky='w', padx=5, pady=8)


def pause_simulation_button():
    pause_simulation_image = ImageTk.PhotoImage(
        Image.open(resources_path + settings.pause_simulation_image()).resize((20, 20), Image.ANTIALIAS))
    simulation_button = customtkinter.CTkButton(
        master=window,
        image=pause_simulation_image,
        text=settings.pause_simulation_label(),
    )
    simulation_button.grid(column=2, row=0, sticky='w', padx=5, pady=8)


def initialize_window():
    set_settings()

    select_file_button()
    start_simulation_button()
    pause_simulation_button()

    canvas = Canvas(window, bg='gray', width='965', height='540')
    canvas.create_arc((5, 10, 150, 200), start=0, extent=150, fill='red')
    canvas.create_arc((500, 30, 100, 130), start=50, extent=80, fill='green')
    canvas.create_arc((500, 700, 100, 130), start=50, extent=80, fill='black')
    canvas.create_arc((150, 50, 20, 150), start=150, extent=80, fill='white')
    canvas.grid(column=0, columnspan=30, row=1, sticky='w', padx=5, pady=5)

    window.mainloop()
