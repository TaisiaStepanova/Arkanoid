import pygame
from data.utils.utils import *
from data.elements.Button import *
from data.elements.Brick import *
from data.elements.Control import Control
from data.elements.Bonus import *
# window settings
import pygame.font
from data.elements.Sound import Sound

WIDTH = 1200  # display width
HEIGHT = 1000  # display height
FPS = 120  # frames per second

# main colors
BLACK = (0, 0, 0)
PURPLE = (160, 9, 220)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_RED = (162, 0, 22)

# screen generation
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arkanoid')
clock = pygame.time.Clock()

pygame.mixer.init()
button_click_sound = pg.mixer.Sound('data/audio/button.wav')
pygame.mixer.music.load('data/audio/menu.mp3')
pygame.mixer.music.play(-1)


class Round(pygame.Surface):
    columns = 14

    def __init__(self, size, file, loss_func, loss_record_func, win_func):
        super().__init__(size)
        with open(file) as f:
            level_content = json.load(f)
            self.bonuses = []
            self.bricks = self.get_bricks(level_content['bricks'])
            self.num = level_content['level_number']
        self.win_func = win_func
        self.loss_func = loss_func
        self.loss_record = loss_record_func
        self.background = load_png('background.png')
        self.edges = load_png('edges.png')
        self.border = pygame.Surface((1100, 1))
        self.info_area = pygame.Surface((1200, 100))
        self.round_end = False
        with open('data/settings.json') as settings:
            data = json.load(settings)
        self.round = data['round']
        self.score = data['score']
        self.min_score = data['min_score']
        self.control = Control(*size, 100, self.bricks, self.loss_func)
        self.font = pygame.font.Font('data/fonts/bonsergo.otf', 100)

    def draw(self):
        self.blit(self.background, (0, 100))
        self.blit(self.edges, (0, 100))
        self.border.fill(RED)
        self.blit(self.border, (50, 980))
        self.update()
        screen.blit(self, (0, 0))

    def create_info_area(self):
        score = self.font.render('Score: {}'.format(str(self.score + self.control.score)), False, WHITE)
        round_num = self.font.render('Level {}'.format(str(self.num)), False, WHITE)
        self.info_area.fill(DARK_RED)
        self.info_area.blit(score, (40, 10))
        self.info_area.blit(round_num, (self.info_area.get_rect().right - round_num.get_width() - 40, 10))
        self.blit(self.info_area, (0, 0))

    def update(self):
        self.create_info_area()
        self.update_round()
        self.update_bonus()
        if self.round_end and self.round != 2:
            self.round += 1
            with open('data/settings.json') as settings:
                data = json.load(settings)
            data['round'] = self.round
            data['score'] = self.score + self.control.score
            with open('data/settings.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            pygame.time.delay(250)
            for ball in self.control.balls:
                self.control.balls.remove(ball)
            menu(self.round, True)
        elif self.round_end and self.round == 10:
            with open('data/settings.json') as settings:
                data = json.load(settings)
            data['round'] = 1
            data['score'] = 0
            with open('data/settings.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.score += self.control.score
            self.win_func(self.score)

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
            set_min_score()
            with open('data/settings.json') as settings:
                data = json.load(settings)
            data['round'] = 1
            data['score'] = 0
            with open('data/settings.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            with open('data/records.json') as rec:
                records = json.load(rec)
            if len(records) < 10:
                self.loss_record(self.score + self.control.score)
            elif len(records) >= 10 and self.score + self.control.score > self.min_score + 1:
                self.loss_record(self.score + self.control.score)
            else:
                self.loss_func()
        set_min_score()

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
            bricks.append(Brick(115 + brick['position'] % self.columns * 70, 250 + brick['position'] //
                                self.columns * 38, brick['lives'], make_color(brick['color'])))
            brick_bonus = self.create_bonus(brick['bonus'], bricks[-1].center)
            bricks[-1].add_bonus(brick_bonus)
            if brick_bonus is not None:
                self.bonuses.append(brick_bonus)
        return bricks

    @staticmethod
    def create_bonus(bonus: str, pos) -> Bonus:
        new_bonus = None
        if bonus == 'increase_board':
            new_bonus = IncreaseBoard(pos)
        elif bonus == 'ball_fast':
            new_bonus = FastBall(pos)
        elif bonus == 'ball_slow':
            new_bonus = SlowBall(pos)
        elif bonus == 'double_ball':
            new_bonus = DoubleBall(pos)
        elif bonus == 'decrease_board':
            new_bonus = DecreaseBoard(pos)
        return new_bonus


class Game:
    def __init__(self):
        self.display = True
        self.score = 0
        self.font = pygame.font.Font('data/fonts/anfisa-grotesk.ttf', 60)

    def loss(self):
        self.display = False
        self.font = pygame.font.Font('data/fonts/anfisa-grotesk.ttf', 150)
        transp = pygame.Surface((WIDTH, HEIGHT))
        transp.fill(DARK_RED)
        transp.set_alpha(5)

        lose_text = self.font.render('You lose!', False, WHITE)

        running = True

        while running:
            pygame.display.update()
            screen.blit(transp, (0, 0))
            screen.blit(lose_text, (400, 400))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        running = False
                        menu(1, False)

            key_press = pygame.key.get_pressed()
            if key_press[pygame.K_SPACE]:
                running = False

    def loss_record(self, score):
        self.display = False
        self.font = pygame.font.Font('data/fonts/anfisa-grotesk.ttf', 100)
        transp = pygame.Surface((WIDTH, HEIGHT))
        transp.fill(DARK_RED)

        lose_text_1 = self.font.render('You lose, but break a record!', False, WHITE)
        lose_text_2 = self.font.render('Enter your name:', False, WHITE)

        running = True
        input_text = ''
        while running:
            pygame.display.update()
            screen.blit(transp, (0, 0))
            screen.blit(lose_text_1, (250, 300))
            screen.blit(lose_text_2, (350, 480))

            need_input = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if need_input and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        running = False
                        menu(1, False)
                    elif event.key == pygame.K_RETURN:
                        need_input = False
                        add_record(input_text, score)
                        menu(1, False)
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        transp.fill(DARK_RED)
                    else:
                        if len(input_text) < 20:
                            input_text += event.unicode
            print_text(screen, input_text, 350, 580, WHITE)

    def win(self, score):
        self.font = pygame.font.Font('data/fonts/anfisa-grotesk.ttf', 100)
        self.display = False

        transp = pygame.Surface((WIDTH, HEIGHT))
        transp.fill(DARK_RED)

        win_text = self.font.render('Congratulations! You win!', False, WHITE)
        win_txt = self.font.render('Your score is {}!'.format(score), False, WHITE)
        text = self.font.render('Enter your name:', False, WHITE)
        running = True
        input_text = ''
        while running:
            pygame.display.update()
            screen.blit(transp, (0, 0))

            screen.blit(win_text, (250, 300))
            screen.blit(win_txt, (250, 420))
            screen.blit(text, (350, 600))

            need_input = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if need_input and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        menu(1, False)
                    elif event.key == pygame.K_RETURN:
                        need_input = False
                        add_record(input_text, score)
                        menu(1, False)
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        transp.fill(DARK_RED)
                    else:
                        if len(input_text) < 20:
                            input_text += event.unicode
            print_text(screen, input_text, 350, 700, WHITE)

    def start_round(self, filename):
        pygame.mouse.set_visible(False)
        round = Round((WIDTH, HEIGHT), filename, self.loss, self.loss_record, self.win)

        while self.display:
            pygame.display.update()
            round.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu(1, False)
            clock.tick(FPS)

        self.display = True


def show_records():
    sorted_dictionary = {}
    font = pygame.font.Font('data/fonts/anfisa-grotesk.ttf', 100)
    with open('data/records.json') as records:
        dictionary = json.load(records)
    sorted_values = sorted(dictionary.values())
    sorted_values.reverse()
    for index in sorted_values:
        for element in dictionary.keys():
            if dictionary[element] == index:
                sorted_dictionary[element] = dictionary[element]
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(DARK_RED)
    screen.blit(background, (0, 0))
    count = 0
    for record, score in sorted_dictionary.items():
        if count < 10:
            text = font.render('{}: {}'.format(record, score), False, WHITE)
            screen.blit(text, (400, 20 + 90 * count))
            count += 1
    running = True
    while running:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    running = False
                    menu(1, False)


def reference():
    with open('data/about.json') as records:
        dictionary = json.load(records)
    font = pygame.font.Font('data/fonts/anfisa-grotesk.ttf', 40)
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(DARK_RED)
    screen.blit(background, (0, 0))
    for number, text in dictionary.items():
        text = font.render(text, False, WHITE)
        screen.blit(text, (20, 20 + 90 * int(number)))
    running = True
    while running:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    running = False
                    menu(1, False)


def menu(level, next: bool):
    pygame.mouse.set_visible(True)
    display = True
    if next:
        button_start_game = Button('Next Round', 300, 110)
    else:
        button_start_game = Button('Start Game', 300, 110)
    button_records = Button('Records', 300, 110)
    button_reference = Button('Reference', 300, 110)
    button_exit = Button('Exit', 300, 110)
    font = pygame.font.Font('data/fonts/anfisa-grotesk.ttf', 200)
    transp = pygame.Surface((WIDTH, HEIGHT))
    transp.fill(DARK_RED)
    transp.set_alpha(5)

    arkanoid_text = font.render('ARKANOID', False, DARK_RED)
    while display:
        screen.blit(load_png('menu.png'), (0, 0))
        screen.blit(arkanoid_text, (200, 100))
        button_start_game.draw(screen, 450, 450, 20)
        button_records.draw(screen, 450, 590, 60)
        button_reference.draw(screen, 450, 730, 42)
        button_exit.draw(screen, 450, 870, 95)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_start_game.is_active():
                    sound_play(button_click_sound)
                    game = Game()
                    game.start_round('data/levels/level{}.json'.format(level))
                if button_records.is_active():
                    sound_play(button_click_sound)
                    show_records()
                if button_reference.is_active():
                    sound_play(button_click_sound)
                    reference()
                if button_exit.is_active():
                    sound_play(button_click_sound)
                    quit_game()
        clock.tick(FPS)
    pygame.quit()


def add_record(name, score):
    with open('data/records.json') as records:
        data = json.load(records)
    data[name] = score
    with open('data/records.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def set_min_score():
    with open('data/records.json') as records:
        data = json.load(records)
    sorted_values = sorted(data.values())
    min_score = sorted_values[0]
    with open('data/settings.json') as settings:
        info = json.load(settings)
    info['min_score'] = min_score
    with open('data/settings.json', 'w') as f:
        json.dump(info, f, ensure_ascii=False, indent=4)


def quit_game():
    sys.exit()


if __name__ == "__main__":
    menu(1, False)
