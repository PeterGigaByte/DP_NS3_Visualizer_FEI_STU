from user_settings import config

settings = config.get_gui_config()


def window_size():
    return settings['width'] + "x" + settings['height']


def window_title():
    return settings['title']


def open_button_label():
    return settings['open_button_label']


def show_info_label():
    return settings['show_info_label']


def appearance_mode():
    return settings['appearance_mode']


def color_theme():
    return settings['color_theme']


def icon():
    return settings['icon']


def select_file_image():
    return settings['select_file_image']


def start_simulation_image():
    return settings['start_simulation_image']


def start_simulation_label():
    return settings['start_simulation_label']


def resume_simulation_image():
    return settings['resume_simulation_image']


def resume_simulation_label():
    return settings['resume_simulation_label']


def pause_simulation_image():
    return settings['pause_simulation_image']


def pause_simulation_label():
    return settings['pause_simulation_label']


def resource_path():
    return settings['resource_path']


def canvas_bg_color():
    return settings['canvas_bg_color']


def canvas_width():
    return settings['canvas_width']


def canvas_height():
    return settings['canvas_height']


def frame_information_width():
    return settings['frame_information_width']


def frame_information_height():
    return settings['frame_information_height']


def frame_information_bg_color():
    return settings['frame_information_bg_color']


def bar_width():
    return settings['bar_width']


def text_color():
    return settings['text_color']


def node_img():
    return settings['node_img']
