import configparser
import os

settings = 'settings.cfg'
settings_exist = os.path.exists(settings)


def build_gui_settings(config):
    config['GUI'] = {}
    config['GUI']['title'] = 'NS3 Visualizer'
    config['GUI']['width'] = '980'
    config['GUI']['height'] = '700'
    config['GUI']['open_button_label'] = 'Select simulation file'
    config['GUI']['show_info_label'] = 'Select file'
    config['GUI']['appearance_mode'] = 'dark'
    config['GUI']['color_theme'] = 'dark-blue'
    config['GUI']['icon'] = 'intranet.ico'
    config['GUI']['select_file_image'] = 'open-file.png'
    config['GUI']['start_simulation_image'] = 'start-sim.png'
    config['GUI']['start_simulation_label'] = 'Start simulation'
    config['GUI']['resume_simulation_image'] = 'resume-sim.png'
    config['GUI']['resume_simulation_label'] = 'Resume simulation'
    config['GUI']['pause_simulation_image'] = 'pause-sim.png'
    config['GUI']['pause_simulation_label'] = 'Pause simulation'


def build_file():
    config = configparser.ConfigParser()

    build_gui_settings(config)

    with open(settings, 'w') as configfile:
        config.write(configfile)


if not settings_exist:
    build_file()


def read_config():
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    config.sections()
    return config


def get_gui_config():
    return read_config()["GUI"]


# TODO
# To delete(testing purpose):
build_file()
