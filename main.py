import pygame
import os
import sys
from random import choice
import sqlite3

con = sqlite3.connect("names.db")
cur = con.cursor()
username = ''


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image_1 = pygame.image.load(fullname)
    if colorkey is not None:
        image_1 = image_1.convert()
        if colorkey == -1:
            colorkey = image_1.get_at((0, 0))
        image_1.set_colorkey(colorkey)
    else:
        image_1 = image_1.convert_alpha()
    return image_1


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0, 0, 0, -1, 0, 0, 0] for _ in range(height)]
        self.randomizer_start()
        self.left = 10
        self.top = 10
        self.cell_size = 50
        self.left = 0
        self.top = 0
        self.cell_size = 50
        self.counter = 0
        self.counter_seconds = 0
        self.delta = 60

    def render(self, screen):
        global counter
        left, top, size = self.left, self.top, self.cell_size
        i = 0
        for row in self.board:
            for el in row:
                if el == -1:
                    image = load_image('tree.png')
                    screen.blit(image, (left, top))
                elif el == 0:
                    image = load_image(f'background/background_{i}.jpg')
                    screen.blit(image, (left, top))
                elif el == 1:
                    image = load_image(f'background/background_{i}.jpg')
                    screen.blit(image, (left, top))
                    image = load_image('vetka.png')
                    screen.blit(image, (left, top + 20))
                elif el == 2:
                    image = load_image(f'background/background_{i}.jpg')
                    screen.blit(image, (left, top))
                    image = load_image(f'улитка_правая.png', -1)
                    screen.blit(image, (left, top))
                elif el == 3:
                    image = load_image(f'background/background_{i}.jpg')
                    screen.blit(image, (left, top))
                    image = load_image(f'улитка_левая.png', -1)
                    screen.blit(image, (left, top))
                left += size
                i += 1
            top += size
            left = self.left
        pygame.draw.rect(screen, color_1,
                         (115, 20, 120, 20), 0)
        if self.delta < 0:
            self.delta = 0
        pygame.draw.rect(screen, color_2,
                         (115, 20, 120 - self.delta, 20), 0)


    def randomizer_start(self):
        for i in range(10):
            pos = choice([1, 2])
            size_vetki = choice([1, 2])
            for j in range(7):
                if j == 3:
                    self.board[i][j] = -1
                elif j == 0 or j == 6 or i == 9 or i == 8 or i == 7:
                    self.board[i][j] = 0
                elif j == 1 and pos == 1 and size_vetki == 2:
                    self.board[i][j] = 1
                elif j == 2 and pos == 1:
                    self.board[i][j] = 1
                elif j == 4 and pos == 2:
                    self.board[i][j] = 1
                elif j == 5 and pos == 2 and size_vetki == 2:
                    self.board[i][j] = 1
                if i != 0:
                    if 1 in self.board[i - 1]:
                        self.board[i] = [0, 0, 0, -1, 0, 0, 0]
            self.board[9][4] = 2

    def randomizer(self):
        board_copy = self.board[:-1]
        pos = choice([1, 2])
        size_vetki = choice([1, 2])
        d = []
        if not(1 in board_copy[0]):
            if pos == 1 and size_vetki == 2:
                d = [0, 1, 1, -1, 0, 0, 0]
            elif pos == 1 and size_vetki == 1:
                d = [0, 0, 1, -1, 0, 0, 0]
            elif pos == 2 and size_vetki == 1:
                d = [0, 0, 0, -1, 1, 0, 0]
            elif pos == 2 and size_vetki == 2:
                d = [0, 0, 0, -1, 1, 1, 0]
        else:
            d = [0, 0, 0, -1, 0, 0, 0]
        board_new = []
        board_new.append(d)
        for el in board_copy:
            board_new.append(el)
        if self.board[9][2] == 3:
            board_new[9][2] = 3
            board_new[9][1] = 0
        if self.board[9][4] == 2:
            board_new[9][4] = 2
            board_new[9][5] = 0
        self.board = board_new


