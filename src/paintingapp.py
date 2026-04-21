import pygame
pygame.init()

fps = 60
timer = pygame.time.Clock()
Width = 800
Height = 600


screen = pygame.display.set_mode([Width, Height])
pygame.display.set_caption('Paint!')


run = True
while run:
    timer.tick(fps)
    screen.fill('white')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()