import pygame
import os
pygame.init()

#global variables
fps = 240
timer = pygame.time.Clock()
Width = 900
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
savedfile = "savedart.png"
if os.path.exists(savedfile):
    saved_image = pygame.image.load(savedfile)
    canvas.blit(saved_image, (0, 0))
    os.remove(savedfile)
undo_stack = []
redo_stack = []
drawingstroke = False
bombs = []
bomb_delay = 2000
explosion_size = 200
prev_mouse = None
filter_modes = ["normal", "grayscale"]
current_filter_index = 0
original_filter = None


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
    colorfilter = pygame.draw.rect(screen, 'black', [10, 540, 50, 50])
    pygame.draw.circle(screen, 'white', (35, 560), 13, width = 3)
    pygame.draw.circle(screen, 'white', (42, 570), 13, width = 3)
    pygame.draw.circle(screen, 'white', (28, 570), 13, width = 3)

    brush_list = [xl_brush, l_brush, m_brush, s_brush, eraser, bucket, bombtool, colorfilter]

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

    elif tool == 'colorfilter':
        pygame.draw.rect(screen, 'green', [10, 540, 50, 50], 3)


    #Utility Buttons
    redo_button = pygame.draw.rect(screen, 'black', [Width - 175, 10, 50, 50])
    pygame.draw.polygon(screen, 'white', ((Width - 165, 20), (Width - 135, 35), (Width - 165, 50)))
    undo_button = pygame.draw.rect(screen, 'black', [Width - 235, 10, 50, 50])
    pygame.draw.polygon(screen, 'white', ((Width - 195, 20), (Width - 225, 35), (Width - 195, 50)))
    save_button = pygame.draw.rect(screen, 'black', [Width - 295, 10, 50, 50])
    pygame.draw.rect(screen, 'white', [Width - 287, 18, 35, 35], width = 3)
    pygame.draw.rect(screen, 'white', [Width - 280, 18, 20, 12], width = 3)
    pygame.draw.rect(screen, 'white', [Width - 282, 33, 24, 20], width = 3)
    clear_button = pygame.draw.rect(screen, 'black', [Width - 355, 10, 50, 50])
    pygame.draw.line(screen, 'white', (Width - 316, 17), (Width - 346, 52), width=6)
    pygame.draw.line(screen, 'white', (Width - 346, 17), (Width - 316, 52), width=6)

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
    return (brush_list, color_rect, rgb_list, undo_button, redo_button, save_button, clear_button, colorfilter)

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

    
def draw_bomb(position, color, elapsed):
    x, y = position
    tickingpulse = 15 + ((elapsed // 200) % 2)
    if (elapsed // 300) % 2 == 0:
        bomb_color = color
    else:
        bomb_color = "dark gray"

    pygame.draw.circle(screen, bomb_color, (x, y), tickingpulse)
    pygame.draw.rect(screen, bomb_color, (x-10, y-20, 20, 10),)
    pygame.draw.rect(screen, bomb_color, (x-2, y-28, 5, 10))

def explodebomb(position, color):
    x, y = position
    half = explosion_size // 2

    pygame.draw.circle(canvas, color, (x, y), 30)
    pygame.draw.rect(canvas, color, (x-half, y-15, explosion_size, 30))
    pygame.draw.rect(canvas, color, (x-15, y-half, 30, explosion_size))

def apply_filter(mode):
    global canvas, original_filter
    if mode != "normal" and original_filter is None:
        original_filter = canvas.copy()

    if mode == "normal":
        if original_filter:
            canvas = original_filter.copy()
            original_filter = None
        return
    save_state()

    temp_surface = original_filter.copy()
    for x in range (SidebarWidth, Width):
        for y in range (ToolbarHeight, Height):
            r, g, b, a = temp_surface.get_at((x, y))
            if mode == "grayscale":
                gray = (r + g + b) // 3
                temp_surface.set_at((x, y), (gray, gray, gray))
    
    canvas = temp_surface


def save_state():
    undo_stack.append(canvas.copy())
    redo_stack.clear()

run = True
while run:
    timer.tick(fps)
    screen.fill('white')

    mouse = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    
    if (left_click and mouse[0] > SidebarWidth and mouse[1] > ToolbarHeight
        and active_tool not in ['bucket', 'bombtool']):
        if not drawingstroke:
            save_state()
            drawingstroke = True
        if active_tool == 'eraser':
            color_to_use = (255, 255, 255)
        else:
            color_to_use = active_color
        
        if prev_mouse is not None:
            mid_x = (prev_mouse[0] + mouse[0]) // 2
            mid_y = (prev_mouse[1] + mouse[1]) // 2
            pygame.draw.line(canvas, color_to_use, prev_mouse, mouse, active_size * 2)
            prev_mouse = mouse
        else:
            pygame.draw.circle(canvas, color_to_use, mouse, active_size)

    screen.blit(canvas, (70, 70), (70, 70, Width-70, Height-70))
    current_time = pygame.time.get_ticks()

    for bomb in bombs[:]:
        elapsed = current_time - bomb['time']
        if elapsed >= bomb_delay:
            save_state()
            explodebomb(bomb["pos"], bomb["color"])
            bombs.remove(bomb)
        else:
            draw_bomb(bomb["pos"], bomb["color"], elapsed)

    #preview circle
    if mouse[0] > SidebarWidth and mouse[1] > ToolbarHeight:
        if active_tool == "brush":
            pygame.draw.circle(screen, active_color, mouse, active_size, width=4)
        
        elif active_tool == "eraser":
            pygame.draw.circle(screen, "gray", mouse, active_size, width=4)

        elif active_tool == "bucket":
            pygame.draw.rect(screen, active_color, (mouse[0]-10, mouse[1]-10, 20, 20), 2)
        
        elif active_tool == "bombtool":
            x, y = mouse
            pygame.draw.circle(screen, active_color, (x, y), 15, 2)
            pygame.draw.rect(screen, active_color, (x-10, y-16, 20, 10), 2)
            pygame.draw.rect(screen, active_color, (x-2, y-23, 5, 10), 2)

    
    brushes, colors, rgbs, undo_button, redo_button, save_button, clear_button, colorfilter = draw_menu(active_size, active_color, active_tool)

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
                    elif i == 7:
                        current_filter_index = (current_filter_index + 1) % len(filter_modes)
                        apply_filter(filter_modes[current_filter_index])
                    else:
                        active_tool = 'brush'
                        active_size = 20 - (i * 5)
            
            for i in range(len(colors)):
                if colors[i].collidepoint(event.pos):
                    active_color = rgbs[i]

            if save_button.collidepoint(event.pos):
                pygame.image.save(canvas, savedfile)

            if clear_button.collidepoint(event.pos):
                save_state()
                canvas.fill("white")
                bombs.clear()

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

            elif (event.pos[0] > SidebarWidth and event.pos[1] > ToolbarHeight and active_tool == 'bombtool'):
                bombs.append({
                    "pos": event.pos,
                    "time": pygame.time.get_ticks(),
                    "color": active_color
                })

        if event.type == pygame.MOUSEBUTTONUP:
            drawingstroke = False
            prev_mouse = None

        #keyboard commands
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if event.key == pygame.K_ESCAPE:
                run = False

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