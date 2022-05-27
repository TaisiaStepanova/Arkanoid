import pygame


class Sound:
    def __init__(self):
        self.platform_increase = pygame.mixer.Sound('data/audio/platform_increase.wav')
        self.platform_decrease = pygame.mixer.Sound('data/audio/platform_decrease.wav')
        self.ball_loss = pygame.mixer.Sound('data/audio/ball_loss.wav')
        self.with_platform_collide = pygame.mixer.Sound('data/audio/with_platform_collide.wav')
        self.with_edge_collide = pygame.mixer.Sound('data/audio/with_edge_collide.wav')
        self.catch_bonus = pygame.mixer.Sound('data/audio/catch_bonus.wav')

    def play(self, name):
        if name == 'platform_increase':
            self.platform_increase.play()
        elif name == 'platform_decrease':
            self.platform_decrease.play()
        elif name == 'ball_loss':
            self.ball_loss.play()
        elif name == 'with_platform_collide':
            self.with_platform_collide.play()
        elif name == 'with_edge_collide':
            self.with_edge_collide.play()
        elif name == 'catch_bonus':
            self.catch_bonus.play()
