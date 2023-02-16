import pygame
import csv
import os
import sys
from copy import deepcopy
from random import choice, randrange


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board2 = [[0] * width for _ in range(height)]
        self.board = [[0] * width for _ in range(height)]
        self.colorboard = [[0] * width for _ in range(height)]
        self.next = [[0] * 4 for _ in range(4)]
        self.nc = 0
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color("#ffbcd9"), (
                    x * (self.cell_size + 1) + self.left, y * (self.cell_size + 1) + self.top, self.cell_size,
                    self.cell_size))
                if self.board[y][x] == 1:
                    color = self.colorboard[y][x]
                    pygame.draw.rect(screen, pygame.Color(color), (
                        x * (self.cell_size + 1) + self.left, y * (self.cell_size + 1) + self.top, self.cell_size,
                        self.cell_size))
                    pygame.draw.rect(screen, pygame.Color("white"), (x * (self.cell_size + 1) + self.left - 1,
                                                                     y * (self.cell_size + 1) + self.top - 1, self.cell_size + 2, self.cell_size + 2), 1)
        pygame.draw.rect(screen, pygame.Color("white"), (self.left, self.top, (self.cell_size + 1) * 10, (self.cell_size + 1) * 20), 1)
        for y in range(4):
            for x in range(4):
                if self.next[y][x] == 1:
                    color = self.nc
                else:
                    color = pygame.Color("#ffbcd9")
                pygame.draw.rect(screen, color, (
                    x * (self.cell_size + 1) + 400, y * (self.cell_size + 1) + 400, self.cell_size,
                    self.cell_size))

    def add_n(self, p, nc):
        self.next = [[0] * 4 for _ in range(4)]
        points = deepcopy(p)
        self.nc = nc
        n = 0
        n2 = 4
        for i in points:
            if i[1] < 0 and i[1] < n:
                n = i[1]
            if i[0] < n2:
                n2 = i[0]
        for i in points:
            i[0] -= n2
            i[1] += n * -1
            self.next[i[1]][i[0]] = 1

    def clear(self, coins):
        m = []
        for i in range(len(self.board2)):
            if self.board2[i] == [1] * 10:
                m.append(i)
        if m == []:
            return coins
        if len(m) == 1:
            coins += 100
        elif len(m) == 2:
            coins += 300
        elif len(m) == 3:
            coins += 700
        else:
            coins += 1500
        for i in m:
            self.board2[i] = [0] * 10
            self.colorboard[i] = [0] * 10
            self.board[i] = [0] * 10
        for i in range(len(self.board2) - 2, -1, -1):
            for t in range(i, len(self.board2) - 1):
                if self.board2[t + 1] == [0] * 10:
                    self.board2[t + 1] = deepcopy(self.board2[t])
                    self.colorboard[t + 1] = deepcopy(self.colorboard[t])
                    self.board[t + 1] = deepcopy(self.board[t])
                    self.board2[t] = [0] * 10
                    self.colorboard[t] = [0] * 10
                    self.board[t] = [0] * 10
        return coins

    def addpoints(self, points, coins):
        f = False
        for i in points:
            if i[1] < 0:
                f = True
                pass
            self.board2[i[1]][i[0]] = 1
        return self.clear(coins), f

    def check(self, m):
        for i in m:
            if i[1] >= 19:
                return True
            if 0 <= i[1] + 1 <= 19 and self.board2[i[1] + 1][i[0]] == 1:
                return True
        return False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


