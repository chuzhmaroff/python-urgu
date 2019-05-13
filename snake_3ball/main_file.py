import pygame
import random
import sys
from pygame.locals import *

# 500 × 889
pygame.init()
clock = pygame.time.Clock()
x_window = 650
y_window = 650
fps = 10
xs = [300, 300, 300, 300, 300]
ys = [300, 280, 260, 240, 220]
background = pygame.image.load("6.jpg")
screen = pygame.display.set_mode((x_window, y_window))
img = pygame.Surface((20, 20))
img = pygame.image.load("snake.png").convert()

appleimage = pygame.Surface((20, 20))
appleimage = pygame.image.load("apple.jpg").convert()


def collision(x1, x2, y1, y2, w1, w2, h1, h2):
    if x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2:
        return True
    else:
        return False


def die(screen, score):
    global clock
    die = True
    while die:
        for direct in pygame.event.get():
            if direct.type == QUIT:
                sys.exit(0)
            elif direct.type == KEYDOWN:
                if direct.key == pygame.K_m:
                    menu_loop()
                elif direct.key == pygame.K_SPACE:
                    game_loop(screen)

        screen.fill((0, 255, 255))
        pygame.display.set_caption('Snake.Died_loop')

        f = pygame.font.SysFont('New Times Roman', 30)

        one = f.render('End of the game. Your game score : ' + str(score), True, (0, 0, 0))
        two = f.render('To start a new game - press Space.', True, (0, 0, 0))
        three = f.render('To exit the menu - press M', True, (0, 0, 0))
        screen.blit(one, (15, 300))
        screen.blit(two, (15, 320))
        screen.blit(three, (15, 340))

        pygame.display.update()
        clock.tick(10)


def menu_loop():
    global clock, screen
    menu_running = True

    while menu_running:
        for direct in pygame.event.get():
            if direct.type == QUIT:
                sys.exit(0)
            elif direct.type == KEYDOWN:
                if direct.key == pygame.K_1:
                    game_loop(screen)
                elif direct.key == pygame.K_0:
                    pygame.quit()
                    sys.exit()
                elif direct.key == pygame.K_h:
                    rules_loop(screen)
                elif direct.key == pygame.K_s:
                    tablescore_loop(screen)

        screen = pygame.display.set_mode((x_window, y_window))
        screen.fill((0, 255, 255))
        pygame.display.set_caption('Snake.Menu_loop')

        f = pygame.font.SysFont('New Times Roman', 30)

        one = f.render('To start a new game, press 1', True, (0, 0, 0))
        two = f.render('To exit the game - press 0', True, (0, 0, 0))
        three = f.render('Rules game - press button H', True, (0, 0, 0))
        four = f.render('Open score table - press button S', True, (0, 0, 0))
        five = f.render('Version : demo v0.1', True, (0, 0, 0))

        screen.blit(one, (30, 100))
        screen.blit(two, (30, 120))
        screen.blit(three, (30, 140))
        screen.blit(four, (30, 160))
        screen.blit(five, (30, 180))

        pygame.display.update()
        clock.tick(10)


def tablescore_loop(screen):
    f = pygame.font.SysFont('New Times Roman', 30)
    tablescore_running = True

    while tablescore_running:
        for direct in pygame.event.get():
            if direct.type == QUIT:
                sys.exit(0)
            elif direct.type == KEYDOWN:
                if direct.key == pygame.K_ESCAPE:
                    menu_loop()

    one = f.render('The points table will work in the next update', True, (0, 0, 0))
    screen.blit(one, (30, 100))

    pygame.display.update()
    clock.tick(10)


def pause_loop(screen):
    global clock
    pause_running = True

    while pause_running:
        for direct in pygame.event.get():
            if direct.type == QUIT:
                sys.exit(0)
            elif direct.type == KEYDOWN:
                if direct.key == pygame.K_ESCAPE:
                    pause_running = False
                elif direct.key == pygame.K_m:
                    pause_running = False
                    menu_loop()

        # screen = pygame.display.set_mode((x_window, y_window))
        screen.fill((0, 255, 255))
        pygame.display.set_caption('Snake.Pause_loop')

        f = pygame.font.SysFont('New Times Roman', 30)

        one = f.render('Pause loop', True, (0, 0, 0))
        two = f.render('To continue - press ESC', True, (0, 0, 0))
        three = f.render('To enter the menu - press M', True, (0, 0, 0))
        four = f.render('Version : demo v0.1', True, (0, 0, 0))

        screen.blit(one, (30, 100))
        screen.blit(two, (30, 120))
        screen.blit(three, (30, 140))
        screen.blit(four, (30, 160))

        pygame.display.update()
        clock.tick(1)


