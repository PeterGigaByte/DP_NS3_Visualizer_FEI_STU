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


def pause_simulation_image():
    return settings['pause_simulation_image']


def pause_simulation_label():
    return settings['pause_simulation_label']
