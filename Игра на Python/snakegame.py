import pygame


pygame.init()

win = pygame.display.set_mode(((1360, 640)))
pygame.display.set_caption(("zme9 ebana9"))

x = 500
y = 500
widht = 50
height = 60
speed = 15
run = True
while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_DOWN]:
        y += speed
    if keys[pygame.K_UP]:
        y -= speed
    pygame.draw.circle(win, (255, 255, 255), (x, y), 10, 0)
    pygame.display.update()
pygame.quit()
