from tkinter import filedialog as fd, Canvas
from tkinter.messagebox import showinfo

import customtkinter
from PIL import Image, ImageTk

from convertors.objects_definition import Node, P
from convertors.xml_reader import call_xml_parser
from gui import settings
from gui.compute_utils import compute_coordinates_location, create_node_dict_with_coordinates
from utils.manager import get_objects_by_type

window = customtkinter.CTk()
open_button = customtkinter.CTkButton
start_button = customtkinter.CTkButton
resume_button = customtkinter.CTkButton
pause_button = customtkinter.CTkButton
is_running_simulation = False
is_next = False
canvas_bg_color = 'gray'
canvas_width = '965'
canvas_height = '540'
canvas_information_width = '965'
canvas_information_height = '20'
multiplier = 10
text_color = 'white'
canvas = Canvas(window, bg=canvas_bg_color, width=canvas_width, height=canvas_height)
canvas_information = Canvas(window, bg=canvas_bg_color, width=canvas_information_width,
                            height=canvas_information_height)
resources_path = 'resources/'
selected_data = ""
actual_position = 0
node_img = ImageTk.PhotoImage(
    Image.open(resources_path + "router.png").resize((50, 50), Image.ANTIALIAS))
delay = 500


def set_settings():
    window.title(settings.window_title())
    window.geometry(settings.window_size())
    window.iconbitmap(resources_path + settings.icon())


def select_file():
    global selected_data
    filetypes = (
        ('Xml files', '*.xml'),
        ('All files', '*.')
    )

    filename = fd.askopenfilename(
        title=settings.open_button_label(),
        initialdir=resources_path,
        filetypes=filetypes)

    showinfo(
        title=settings.show_info_label(),
        message=filename
    )
    selected_data = call_xml_parser(filename)


def start_simulation():
    global actual_position, is_running_simulation, canvas, canvas_information, node_img, delay
    # 1. sets
    actual_position = 0
    is_running_simulation = True

    # 2. get nodes from data
    nodes = get_objects_by_type(selected_data[0].content, Node)
    nodes_size = "Number of nodes in simulation: " + str(len(nodes))

    # 3. show info about nodes
    text_x = 850
    text_y = 11
    canvas_information.create_text(text_x, text_y, text=nodes_size, fill=text_color)
    canvas_information.grid(column=0, columnspan=30, row=1, sticky='w', padx=5, pady=5)

    # 4. show nodes
    for node in nodes:
        x, y = compute_coordinates_location(node.loc_x, node.loc_y, multiplier, int(canvas_width), int(canvas_height))
        node.loc_x = x
        node.loc_y = y
        canvas.create_image(x, y, anchor="nw", image=node_img)
    canvas.grid(column=0, columnspan=30, row=2, sticky='w', padx=5, pady=5)

    # 5. show packet simulation
    packet_simulation_objects = get_objects_by_type(selected_data[0].content, P)
    node_dict = create_node_dict_with_coordinates(nodes)
    canvas.after(delay, draw_lines, node_dict, packet_simulation_objects)


def draw_lines(node_dict, packet_simulation_objects):
    global actual_position, is_running_simulation, is_next, delay
    if is_running_simulation and actual_position < len(packet_simulation_objects):
        if is_next:
            color = "red"
            is_next = False
        else:
            color = "blue"
            is_next = True
        from_id = packet_simulation_objects[actual_position].f_id
        to_id = packet_simulation_objects[actual_position].t_id
        text_x, text_y = 650, 11
        information_text = "From: " + from_id + "   |  To: " + to_id
        inf_text_id = canvas_information.create_text(text_x, text_y, text=information_text, fill=text_color)
        canvas_information.grid(column=0, columnspan=30, row=1, sticky='w', padx=5, pady=5)
        line_id = canvas.create_line(node_dict[from_id]["loc_x"] + 25, node_dict[from_id]["loc_y"] + 25,
                                     node_dict[to_id]["loc_x"] + 25,
                                     node_dict[to_id]["loc_y"] + 25, fill=color, arrow="last", width=5)
        canvas.after(delay, canvas.delete, line_id)
        canvas_information.after(delay, canvas_information.delete, inf_text_id)
        actual_position = actual_position + 1

    canvas.after(delay, draw_lines, node_dict, packet_simulation_objects)


def resume_simulation():
    global actual_position, is_running_simulation
    is_running_simulation = True


def pause_simulation():
    global actual_position, is_running_simulation
    is_running_simulation = False


def init_button(image_name, button_label, column_position, command):
    image = ImageTk.PhotoImage(
        Image.open(resources_path + image_name).resize((20, 20), Image.ANTIALIAS))
    button = customtkinter.CTkButton(
        master=window,
        image=image,
        text=button_label,
        command=command
    )
    button.grid(column=column_position, row=0, sticky='w', padx=5, pady=8)
    return button


def initialize_window():
    set_settings()
    global start_button, resume_button, pause_button
    init_button(settings.select_file_image(), settings.open_button_label(), 0, select_file)
    start_button = init_button(settings.start_simulation_image(), settings.start_simulation_label(), 1,
                               start_simulation)
    resume_button = init_button(settings.resume_simulation_image(), settings.resume_simulation_label(), 2,
                                resume_simulation)
    pause_button = init_button(settings.pause_simulation_image(), settings.pause_simulation_label(), 3,
                               pause_simulation)

    window.mainloop()
