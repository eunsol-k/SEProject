import pygame
import configparser, os

thisfolder = os.path.dirname(os.path.abspath(__file__))
inifile = os.path.join(thisfolder, 'settings.ini')

config = configparser.RawConfigParser()
config.read(inifile)

# Set Mod
def set_difficulty(difficulty):
    config.set('Mod', 'Difficulty', str(difficulty))
def set_sound(sound):
    config.set('Mod', 'Sound', str(sound))
def set_screen(size):
    config.set('Mod', 'Screen', str(size))
    screen_size = get_screen(size)
    pygame.display.set_mode(screen_size, pygame.RESIZABLE)
def set_colorblind(state):
    config.set('Mod', 'colorblind', str(state))

# Set Control
def set_keymap_left(key):
    config.set('Control', 'left', str(key))
def set_keymap_right(key):
    config.set('Control', 'right', str(key))
def set_keymap_up(key):
    config.set('Control', 'up', str(key))
def set_keymap_down(key):
    config.set('Control', 'down', str(key))
def set_keymap_uno(key):
    config.set('Control', 'uno', str(key))
def set_keymap_time(key):
    config.set('Control', 'time', str(key))
def set_keymap_check(key):
    config.set('Control', 'check', str(key))
def set_keymap_by_index(index, key):
    if index == 0:
        set_keymap_left(key)
    elif index == 1:
        set_keymap_right(key)
    elif index == 2:
        set_keymap_up(key)
    elif index == 3:
        set_keymap_down(key)
    elif index == 4:
        set_keymap_uno(key)
    elif index == 5:
        set_keymap_time(key)
    elif index == 6:
        set_keymap_check(key)

# Get Mod
def get_difficulty_num():
    return config.getint('Mod', 'Difficulty')
def get_sound_bool():
    return config.getboolean('Mod', 'Sound')
def get_screen_num():
    return config.getint('Mod', 'Screen')
def get_colorblind_bool():
    return config.getboolean('Mod', 'colorblind')

def get_difficulty(value):
    if(value == 0):
        return 'Easy'
    elif(value == 1):
        return 'Normal'
    else:
        return 'Hard'
def get_sound(value):
    if value:
        return "ON"
    else:
        return "OFF"
def get_screen(value):
    if(value == 0):
        return (800, 600)
    elif(value == 1):
        return (1280, 720)
    else:
        return (1920, 1080)
def get_colorblind(value):
    if value:
        return "ON"
    else:
        return "OFF"

def get_mod_all(index):
    if(index == 0):
        return str(get_difficulty(get_difficulty_num()))
    elif(index == 1):
        return str(get_sound(get_sound_bool()))
    elif(index == 2):
        return str(get_screen(get_screen_num())[0]) + 'x' + str(get_screen(get_screen_num())[1])
    elif(index == 3):
        return str(get_colorblind(get_colorblind_bool()))
    else:
        return ''

# Get Control
def get_keymap_left():
    return config.getint('Control', 'left')
def get_keymap_right():
    return config.getint('Control', 'right')
def get_keymap_up():
    return config.getint('Control', 'up')
def get_keymap_down():
    return config.getint('Control', 'down')
def get_keymap_uno():
    return config.getint('Control', 'uno')
def get_keymap_time():
    return config.getint('Control', 'time')
def get_keymap_check():
    return config.getint('Control', 'check')

def get_keymap_all(index):
    if(index == 0):
        return str(pygame.key.name(get_keymap_left()))
    elif(index == 1):
        return str(pygame.key.name(get_keymap_right()))
    elif(index == 2):
        return str(pygame.key.name(get_keymap_up()))
    elif(index == 3):
        return str(pygame.key.name(get_keymap_down()))
    elif(index == 4):
        return str(pygame.key.name(get_keymap_uno()))
    elif(index == 5):
        return str(pygame.key.name(get_keymap_time()))
    else:
        return str(pygame.key.name(get_keymap_check()))

# Get Section's option list
def get_mod_list():
    return config.options('Mod')
def get_control_list():
    return config.options('Control')
def get_control_list_all():
    control_list = []
    control_list_num = []
    control_tuple = config.items('Control')
    for control in control_tuple:
        value = int(control[1])
        control_list.append(pygame.key.name(value))
        control_list_num.append(value)
    return (control_list, control_list_num)

# Rollback settings
def mod_back():
    set_difficulty(0) # Easy
    set_sound(True) # ON
    set_screen(0) # 800x600
    set_colorblind(False) # OFF
def control_back():
    set_keymap_left(1073741904) # ←
    set_keymap_right(1073741903) # →
    set_keymap_up(1073741906) # ↑
    set_keymap_down(1073741905) # ↓
    set_keymap_uno(117) # u
    set_keymap_time(116) # t
    set_keymap_check(13) # Enter

# Save Settings
def save():
    with open(inifile, 'w') as configfile:
        config.write(configfile)