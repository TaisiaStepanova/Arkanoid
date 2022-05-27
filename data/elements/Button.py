import sys
import pygame as pg
import pygame.mixer

from data.utils.utils import print_text


class Button:
    def __init__(self, message, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (162, 0, 22)
        self.active_clr = (191, 0, 31)
        self.message = message
        self.x = 0
        self.y = 0
        self.count = 0

    def draw(self, surface, x, y, indent):
        self.x = x
        self.y = y
        mouse = pg.mouse.get_pos()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pg.draw.rect(surface, self.active_clr, (x, y, self.width, self.height))
        else:
            pg.draw.rect(surface, self.inactive_clr, (x, y, self.width, self.height))

        print_text(surface, self.message, x + indent, y + 3)

    def is_active(self):
        mouse = pg.mouse.get_pos()
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            return True
        else:
            return False