def draw_intro():
    global username
    font = pygame.font.SysFont('Comic Sans MS', 20)
    font_2 = pygame.font.SysFont('Comic Sans MS', 30)
    is_find_name = True
    name = ''
    r = cur.execute("""SELECT name, score FROM name_score""").fetchall()
    top_1 = 0
    top_1_name = ''
    top_2 = 0
    top_2_name = ''
    top_3 = 0
    top_3_name = ''
    top_4 = 0
    top_4_name = ''
    top_5 = 0
    top_5_name = ''
    for result in r:
        if result[1] >= top_1:
            top_1, top_2, top_3, top_4, top_5 = result[1], top_1, top_2, top_3, top_4
            top_1_name, top_2_name, top_3_name, top_4_name, top_5_name = result[0], top_1_name, top_2_name,\
                                                                         top_3_name, top_4_name
        elif result[1] >= top_2:
            top_1, top_2, top_3, top_4, top_5 = top_1, result[1], top_2, top_3, top_4
            top_1_name, top_2_name, top_3_name, top_4_name, top_5_name = top_1_name, result[0], top_2_name,\
                                                                         top_3_name, top_4_name
        elif result[1] >= top_3:
            top_1, top_2, top_3, top_4, top_5 = top_1, top_2, result[1], top_3, top_4
            top_1_name, top_2_name, top_3_name, top_4_name, top_5_name = top_1_name, top_2_name, result[0],\
                                                                         top_3_name, top_4_name
        elif result[1] >= top_4:
            top_1, top_2, top_3, top_4, top_5 = top_1, top_2, top_3, result[1], top_4
            top_1_name, top_2_name, top_3_name, top_4_name, top_5_name = top_1_name, top_2_name,\
                                                                         top_3_name, result[0], top_4_name
        elif result[1] > top_2:
            top_1, top_2, top_3, top_4, top_5 = top_1, top_2, top_3, top_4, result[1]
            top_1_name, top_2_name, top_3_name, top_4_name, top_5_name = top_1_name, top_2_name,\
                                                                         top_3_name, top_4_name, result[0]
    top_list_names = [top_1_name, top_2_name, top_3_name, top_4_name, top_5_name]
    top_list_score = [top_1, top_2, top_3, top_4, top_5]
    top_list = ['1 место: ', '2 место: ', '3 место: ', '4 место: ', '5 место: ']
    pravila = ['Правила:', 'Цель игры: достичь как можно', 'большего счёта. Счёт набивается ',
               'при уклонений от веток дерева.',
               'Уклонение происходит при', 'нажатии клавиш "a" и "d" или', 'стрелочками. Пять',
               'лучших результатов попадают',
               'в список лидеров.', 'Для начала игры введите имя ', '(больше 2 символов) и', 'нажмите Enter']
    while is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and len(name) < 20:
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN and 2 < len(name):
                    username = name
                    is_find_name = False
                    break
        image = load_image('background.jpg')
        screen.blit(image, (0, 0))
        text = font_2.render('Лучшие игроки:', True, 'RED')
        screen.blit(text, (10, 5))
        pos = 40
        for i in range(5):
            if i == 0:
                text = font.render(top_list[i] + top_list_names[i] + ' - ' + str(top_list_score[i]), True,
                                   (255, 215, 0))
            elif i == 1:
                text = font.render(top_list[i] + top_list_names[i] + ' - ' + str(top_list_score[i]), True,
                                   (192, 192, 192))
            elif i == 2:
                text = font.render(top_list[i] + top_list_names[i] + ' - ' + str(top_list_score[i]), True,
                                   (177, 86, 15))
            else:
                text = font.render(top_list[i] + top_list_names[i] + ' - ' + str(top_list_score[i]), True, 'BLACK')
            screen.blit(text, (10, pos))
            pos += 20
        pos -= 20
        for i in pravila:
            if 'Правила:' == i:
                text = font_2.render(i, True, 'RED')
                pos += 20
                screen.blit(text, (10, pos))
                pos += 15
            else:
                text = font.render(i, True, 'BLACK')
                pos += 20
                screen.blit(text, (10, pos))
        pygame.draw.rect(screen, 'BLACK', (5, pos - 195, 330, 220), 1)
        pos += 20
        text_surface_name = font_2.render('Введите имя:', True, 'Red')
        screen.blit(text_surface_name, (10, pos))
        pos += 25
        text_surface_name = font_2.render(name, True, 'BLACK')
        screen.blit(text_surface_name, (10, pos))
        pygame.draw.rect(screen, 'BLACK', (5, pos + 13, 330, 30), 1)
        pygame.display.flip()