def rules_loop(screen):
    rules_running = True

    while rules_running:
        for direct in pygame.event.get():
            if direct.type == QUIT:
                sys.exit(0)
            elif direct.type == KEYDOWN:
                if direct.key == pygame.K_ESCAPE:
                    rules_running = False

        # screen = pygame.display.set_mode((x_window, y_window))
        screen.fill((0, 255, 255))
        pygame.display.set_caption('Snake.Rules_loop')

        f = pygame.font.SysFont('New Times Roman', 30)

        one = f.render('In this application, a realized game called snake', True, (0, 0, 0))
        two = f.render('You are a snake. Your task is to eat as many apples as possible.', True, (0, 0, 0))
        three = f.render('Management takes place by pressing keys', True, (0, 0, 0))
        four = f.render('Up and down arrows left', True, (0, 0, 0))
        five = f.render('To close the rules, click ESC.', True, (0, 0, 0))

        screen.blit(one, (30, 100))
        screen.blit(two, (30, 120))
        screen.blit(three, (30, 140))
        screen.blit(four, (30, 160))
        screen.blit(five, (30, 180))

        pygame.display.update()


def game_loop(screen):
    global x_window, y_window, clock, fps, dirs
    # Следующие переменные для обнуления игры и начать заного
    score = 0
    xs = [300, 300, 300, 300, 300]
    ys = [300, 280, 260, 240, 220]
    fps = 10
    dirs = 0
    #

    applepos = (random.randint(30, x_window - 10), random.randint(30, y_window - 10))
    pygame.display.set_caption('Snake')

    while True:
        # screen.blit(background,[0,0])
        screen.fill((255, 255, 255))
        clock.tick(fps)
        screen.blit(appleimage, applepos)
        for direct in pygame.event.get():
            if direct.type == QUIT:
                sys.exit(0)
            elif direct.type == KEYDOWN:
                if direct.key == K_UP and dirs != 0:
                    dirs = 2
                elif direct.key == K_DOWN and dirs != 2:
                    dirs = 0
                elif direct.key == K_LEFT and dirs != 1:
                    dirs = 3
                elif direct.key == K_RIGHT and dirs != 3:
                    dirs = 1
                elif direct.key == pygame.K_ESCAPE:
                    pause_loop(screen)

        i = len(xs) - 1
        while i >= 2:
            if collision(xs[0], xs[i], ys[0], ys[i], 20, 20, 20, 20):
                die(screen, score)
            i -= 1
        if collision(xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):
            score += 1
            fps += 0.5
            xs.append(1)
            ys.append(1)
            applepos = (random.randint(30, x_window - 30), random.randint(30, y_window - 30))
        if xs[0] <= 0 or xs[0] >= x_window or ys[0] <= 0 or ys[0] >= y_window:
            die(screen, score)
        i = len(xs) - 1
        while i >= 1:
            xs[i] = xs[i - 1]
            ys[i] = ys[i - 1]
            i -= 1
        if dirs == 0:
            ys[0] += 20
        elif dirs == 1:
            xs[0] += 20
        elif dirs == 2:
            ys[0] -= 20
        elif dirs == 3:
            xs[0] -= 20
        for i in range(0, len(xs)):
            screen.blit(img, (xs[i], ys[i]))
        f = pygame.font.SysFont('Arial', 20)
        one = f.render('You scores : ' + str(score), True, (0, 0, 0))
        two = f.render('You speed : ' + str(fps), True, (0, 0, 0))
        screen.blit(one, (10, 10))
        screen.blit(two, (450, 10))
        pygame.display.update()
        screen.fill((255, 255, 255))


def __main__():
    menu_loop()


if __name__ == '__main__':
    __main__()
