import pygame
import random
import sys
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
sizeoknox = 600
sizeoknoy = 600
fps = 10
xs = [300, 300, 300, 300, 300]
ys = [300, 280, 260, 240, 220]


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

        one = f.render('Конец игры. Ваш счёт : ' + str(score), True, (0, 0, 0))
        two = f.render('Для начала новой игры - нажмите Пробел', True, (0, 0, 0))
        three = f.render('Для выхода в меню - нажмине M', True, (0, 0, 0))
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

        screen = pygame.display.set_mode((sizeoknox, sizeoknoy))
        screen.fill((0, 255, 255))
        pygame.display.set_caption('Snake.Menu_loop')

        f = pygame.font.SysFont('New Times Roman', 30)

        one = f.render('Для начала новой игры нажмите 1', True, (0, 0, 0))
        two = f.render('Для выхода из игры - нажмите 0', True, (0, 0, 0))
        three = f.render('Version : demo v0.1', True, (0, 0, 0))

        screen.blit(one, (60, 300))
        screen.blit(two, (60, 320))
        screen.blit(three, (60, 340))

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

        # screen = pygame.display.set_mode((sizeoknox, sizeoknoy))
        screen.fill((0, 255, 255))
        pygame.display.set_caption('Snake.Pause_loop')

        f = pygame.font.SysFont('New Times Roman', 30)

        one = f.render('Pause loop', True, (0, 0, 0))
        two = f.render('Для продолжения - нажмите ESC', True, (0, 0, 0))
        three = f.render('Для выхода в меню - нажмите M', True, (0, 0, 0))
        four = f.render('Version : demo v0.1', True, (0, 0, 0))

        screen.blit(one, (60, 300))
        screen.blit(two, (60, 320))
        screen.blit(three, (60, 340))
        screen.blit(four, (60, 3600))


        pygame.display.update()
        clock.tick(1)


appleimage = pygame.Surface((20, 20))
appleimage.fill((0, 255, 0))

img = pygame.Surface((20, 20))
img=pygame.image.load("saturn_family1.jpg").convert()




def game_loop(screen):
    global sizeoknox, sizeoknoy, clock, fps, dirs, score
    # Следующие переменные для обнуления игры и начать заного
    score = 0
    xs = [300, 300, 300, 300, 300]
    ys = [300, 280, 260, 240, 220]
    fps = 10
    dirs = 0
    #

    applepos = (random.randint(30, 600 - 10), random.randint(30, 600 - 10))
    screen = pygame.display.set_mode((sizeoknox, sizeoknoy))

    pygame.display.set_caption('Snake')



    while True:
        clock.tick(fps)
        screen.fill((255, 255, 255))

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
            xs.append(700)
            ys.append(700)
            applepos = (random.randint(0, sizeoknox), random.randint(0, sizeoknoy))
        if xs[0] < 0 or xs[0] > sizeoknox or ys[0] < 0 or ys[0] > sizeoknoy:
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
        screen.blit(appleimage, applepos)
        f = pygame.font.SysFont('Arial', 20)
        t = f.render('Твой счёт : ' + str(score), True, (0, 0, 0))
        screen.blit(t, (10, 10))
        pygame.display.update()


def __main__():
    menu_loop()


if __name__ == '__main__':
    __main__()