def draw_end():
    global username
    font = pygame.font.SysFont('Comic Sans MS', 20)
    font_2 = pygame.font.SysFont('Comic Sans MS', 25)
    is_find_name = True
    r = cur.execute("""SELECT name, score FROM name_score""").fetchall()
    top_1 = 0
    top_1_name = ''
    top_2 = 0
    top_2_name = ''
    top_3 = 0
    top_3_name = ''
    top_4 = 0
    top_4_name = ''
    top_5 = 0
    top_5_name = ''
    for result in r:
        if result[1] >= top_1:
            top_1, top_2, top_3, top_4, top_5 = result[1], top_1, top_2, top_3, top_4
            top_1_name, top_2_name, top_3_name, top_4_name, top_5_name = result[0], top_1_name, top_2_name,\
                                                                         top_3_name, top_4_name
        elif result[1] >= top_2:
            top_1, top_2, top_3, top_4, top_5 = top_1, result[1], top_2, top_3, top_4
            top_1_name, top_2_name, top_3_name, top_4_name, top_5_name = top_1_name, result[0], top_2_name,\
                                                                         top_3_name, top_4_name
        elif result[1] >= top_3:
            top_1, top_2, top_3, top_4, top_5 = top_1, top_2, result[1], top_3, top_4
            top_1_name, top_2_name, top_3_name, top_4_name, top_5_name = top_1_name, top_2_name, result[0],\
                                                                         top_3_name, top_4_name
        elif result[1] >= top_4:
            top_1, top_2, top_3, top_4, top_5 = top_1, top_2, top_3, result[1], top_4
            top_1_name, top_2_name, top_3_name, top_4_name, top_5_name = top_1_name, top_2_name,\
                                                                         top_3_name, result[0], top_4_name
        elif result[1] > top_2:
            top_1, top_2, top_3, top_4, top_5 = top_1, top_2, top_3, top_4, result[1]
            top_1_name, top_2_name, top_3_name, top_4_name, top_5_name = top_1_name, top_2_name,\
                                                                         top_3_name, top_4_name, result[0]
    top_list_names = [top_1_name, top_2_name, top_3_name, top_4_name, top_5_name]
    top_list_score = [top_1, top_2, top_3, top_4, top_5]
    top_list = ['1 место: ', '2 место: ', '3 место: ', '4 место: ', '5 место: ']
    best_result = cur.execute(f"""SELECT score FROM name_score WHERE name = '{username}' """).fetchall()
    best_result = int(str(best_result)[2:-3])
    while is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_find_name = False
                    break
        image = load_image('background.jpg')
        screen.blit(image, (0, 0))
        text = font_2.render('Лучшие игроки:', True, 'RED')
        screen.blit(text, (10, 5))
        pos = 40
        for i in range(5):
            if i == 0:
                text = font.render(top_list[i] + top_list_names[i] + ' - ' + str(top_list_score[i]), True,
                                   (255, 215, 0))
            elif i == 1:
                text = font.render(top_list[i] + top_list_names[i] + ' - ' + str(top_list_score[i]), True,
                                   (192, 192, 192))
            elif i == 2:
                text = font.render(top_list[i] + top_list_names[i] + ' - ' + str(top_list_score[i]), True,
                                   (177, 86, 15))
            else:
                text = font.render(top_list[i] + top_list_names[i] + ' - ' + str(top_list_score[i]), True, 'BLACK')
            screen.blit(text, (10, pos))
            pos += 20
        pos += 20
        if best_result != counter_touch - 1:
            text = font.render(f'Ваш лучший результат: {best_result}', True, 'BLACK')
            screen.blit(text, (10, pos))
            pos += 30
            text = font.render(f'Ваш набитый сейчас счёт: {counter_touch - 1}', True, 'BLACK')
            screen.blit(text, (10, pos))
            pos += 40
        else:
            text = font.render('Поздравляю вы побили рекорд!!!', True, 'BLACK')
            screen.blit(text, (10, pos))
            pos += 30
            text = font.render(f'Ваш новый лучший результат: {best_result}', True, 'BLACK')
            screen.blit(text, (10, pos))
            pos += 40
        t = ['Для повторной игры', 'нажмите Enter']
        for i in t:
            text = font.render(i, True, 'BLACK')
            screen.blit(text, (10, pos))
            pos += 20
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    size = width, height = 350, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Моя игра')
    running = True
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    board = Board(7, 10)
    color_1 = pygame.Color('white')
    color_2 = pygame.Color('red')
    timer_event = pygame.USEREVENT + 1
    timer_event_2 = pygame.USEREVENT + 2
    pygame.time.set_timer(timer_event, 250)
    pygame.font.init()
    clock = pygame.time.Clock()
    counter_touch = 0
    counter = 0
    print_level = False
    draw_intro()
    game = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == timer_event:
                if counter_touch != 0:
                    board.delta += 2 + (counter_touch // 15)
            if event.type == timer_event_2:
                counter += 1
                print_level = True
            if event.type == pygame.KEYDOWN:
                if event.key == 97 or event.key == pygame.K_LEFT:
                    counter_touch += 1
                    if board.board[8][2] == 1 or board.board[9][2] == 1:
                        game = False
                    else:
                        board.board[9][2] = 3
                        board.board[9][4] = 0
                        board.delta -= 7
                        board.randomizer()
                elif event.key == 100 or event.key == pygame.K_RIGHT:
                    counter_touch += 1
                    if board.board[8][4] == 1 or board.board[9][4] == 1:
                        game = False
                    else:
                        board.board[9][2] = 0
                        board.board[9][4] = 2
                        board.delta -= 7
                        board.randomizer()
        if board.delta >= 120:
            game = False
        screen.fill((255, 255, 255))
        board.render(screen)
        if counter_touch % 15 == 0 and counter_touch != 0:
            pygame.time.set_timer(timer_event_2, 250)
        text_surface = my_font.render(str(counter_touch), False, (0, 0, 0))
        screen.blit(text_surface, (156, 50))
        if print_level:
            if counter != 5:
                text_surface_2 = my_font.render('level' + str(counter_touch // 15), False, (0, 0, 0))
                screen.blit(text_surface_2, (156, 80))
                pygame.display.flip()
            else:
                counter = 0
                pygame.time.set_timer(timer_event_2, 0)
                print_level = False
        if game == False:
            counter = 0
            print_level = False
            game = True
            board = Board(7, 10)

            r = cur.execute("""SELECT name FROM name_score""").fetchall()
            if username in [str(i)[2:-3] for i in r]:
                k = cur.execute(f"""SELECT score FROM name_score WHERE name = '{username}' """).fetchall()
                k = int(str(k)[2:-3])
                if counter_touch - 1 > k:
                    cur.execute(f'''UPDATE name_score SET score = {counter_touch - 1} WHERE name = '{username}' ''')
                    con.commit()
            else:
                cur.execute(f"INSERT INTO name_score(name,score) VALUES('{username}',{counter_touch - 1}) ")
                con.commit()

            draw_end()
            counter_touch = 0
        pygame.display.flip()
    pygame.quit()
