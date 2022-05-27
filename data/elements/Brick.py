import pygame
from data.elements.Bonus import *


class Brick(pygame.Rect):
    def __init__(self, x_pos, y_pos, lives, color):
        super().__init__(x_pos, y_pos, 60, 30)
        self.bonus = None
        self.lives = lives
        self.color = color
        self.active = True
        self.sound = pygame.mixer.Sound("data/audio/hit.wav")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)

    def hit(self):
        self.lives -= 1
        if self.lives == 0:
            self.active = False
            self.sound.play()
            self.drop_bonus()

    def add_bonus(self, bonus: Bonus):
        self.bonus = bonus

    def drop_bonus(self):
        if self.bonus is not None:
            self.bonus.activate()
