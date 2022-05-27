import pygame
import json
from data.utils.utils import *
from data.elements.Button import *
from data.elements.Brick import *
from data.elements.Control import Control
from data.elements.Bonus import *


class Round(pygame.Surface):
    columns = 14

    def __init__(self, size, file, loss_func, win_func):
        super().__init__(size)
        with open(file) as f:
            level_content = json.load(f)
            self.bonuses = []
            self.bricks = self.get_bricks(level_content['bricks'])
            self.num = level_content["level_number"]
        self.win_func = win_func
        self.loss_func = loss_func
        self.background = load_png('background.png')
        self.edges = load_png('edges.png')
        self.border = pygame.Surface((1100, 1))
        self.info_area = pygame.Surface((1200, 100))
        self.round_end = False
        self.control = Control(*size, 100, self.bricks, self.loss_func)
        self.font = pygame.font.Font('data/fonts/bonsergo.otf', 100)

    def draw(self, screen):
        self.blit(self.background, (0, 100))
        self.blit(self.edges, (0, 100))
        self.border.fill((255, 0, 0))
        self.blit(self.border, (50, 980))
        self.update()
        screen.blit(self, (0, 0))

    def create_info_area(self):
        score = self.font.render('Score: {}'.format(str(self.control.score)), False, (255, 255, 255))
        round_num = self.font.render('Level {}'.format(str(self.num)), False, (255, 255, 255))
        self.info_area.fill((160, 9, 220))
        self.info_area.blit(score, (40, 20))
        self.info_area.blit(round_num, (self.info_area.get_rect().right - round_num.get_width() - 40, 10))
        self.blit(self.info_area, (0, 0))

    def update(self):
        self.create_info_area()
        self.update_round()
        self.update_bonus()
        if self.round_end:
            self.num += 1

    def update_round(self):
        if len(self.bricks) == 0:
            self.round_end = True
        for brick in self.bricks:
            if brick.active:
                brick.draw(self)
            else:
                self.bricks.remove(brick)

        if self.control.active:
            self.control.update()
            self.control.draw(self)
        else:
            self.loss_func()

    def update_bonus(self):
        for bonus in self.bonuses:
            if bonus.active:
                bonus.update()
                bonus.draw(self)
        for bonus in self.bonuses:
            if bonus.active and self.control.collide(pygame.Rect(bonus.get_pos(), bonus.get_size())):
                self.control.call_bonus(bonus)
                self.bonuses.remove(bonus)

    def get_bricks(self, data):
        bricks = []
        for brick in data:
            bricks.append(Brick(115 + brick['position'] % self.columns * 70, 250 + brick['position'] // self.columns * 38,
                                brick['lives'], make_color(brick['color'])))
            brick_bonus = self.create_bonus(brick['bonus'], bricks[-1].center)
            bricks[-1].add_bonus(brick_bonus)
            if brick_bonus is not None:
                self.bonuses.append(brick_bonus)
        return bricks

    @staticmethod
    def create_bonus(bonus_name: str, pos) -> Bonus:
        new_bonus = None
        if bonus_name == 'increase_board':
            new_bonus = IncreaseBoard(pos)
        elif bonus_name == 'ball_fast':
            new_bonus = BallFast(pos)
        elif bonus_name == 'ball_slow':
            new_bonus = BallSlow(pos)
        elif bonus_name == 'double_ball':
            new_bonus = DoubleBall(pos)
        elif bonus_name == 'decrease_board':
            new_bonus = DecreaseBoard(pos)
        return new_bonus
