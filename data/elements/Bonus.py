import pygame


class Bonus:
    def __init__(self, pos):
        self.img = None
        self.active = False
        self.speed = 3
        self.pos = pos
        self.size = (50, 50)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def draw(self, screen):
        screen.blit(self.img, (self.pos_x, self.pos_y))

    def update(self):
        self.pos_y += self.speed
        self.pos = (self.pos_x, self.pos_y)

    def activate(self):
        self.active = True

    def get_pos(self):
        return self.pos

    def get_size(self):
        return self.size


class IncreaseBoard(Bonus):
    def __init__(self, pos):
        super().__init__(pos)
        self.img = pygame.transform.scale(pygame.image.load('data/graphics/increase.png'), self.size)


class FastBall(Bonus):
    def __init__(self, pos):
        super().__init__(pos)
        self.img = pygame.transform.scale(pygame.image.load('data/graphics/fast.png'), self.size)


class SlowBall(Bonus):
    def __init__(self, pos):
        super().__init__(pos)
        self.img = pygame.transform.scale(pygame.image.load('data/graphics/slow.png'), self.size)


class DoubleBall(Bonus):
    def __init__(self, pos):
        super().__init__(pos)
        self.img = pygame.transform.scale(pygame.image.load('data/graphics/double.png'), self.size)


class DecreaseBoard(Bonus):
    def __init__(self, pos):
        super().__init__(pos)
        self.img = pygame.transform.scale(pygame.image.load('data/graphics/decrease.png'), self.size)