class Figura:
    def __init__(self, board):
        pass

    def move(self):
        a = True
        for i in self.points:
            if i[1] >= 19:
                a = False
                break
            if [i[0], i[1] + 1] not in self.points and self.board[i[1] + 1][i[0]] == 1 and i[1] + 1 >= 0:
                a = False
                break
        if a:
            for i in self.points:
                if i[1] >= 0:
                    self.board[i[1]][i[0]] = 0
                    self.colorboard[i[1]][i[0]] = 0
            for i in self.a:
                for t in i:
                    t[1] += 1
            for i in self.points:
                if i[1] >= 0:
                    self.board[i[1]][i[0]] = 1
                    self.colorboard[i[1]][i[0]] = self.color

    def right(self):
        s = True
        for i in self.points:
            if i[0] == 9:
                s = False
                break
            if i[0] > 8 or i[1] >= 0 and [i[0] + 1, i[1]] not in self.points and self.board[i[1]][i[0] + 1] == 1:
                s = False
                break
        if s:
            for i in self.points:
                if i[1] >= 0:
                    self.board[i[1]][i[0]] = 0
                    self.colorboard[i[1]][i[0]] = 0
            for i in self.a:
                for t in i:
                    t[0] += 1
            for i in self.points:
                if i[1] >= 0:
                    self.board[i[1]][i[0]] = 1
                    self.colorboard[i[1]][i[0]] = self.color

    def left(self):
        s = True
        for i in self.points:
            if i[0] == 0:
                s = False
                break
            if i[0] < 1 or i[1] >= 0 and [i[0] - 1, i[1]] not in self.points and self.board[i[1]][i[0] - 1] == 1:
                s = False
                break
        if s:
            for i in self.points:
                if i[1] >= 0:
                    self.board[i[1]][i[0]] = 0
                    self.colorboard[i[1]][i[0]] = 0
            for i in self.a:
                for t in i:
                    t[0] -= 1
            for i in self.points:
                if i[1] >= 0:
                    self.board[i[1]][i[0]] = 1
                    self.colorboard[i[1]][i[0]] = self.color

    def turn(self):
        if len(self.a) == 2:
            if self.points == self.a[0]:
                m = self.a[1]
            else:
                m = self.a[0]
        else:
            m = self.a[(self.a.index(self.points) + 1) % 4]
        s = True
        for i in m:
            if not 0 <= i[0] <= 9 or i[1] > 19:
                s = False
                break
            if i[1] >= 0 and i not in self.points and self.board[i[1]][i[0]] == 1:
                s = False
                break
        if s:
            for i in self.points:
                if i[1] >= 0:
                    self.board[i[1]][i[0]] = 0
                    self.colorboard[i[1]][i[0]] = 0
            self.points = m
            for i in self.points:
                if i[1] >= 0:
                    self.board[i[1]][i[0]] = 1
                    self.colorboard[i[1]][i[0]] = self.color


class A(Figura):
    def __init__(self, board, colorboard):
        self.a = [[[5, -1], [5, -2], [5, -3], [5, -4]], [[3, -2], [4, -2], [5, -2], [6, -2]]]
        self.color = pygame.Color("#ff9218")
        self.colorboard = colorboard
        self.points = choice(self.a)
        self.board = board

    def turn(self):
        if self.points == self.a[0]:
            m = self.a[1]
        else:
            m = self.a[0]
        s = True
        for i in m:
            if not 0 <= i[0] <= 9 or i[1] > 19:
                s = False
                break
            if i[1] >= 0 and self.board[i[1]][i[0]] == 1 and i not in self.points:
                s = False
                break
        if s:
            for i in self.points:
                if i[1] >= 0:
                    self.board[i[1]][i[0]] = 0
                    self.colorboard[i[1]][i[0]] = 0
            self.points = m
            for i in self.points:
                if i[1] >= 0 and i[0] >= 0:
                    self.board[i[1]][i[0]] = 1
                    self.colorboard[i[1]][i[0]] = self.color


class B(Figura):
    def __init__(self, board, colorboard):
        self.a = [[[4, -1], [5, -1], [4, -2], [5, -2]]]
        self.color = pygame.Color("#7fffd4")
        self.colorboard = colorboard
        self.points = self.a[0]
        self.board = board

    def turn(self):
        pass


class C(Figura):
    def __init__(self, board, colorboard):
        self.a = [[[4, -2], [5, -2], [6, -2], [5, -3]], [[5, -1], [5, -2], [6, -2], [5, -3]],
                  [[5, -1], [4, -2], [5, -2], [6, -2]], [[5, -1], [4, -2], [5, -2], [5, -3]]]
        self.color = pygame.Color("#ff77ff")
        self.colorboard = colorboard
        self.points = choice(self.a)
        self.board = board


class D(Figura):
    def __init__(self, board, colorboard):
        self.a = [[[5, -1], [5, -2], [5, -3], [6, -3]], [[4, -2], [5, -2], [6, -2], [6, -1]],
                  [[5, -3], [5, -2], [4, -1], [5, -1]], [[4, -3], [4, -2], [5, -2], [6, -2]]]
        self.color = pygame.Color("purple")
        self.colorboard = colorboard
        self.points = choice(self.a)
        self.board = board


class E(Figura):
    def __init__(self, board, colorboard):
        self.a = [[[5, -1], [5, -2], [5, -3], [4, -3]], [[4, -2], [5, -2], [6, -2], [6, -3]],
                  [[5, -3], [5, -2], [5, -1], [6, -1]], [[4, -1], [4, -2], [5, -2], [6, -2]]]
        self.color = pygame.Color("#008cf0")
        self.colorboard = colorboard
        self.points = choice(self.a)
        self.board = board


