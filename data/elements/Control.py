import pygame
from data.utils.utils import *
import math
from data.elements.Ball import *
from data.elements.Bonus import *
from data.elements.Sound import Sound


class Control:
    def __init__(self, screen_width, screen_height, top_padding, bricks, loss_func):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.top_padding = top_padding
        self.platform = pygame.Rect(500, 950, 200, 15)
        self.m_size = self.platform.width * 0.4
        self.speed = 10
        self.platform_angle = math.pi / 6
        self.loss_func = loss_func

        # balls
        self.balls = [
            Ball(self.platform.centerx, self.platform.top - 20, math.pi / 4, 5, 6, screen_width,
                 screen_height, top_padding)]
        self.bricks = bricks
        self.score = 0
        self.active = True

    def draw(self, screen):
        pygame.draw.rect(screen, (190, 190, 190), self.platform)
        for ball in self.balls:
            if ball.active:
                ball.draw(screen)

    def update(self):
        for ball in self.balls:
            if not ball.active:
                self.balls.remove(ball)

        for ball in self.balls:
            if ball.active:
                ball.update()

        for ball in self.balls:
            if ball.collide(self.platform) and ball.get_dy() > 0:
                Sound().play('with_platform_collide')
                ball.reflect_y()
                if ball.rect.centerx > self.platform.centerx + self.m_size / 2:
                    ball.change_angle(-self.platform_angle)
                elif ball.rect.centerx < self.platform.centerx - self.m_size / 2:
                    ball.change_angle(self.platform_angle)
            for brick in self.bricks:
                if ball.detect_collision(brick):
                    brick.hit()
                    self.score += 100

        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_LEFT]:
            self.move_left()
        if key_press[pygame.K_RIGHT]:
            self.move_right()

        if len(self.balls) == 0:
            self.active = False

    def move_left(self):
        if self.platform.left - self.speed > 50:
            self.platform.left -= self.speed

    def move_right(self):
        if self.platform.right + self.speed < self.screen_width - 50:
            self.platform.right += self.speed

    def change_board_size(self, ds):
        self.platform.width += ds
        self.platform.width = min(self.platform.width, 320)
        self.platform.width = max(self.platform.width, 80)
        self.m_size = self.platform.width * 0.6

    def collide(self, rect):
        return self.platform.colliderect(rect)

    def call_bonus(self, bonus):
        if type(bonus) is IncreaseBoard:
            Sound().play('platform_increase')
            self.change_board_size(30)
        elif type(bonus) is FastBall:
            Sound().play('catch_bonus')
            for ball in self.balls:
                ball.change_speed(1)
        elif type(bonus) is SlowBall:
            Sound().play('catch_bonus')
            for ball in self.balls:
                ball.change_speed(-1)
        elif type(bonus) is DoubleBall:
            Sound().play('catch_bonus')
            self.double_balls()
        elif type(bonus) is DecreaseBoard:
            Sound().play('platform_decrease')
            self.change_board_size(-30)

    def double_balls(self):
        new_balls = []
        for ball in self.balls:
            new_balls.append(Ball(*ball.get_pos(), ball.get_angle() + math.pi / 3, ball.get_speed(), ball.get_radius(),
                                  self.screen_width, self.screen_height, self.top_padding))
            new_balls.append(Ball(*ball.get_pos(), ball.get_angle() - math.pi / 3, ball.get_speed(), ball.get_radius(),
                                  self.screen_width, self.screen_height, self.top_padding))
        self.balls = new_balls


