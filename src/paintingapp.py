import pygame
pygame.init()

#global variables
fps = 240
timer = pygame.time.Clock()
Width = 800
Height = 600
ToolbarHeight = 70
SidebarWidth = 70
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
bombs = []
bomb_delay = 2000
explosion_size = 80


def draw_menu(size, color, tool):
    #toolbar
    pygame.draw.line(screen, 'black', (70, 0), (70, Height), 3)
    pygame.draw.rect(screen, 'gray', [0, 0 , Width, 70])
    pygame.draw.rect(screen, 'gray', [0, 0 , 70, Height])
    pygame.draw.line(screen, 'black', (0, 70), (Width, 70), 3)

    #brushes
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
    bucket = pygame.draw.rect(screen, 'black', [310, 10, 50, 50])
    pygame.draw.rect(screen, 'white', [320, 25, 30, 30])
    pygame.draw.rect(screen, 'white', [315, 15, 40, 20], width = 3)
    
    #Toys
    bombtool = pygame.draw.rect(screen, 'black', [10, 80, 50, 50])
    pygame.draw.circle(screen, 'white', (35, 108), 15)
    pygame.draw.rect(screen, 'white', (25, 93, 20, 10))
    pygame.draw.rect(screen, 'white', (33, 86, 5, 10))

    brush_list = [xl_brush, l_brush, m_brush, s_brush, eraser, bucket, bombtool]

    #tool selection
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

    elif tool == 'bucket':
        pygame.draw.rect(screen, 'green', [310, 10, 50, 50], 3)
    
    elif tool == 'bombtool':
        pygame.draw.rect(screen, 'green', [10, 80, 50, 50], 3)

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

def flood_fill(surface, start_pos, fill_color):
    #paint bucket functionality
    x, y = start_pos

    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return
    stack = [(x, y)]

    while stack:
        x, y = stack.pop()
        if x < SidebarWidth or x >= Width or y < ToolbarHeight or y >= Height:
            continue
        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))

    
def draw_bomb(position):
    x, y = position

    pygame.draw.circle(screen, 'black', (x, y), 15)
    pygame.draw.rect(screen, 'black', (x-10, y-25, 20, 10))
    pygame.draw.rect(screen, 'black', (x-2, y-32, 4, 10))

def explodebomb(position, color):
    x, y = position
    half = explosion_size // 2

    pygame.draw.circle(canvas, color, (x, y), 20)
    pygame.draw.rect(canvas, color, (x-half, y-10, explosion_size, 20))
    pygame.draw.rect(canvas, color, (x-10, y-half, 20, explosion_size))


def save_state():
    undo_stack.append(canvas.copy())
    redo_stack.clear()

run = True
while run:
    timer.tick(fps)
    screen.fill('white')

    mouse = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    
    if left_click and mouse[0] > SidebarWidth and mouse[1] > ToolbarHeight and active_tool != 'bucket':
        if not drawingstroke:
            save_state()
            drawingstroke = True
        if active_tool == 'eraser':
            color_to_use = (255, 255, 255)
        else:
            color_to_use = active_color
        
        pygame.draw.circle(canvas, color_to_use, mouse, active_size)

    screen.blit(canvas, (70, 70), (70, 70, Width-70, Height-70))

    #preview circle
    if mouse[0] > SidebarWidth and mouse[1] > ToolbarHeight:
        preview_color = (255, 255, 255) if active_tool == "eraser" else active_color
        pygame.draw.circle(screen, preview_color, mouse, active_size, width = 4)
    
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
                    elif i == 5:
                        active_tool = 'bucket'
                    elif i == 6:
                        active_tool = 'bombtool'
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
            
            elif event.pos[0] > SidebarWidth and event.pos[1] > ToolbarHeight and active_tool == 'bucket':
                save_state()
                flood_fill(canvas, event.pos, active_color)
                drawingstroke = True

        if event.type == pygame.MOUSEBUTTONUP:
            drawingstroke = False

        #keyboard commands
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
        
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if event.key == pygame.K_z:
                    if undo_stack:
                        redo_stack.append(canvas.copy())
                        canvas = undo_stack.pop()
            
                elif event.key == pygame.K_y:
                    if redo_stack:
                        undo_stack.append(canvas.copy())
                        canvas = redo_stack.pop()

    pygame.display.flip()
pygame.quit()