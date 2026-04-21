import pygame
pygame.init()

fps = 60
timer = pygame.time.Clock()
Width = 800
Height = 600


screen = pygame.display.set_mode([Width, Height])
pygame.display.set_caption('Paint!')


def draw_menu():
    pygame.draw.rect(screen, 'gray', [0, 0 , Width, 70])
    pygame.draw.line(screen, 'black', (0, 70), (Width, 70), 3)
    xl_brush = pygame.draw.rect(screen, 'black', [10, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (35, 35), 20)
    l_brush = pygame.draw.rect(screen, 'black', [70, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (95, 35), 15)
    m_brush = pygame.draw.rect(screen, 'black', [130, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (155, 35), 10)
    s_brush = pygame.draw.rect(screen, 'black', [190, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (215, 35), 5)

    

run = True
while run:
    timer.tick(fps)
    screen.fill('white')

    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()