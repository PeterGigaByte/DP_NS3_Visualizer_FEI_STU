import threading
from tkinter import filedialog as fd, Canvas
from tkinter.messagebox import showinfo

import customtkinter
from PIL import Image, ImageTk
from customtkinter import CTkProgressBar

from convertors.objects_definition import Node, P
from convertors.xml_reader import call_xml_parser
from gui import settings
from gui.compute_utils import compute_coordinates_location, create_node_dict_with_coordinates
from utils.manager import get_objects_by_type


class Gui2D:
    def __init__(self):
        self.settings = GuiSettings()
        self.window = customtkinter.CTk()
        self.canvas = Canvas(self.window, bg=self.settings.canvas_bg_color, width=self.settings.canvas_width,
                             height=self.settings.canvas_height, )
        self.canvas_information = Canvas(self.window, bg=self.settings.canvas_bg_color,
                                         width=self.settings.canvas_information_width,
                                         height=self.settings.canvas_information_height)
        self.simulation = Simulation(self)
        self.progress_bar = CTkProgressBar(master=self.window, width=self.settings.bar_width, height=30,
                                           orient='horizontal',
                                           mode='determinate')

        self.progress_bar_label = customtkinter.CTkLabel(master=self.window, text="0.00 %")

    def initialize_window(self):
        self.window.title(settings.window_title())
        self.window.geometry(settings.window_size())
        self.window.iconbitmap(self.settings.resources_path + settings.icon())
        # open file
        self.init_button(settings.select_file_image(), settings.open_button_label(), 0, self.simulation.select_file)
        # start simulation
        self.init_button(settings.start_simulation_image(), settings.start_simulation_label(), 1,
                         self.simulation.start_simulation)
        # resume simulation
        self.init_button(settings.resume_simulation_image(), settings.resume_simulation_label(), 2,
                         self.simulation.resume_simulation)
        # pause simulation
        self.init_button(settings.pause_simulation_image(), settings.pause_simulation_label(), 3,
                         self.simulation.pause_simulation)
        self.simulation.innitialize_scheduled_events()
        self.window.mainloop()

    def init_button(self, image_name, button_label, column_position, command):
        image = ImageTk.PhotoImage(
            Image.open(self.settings.resources_path + image_name).resize((20, 20), Image.ANTIALIAS))
        button = customtkinter.CTkButton(
            master=self.window,
            image=image,
            text=button_label,
            command=command
        )
        button.grid(column=column_position, row=0, sticky='w', padx=5, pady=8)


class GuiSettings:
    def __init__(self):
        self.canvas_bg_color = 'gray'
        self.canvas_width = '965'
        self.canvas_height = '540'
        self.canvas_information_width = '965'
        self.bar_width = 965
        self.canvas_information_height = '20'
        self.text_color = 'white'
        self.resources_path = 'resources/'
        self.node_img = None


