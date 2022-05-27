import pygame
import math
from data.elements.Sound import Sound
from data.elements.Sound import Sound


class Ball:
    def __init__(self, x_pos, y_pos, angle, speed, radius, screen_width, screen_height, padding):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.top_padding = padding
        # ball parameters
        self.radius = radius
        self.speed = speed
        self.angle = angle
        self.dx, self.dy = self.get_direction()
        rect_side = self.radius * 2
        self.rect = pygame.Rect(0, 0, rect_side, rect_side)
        self.rect.center = (x_pos, y_pos)
        self.active = True
        self.bonk_sound = pygame.mixer.Sound("data/audio/hit.wav")

    def change_radius(self, dr):
        self.radius += dr
        self.radius = min(self.radius, 25)
        rect_side = self.radius * 2
        self.rect = pygame.Rect(self.rect.left, self.rect.top, rect_side, rect_side)

    def change_angle(self, da):
        self.angle += da
        self.dx, self.dy = self.get_direction()

    def change_speed(self, ds):
        self.speed += ds
        self.speed = min(9, self.speed)
        self.speed = max(2, self.speed)

    def collide(self, rect):
        return self.rect.colliderect(rect)

    def reflect_x(self):
        self.angle = math.pi - self.angle if self.angle >= 0 else -math.pi - self.angle
        self.dx, self.dy = self.get_direction()

    def reflect_y(self):
        self.angle = - self.angle
        self.dx, self.dy = self.get_direction()

    def get_dy(self):
        return self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.rect.center, self.radius)

    def update(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

        if self.rect.centerx < self.radius + 50:
            Sound().play('with_edge_collide')
            self.reflect_x()
            self.rect.centerx = self.radius + 50

        if self.rect.centerx > self.screen_width - self.radius - 50:
            self.reflect_x()
            Sound().play('with_edge_collide')
            self.rect.centerx = self.screen_width - self.radius - 50

        if self.rect.centery < self.radius + self.top_padding + 50:
            self.reflect_y()
            Sound().play('with_edge_collide')
            self.rect.centery = self.radius + self.top_padding + 50

        if self.rect.centery > self.screen_height - 20:
            Sound().play('ball_loss')
            self.active = False

    def detect_collision(self, rect):
        if not self.collide(rect):
            return False
        self.bonk_sound.play()
        if self.dx > 0:
            delta_x = self.rect.right - rect.left
        else:
            delta_x = rect.right - self.rect.left
        if self.dy > 0:
            delta_y = self.rect.bottom - rect.top
        else:
            delta_y = rect.bottom - self.rect.top

        if abs(delta_x - delta_y) < 10:
            self.reflect_y()
            self.reflect_x()
        elif delta_x > delta_y:
            self.reflect_y()
        elif delta_y > delta_x:
            self.reflect_x()
        return True

    def get_direction(self):
        return math.cos(self.angle), -math.sin(self.angle)

    def get_angle(self):
        return self.angle

    def get_radius(self):
        return self.radius

    def get_speed(self):
        return self.speed

    def get_pos(self):
        return self.rect.center
