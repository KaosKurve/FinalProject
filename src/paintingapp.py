import pygame
pygame.init()

fps = 240
timer = pygame.time.Clock()
Width = 800
Height = 600
active_size = 0
active_color = 'white'
active_tool = 'brush'
screen = pygame.display.set_mode([Width, Height])
pygame.display.set_caption('My Painting App!')
canvas = pygame.Surface((Width, Height))
canvas.fill("white")
undo_stack = []
redo_stack = []
drawingstroke = False


def draw_menu(size, color, tool):
    pygame.draw.rect(screen, 'gray', [0, 0 , Width, 70])
    pygame.draw.line(screen, 'black', (0, 70), (Width, 70), 3)

    #brush sizes
    xl_brush = pygame.draw.rect(screen, 'black', [10, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (35, 35), 20)
    l_brush = pygame.draw.rect(screen, 'black', [70, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (95, 35), 15)
    m_brush = pygame.draw.rect(screen, 'black', [130, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (155, 35), 10)
    s_brush = pygame.draw.rect(screen, 'black', [190, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (215, 35), 5)
    eraser = pygame.draw.rect(screen, 'black', [250, 10, 50, 50])
    pygame.draw.rect(screen, 'white', (260, 15, 30, 40), width = 4, border_top_left_radius = 8, border_top_right_radius = 8)
    pygame.draw.rect(screen, 'white', (260, 25, 30, 4))
    brush_list = [xl_brush, l_brush, m_brush, s_brush, eraser]
    if tool == 'brush':
        if size == 20:
            pygame.draw.rect(screen, 'green', [10, 10, 50, 50], 3)
        elif size == 15:
            pygame.draw.rect(screen, 'green', [70, 10, 50, 50], 3)
        elif size == 10:
            pygame.draw.rect(screen, 'green', [130, 10, 50, 50], 3)
        elif size == 5:
            pygame.draw.rect(screen, 'green', [190, 10, 50, 50], 3)
    
    elif tool == 'eraser':
        pygame.draw.rect(screen, 'green', [250, 10, 50, 50], 3)

    #undo/redo paint
    redo_button = pygame.draw.rect(screen, 'black', [630, 10, 50, 50])
    pygame.draw.polygon(screen, 'white', ((640, 20), (670, 35), (640, 50)))
    undo_button = pygame.draw.rect(screen, 'black', [570, 10, 50, 50])
    pygame.draw.polygon(screen, 'white', ((610, 20), (580, 35), (610, 50)))

    #current color selected
    pygame.draw.circle(screen, color, (400, 35), 30)
    pygame.draw.circle(screen, 'dark grey', (400, 35), 30, 3)



    #colors you can choose
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
    return brush_list, color_rect, rgb_list, undo_button, redo_button


run = True
while run:
    timer.tick(fps)
    screen.fill('white')

    mouse = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    
    if left_click and mouse[1] > 70:
        if active_tool == 'eraser':
            color_to_use = (255, 255, 255)
        else:
            color_to_use = active_color
        
        pygame.draw.circle(canvas, color_to_use, mouse, active_size)

    screen.blit(canvas, (0, 0))

    if mouse[1] > 70:
        preview_color = (255, 255, 255) if active_tool == "eraser" else active_color
        pygame.draw.circle(screen, active_color, mouse, active_size)
    
    brushes, colors, rgbs, undo_button, redo_button = draw_menu(active_size, active_color, active_tool)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(brushes)):
                if brushes[i].collidepoint(event.pos):
                    if i == 4:
                        active_tool = 'eraser'
                        active_size = 20
                    else:
                        active_tool = 'brush'
                        active_size = 20 - (i * 5)
            
            for i in range(len(colors)):
                if colors[i].collidepoint(event.pos):
                    active_color = rgbs[i]

            if undo_button.collidepoint(event.pos):
                if undo_stack:
                    redo_stack.append(canvas.copy())
                    canvas = undo_stack.pop()
            
            if redo_button.collidepoint(event.pos):
                if redo_stack:
                    undo_stack.append(canvas.copy())
                    canvas = redo_stack.pop()
            
            elif event.pos[1] > 70:
                undo_stack.append(canvas.copy())
                redo_stack.clear()
                drawingstroke = True

    pygame.display.flip()
pygame.quit()