class Simulation:
    def __init__(self, gui):
        self.gui = gui
        self.settings = GuiSettings()
        self.is_running_simulation = False
        self.is_next = False
        self.multiplier = 10
        self.actual_position = 0
        self.delay = 100
        self.selected_data = None
        self.node_dict = {}
        self.packet_simulation_objects = {}
        self.line_id_to_delete = None
        self.inf_text_id_to_delete = None
        self.inf_text_id = None
        self.line_id = None
        self.nodes = []
        self.nodes_text_info = None

    def innitialize_scheduled_events(self):
        self.gui.canvas.after(self.delay, self.draw_lines(), self.node_dict,
                              self.packet_simulation_objects)
        self.stop_deleting()

    def start_simulation(self):
        if self.selected_data is None:
            return
        if self.settings.node_img is None:
            self.settings.node_img = ImageTk.PhotoImage(
                Image.open(self.settings.resources_path + "router.png").resize((50, 50), Image.ANTIALIAS))
        self.restart_canvas()
        # 1. sets
        self.actual_position = 0
        self.gui.progress_bar.grid(column=0, row=3, columnspan=30, pady=5, padx=5, sticky="w")
        self.gui.progress_bar_label.grid(column=2, row=4, columnspan=30, padx=50, sticky="w")
        self.is_running_simulation = True

        # 2. get nodes from data
        nodes = get_objects_by_type(self.selected_data[0].content, Node)
        nodes_size = "Number of nodes in simulation: " + str(len(nodes))

        # 3. show info about nodes
        text_x = 850
        text_y = 11
        self.nodes_text_info = self.gui.canvas_information.create_text(text_x, text_y, text=nodes_size,
                                                                       fill=self.settings.text_color)
        self.gui.canvas_information.grid(column=0, columnspan=30, row=1, sticky='w', padx=5, pady=5)

        # 4. show nodes
        for node in nodes:
            x, y = compute_coordinates_location(node.loc_x, node.loc_y, self.multiplier,
                                                int(self.settings.canvas_width),
                                                int(self.settings.canvas_height))
            node.loc_x = x
            node.loc_y = y
            self.nodes.append(self.gui.canvas.create_image(x, y, anchor="nw", image=self.settings.node_img))
        self.gui.canvas.grid(column=0, columnspan=30, row=2, sticky='w', padx=5, pady=5)

        # 5. show packet simulation
        self.packet_simulation_objects = get_objects_by_type(self.selected_data[0].content, P)
        self.node_dict = create_node_dict_with_coordinates(nodes)

    def resume_simulation(self):
        self.clear_after_resume()
        self.is_running_simulation = True

    def pause_simulation(self):
        self.is_running_simulation = False

    def draw_lines(self):
        if self.is_running_simulation and self.actual_position < len(self.packet_simulation_objects):
            if self.is_next:
                color = "red"
                self.is_next = False
            else:
                color = "blue"
                self.is_next = True
            from_id = self.packet_simulation_objects[self.actual_position].f_id
            to_id = self.packet_simulation_objects[self.actual_position].t_id
            text_x, text_y = 650, 11
            information_text = "From: " + from_id + "   |  To: " + to_id
            self.inf_text_id = self.gui.canvas_information.create_text(text_x, text_y, text=information_text,
                                                                       fill=self.settings.text_color)
            self.gui.canvas_information.grid(column=0, columnspan=30, row=1, sticky='w', padx=5, pady=5)
            self.line_id = self.gui.canvas.create_line(self.node_dict[from_id]["loc_x"] + 25,
                                                       self.node_dict[from_id]["loc_y"] + 25,
                                                       self.node_dict[to_id]["loc_x"] + 25,
                                                       self.node_dict[to_id]["loc_y"] + 25, fill=color, arrow="last",
                                                       width=5)
            self.line_id_to_delete = self.gui.canvas.after(self.delay, self.gui.canvas.delete, self.line_id)
            self.inf_text_id_to_delete = self.gui.canvas_information.after(self.delay,
                                                                           self.gui.canvas_information.delete,
                                                                           self.inf_text_id)
            self.actual_position = self.actual_position + 1
            percentage = self.actual_position / len(self.packet_simulation_objects)
            self.gui.progress_bar.set(percentage)
            self.gui.progress_bar_label.configure(text=str('{:.2f} %'.format(percentage * 100)))
        self.gui.canvas.after(self.delay, self.draw_lines)

    def restart_canvas(self):
        self.clear_after_resume()
        if self.nodes_text_info is not None:
            self.gui.canvas_information.delete(self.nodes_text_info)
            self.gui.nodes_text_info = None
        if len(self.nodes) != 0:
            for node in self.nodes:
                self.gui.canvas.delete(node)

    def clear_after_resume(self):
        if self.inf_text_id is not None:
            self.gui.canvas_information.delete(self.inf_text_id)
        if self.line_id is not None:
            self.gui.canvas.delete(self.line_id)

    def select_file(self):
        filetypes = (
            ('Xml files', '*.xml'),
            ('All files', '*.')
        )

        filename = fd.askopenfilename(
            title=settings.open_button_label(),
            initialdir=self.settings.resources_path,
            filetypes=filetypes)

        showinfo(
            title=settings.show_info_label(),
            message=filename
        )
        self.selected_data = call_xml_parser(filename)

    def stop_deleting(self):
        if not self.is_running_simulation and (self.line_id_to_delete or self.line_id_to_delete is not None):
            self.gui.canvas.after_cancel(self.line_id_to_delete)
            self.gui.canvas.after_cancel(self.inf_text_id_to_delete)
        threading.Timer(self.delay / 200, self.stop_deleting).start()
