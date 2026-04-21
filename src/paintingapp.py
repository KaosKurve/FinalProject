import pygame
pygame.init()

fps = 60
timer = pygame.time.Clock()
Width = 800
Height = 600
active_size = 0
active_color = 'white'

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
    brush_list = [xl_brush, l_brush, m_brush, s_brush]

    blue = pygame.draw.rect(screen, (0, 0, 255), [Width - 35, 10, 25, 25])
    red = pygame.draw.rect(screen, (255, 0, 0), [Width - 35, 35, 25, 25])
    green = pygame.draw.rect(screen, (0, 255, 0), [Width - 60, 10, 25, 25])
    yellow = pygame.draw.rect(screen, (255, 255, 0), [Width - 60, 35, 25, 25])
    teal = pygame.draw.rect(screen, (0, 255, 255), [Width - 85, 10, 25, 25])
    purple = pygame.draw.rect(screen, (255, 0, 255), [Width - 85, 35, 25, 25])
    white = pygame.draw.rect(screen, (0, 0, 0), [Width - 110, 10, 25, 25])
    black = pygame.draw.rect(screen, (255, 255, 255), [Width - 110, 35, 25, 25])
    color_rect = [blue, red, green, yellow, teal, purple, white, black]
    rgb_list = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0),
                (0, 255, 255), (255, 0, 255),(0, 0, 0), (255, 255, 255)]
    return brush_list, color_rect, rgb_list


run = True
while run:
    timer.tick(fps)
    screen.fill('white')
    mouse = pygame.mouse.get_pos()
    brushes, colors, rgbs = draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(brushes)):
                if brushes[i].collidepoint(event.pos):
                    active_size = 20 - (i * 5)
            
            for i in range(len(colors)):
                if colors[i].collidepoint(event.pos):
                    active_color = rgbs[i]

    pygame.display.flip()
pygame.quit()