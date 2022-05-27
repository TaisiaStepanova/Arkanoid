import os
import pygame
import json

import pygame.font

pygame.font.init()

RED = (255, 0, 0)
AQUA = (51, 255, 255)
ORANGE = (255, 128, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (153, 0, 153)


def load_png(filename):
    if not filename.lower().endswith('.png'):
        filename = '{}.png'.format(filename)
    fullpath = os.path.join(os.path.dirname(__file__), '..', 'graphics', filename)
    if not os.path.exists(fullpath):
        raise FileNotFoundError('File not found: {}'.format(fullpath))

    image = pygame.image.load(fullpath)
    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image


def print_text(surface, message, x, y, font_color=(255, 255, 255), font_type='data/fonts/anfisa-grotesk.ttf', font_size=80):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    surface.blit(text, (x, y))


def from_json(filename):
    if not filename.lower().endswith('.json'):
        filename = '{}.json'.format(filename)
    fullpath = os.path.join(os.path.dirname(__file__), '..', 'rounds', filename)
    with open(fullpath) as file:
        content = json.load(file)
        return content


def sound_play(sound):
    sound.play()
    pygame.time.delay(300)


def make_color(color_name: str):
    if color_name == 'red':
        return RED
    elif color_name == 'yellow':
        return YELLOW
    elif color_name == 'orange':
        return ORANGE
    elif color_name == 'green':
        return GREEN
    elif color_name == 'blue':
        return BLUE
    elif color_name == 'aqua':
        return AQUA
    elif color_name == 'purple':
        return PURPLE
