import pygame
import os
from copy import deepcopy
from rng_handle.rand_inter import ControlledRNG
#from random import choice, randrange
from player import random_player
from player import Move

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 600

# Set Random Seed before working with this system
rnd = ControlledRNG()

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                 #  
                 #  XXXX
                 #
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                 #
                 #   XX
                 #   XX
                 #
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                 #
                 #   X
                 #   XX
                 #    X
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                 #
                 #   X
                 #  XX
                 #  X
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
                 #
                 #    X
                 #    X
                 #   XX
               [(0, 0), (0, -1), (0, 1), (1, -1)],
                 #
                 #   X
                 #   X
                 #   XX
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]
                 #
                 #   X 
                 #  XX
                 #   X

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

bg = pygame.image.load('img/bg.jpg').convert()
game_bg = pygame.image.load('img/bg2.jpg').convert()

main_font = pygame.font.Font('font/font.ttf', 65)
font = pygame.font.Font('font/font.ttf', 45)

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))

get_color = lambda : (rnd.randrange(30, 256), rnd.randrange(30, 256), rnd.randrange(30, 256))

figure, next_figure = deepcopy(rnd.choice(figures)), deepcopy(rnd.choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

play = random_player(ControlledRNG())
last_move = 0
timing = (FPS/60)

while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True"""
    now = pygame.time.get_ticks()
    if now - last_move >= timing:
        last_move = now
        move_choice = play.get_move()

        if move_choice == Move.LEFT:
            dx = -1
        elif move_choice == Move.RIGHT:
            dx = 1
        elif move_choice == Move.DOWN:
            anim_limit = 100
        elif move_choice == Move.UP:
            rotate = True
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(rnd.choice(figures)), get_color()
                anim_limit = 2000
                break
    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    # check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
    # compute score
    score += scores[lines]
    #print(f"Current Score: {score}")
    # draw grid
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # draw figure
    current_fig = []
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        current_fig.append((figure[i].x,figure[i].y))
        pygame.draw.rect(game_sc, color, figure_rect)
    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
    
    #print(f"CurrentField: {field}")
    ## AI Eyes Output
    picture = []
    for y, raw in enumerate(field):
        col_pic = []        
        for x, col in enumerate(raw):
            skip = False
            for coord in current_fig:
                if (x == coord[0] and y == coord[1]):
                    col_pic.append(2)
                    skip = True
            if (not skip):
                if col:
                    col_pic.append(1)
                else:
                    col_pic.append(0)
        picture.append(col_pic)
    print(f"AI Image: {picture}")
    print(f"Field = {field}")

    # draw next figure
    # print(f"Next Figure: {next_figure}")
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)
    
    """
    block_list = []
    for i in range(4):
        x,y = next_figure[i].x, next_figure[i].y
        block_list.append((x-4, y))
    
    next_fig_picture = []
    for i in range(4):
        next_fig_picture_row = []
        for j in range(4):
            has_block = False
            for pos in block_list:
                if (pos[1] == i and pos[0] == j):
                    has_block = True
            if (has_block):
                next_fig_picture_row.append(1)
            else:
                next_fig_picture_row.append(0)
        next_fig_picture.append(next_fig_picture_row)

    print(f"Next Figure = {next_fig_picture}")
    """

    # draw titles
    sc.blit(title_tetris, (485, -10))
    sc.blit(title_score, (535, 780))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 840))
    sc.blit(title_record, (525, 650))
    sc.blit(font.render(record, True, pygame.Color('gold')), (550, 710))
    # game over
    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)