class F(Figura):
    def __init__(self, board, colorboard):
        self.a = [[[4, -1], [4, -2], [5, -2], [5, -3]], [[4, -3], [5, -3], [5, -2], [6, -2]]]
        self.color = pygame.Color("#ffd700")
        self.colorboard = colorboard
        self.points = choice(self.a)
        self.board = board


class G(Figura):
    def __init__(self, board, colorboard):
        self.a = [[[5, -1], [5, -2], [4, -2], [4, -3]], [[4, -2], [5, -3], [5, -2], [6, -3]]]
        self.color = pygame.Color("#54ff9f")
        self.colorboard = colorboard
        self.points = choice(self.a)
        self.board = board


def bestr():
    with open("coins.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        return next(reader)[0]


def savebestr(res):
    with open("coins.csv", "w", encoding="utf8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([res])


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def start_screen(screen, screen_size, clock):
    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 700
    string_rendered = font.render("Нажмите на экране чтобы начать", 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 140
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(50)


def main(start=True):
    pygame.init()
    screen_size = 600, 800
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Тетрис')
    clock = pygame.time.Clock()
    if start:
        start_screen(screen, screen_size, clock)
    board = Board(10, 20)
    board.set_view(10, 10, 30)
    mas = [A, B, C, D, E, F, G]
    nf = choice(mas)(board.board, board.colorboard)
    board.add_n(nf.points, nf.color)
    f = choice(mas)(board.board, board.colorboard)
    running = 1
    counter = 0
    coins = 0
    turn = False
    right = False
    left = False
    down = False
    mv = True
    finish = False
    speed = 8
    sp = 0
    while running:
        mv = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    mv = False
                    if not finish:
                        f.turn()
                    turn = True
                if event.key == pygame.K_RIGHT:
                    mv = False
                    if not finish:
                        f.right()
                    right = True
                if event.key == pygame.K_LEFT:
                    mv = False
                    if not finish:
                        f.left()
                    left = True
                if event.key == pygame.K_DOWN:
                    mv = False
                    if not finish:
                        f.move()
                    down = True
                if event.key == pygame.K_SPACE:
                    main(start=False)
                    sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    turn = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_DOWN:
                    down = False
        if not finish:
            screen.fill(pygame.Color("#fcfcee"))
            if counter % (speed / 2 - 3) == 0:
                if turn and mv:
                    f.turn()
                if right and mv:
                    f.right()
                if left and mv:
                    f.left()
            if down and mv:
                f.move()
            if counter % 4 == 0:
                f.move()
                if board.check(f.points):
                    coins, finish = board.addpoints(f.points, coins)
                    if finish:
                        t = pygame.font.Font(None, 30)
                        t = t.render("Игра окончена, чтобы начать заново нажмите пробел", True, (0, 100, 0))
                        p = t.get_rect(center=(290, 700))
                        screen.blit(t, p)
                    coins += 10
                    if coins > int(bestr()):
                        savebestr(coins)
                    if coins >= 1000 and sp == 0:
                        speed += 2
                        sp = 1
                    if coins >= 3000 and sp == 1:
                        speed += 2
                        sp = 2
                    if coins >= 7000 and sp == 2:
                        speed += 2
                        sp = 3
                    if coins >= 15000 and sp == 3:
                        speed += 2
                        sp = 4
                    f = nf
                    nf = choice(mas)(board.board, board.colorboard)
                    board.add_n(nf.points, nf.color)
            text = pygame.font.Font(None, 50)
            text = text.render("Очки: " + str(coins), True, (0, 100, 0))
            place = text.get_rect(center=(450, 150))
            text1 = pygame.font.Font(None, 35)
            text1 = text1.render("Лучший результат:", True, (0, 100, 0))
            place1 = text1.get_rect(center=(450, 50))
            text2 = pygame.font.Font(None, 40)
            text2 = text2.render(bestr(), True, (0, 100, 0))
            place2 = text2.get_rect(center=(450, 90))
            screen.blit(text, place)
            screen.blit(text1, place1)
            screen.blit(text2, place2)
            text3 = pygame.font.Font(None, 35)
            text3 = text3.render("Следующая фигура:", True, (0, 100, 0))
            place3 = text3.get_rect(center=(460, 350))
            screen.blit(text3, place3)
            board.render(screen)
            pygame.display.flip()
            clock.tick(speed)
            counter += 1
    pygame.quit()


if __name__ == "__main__":
    main()
