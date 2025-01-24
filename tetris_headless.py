"""
This is the implementation of a "headless" tetris, wherein the game can be played without showing the specific results.
Specifically this will allow us to do all of the ai testing without actually having to watch the games play out.
"""
import os
from tetris_helpers.coord import Coord
from copy import deepcopy
from rng_handle.rand_inter import ControlledRNG
#from random import choice, randrange
from player import random_player
from player import Move

class Tetris():
    def __init__(self):
        self.W=10
        self.H=20
        self.field=[[0 for i in range(self.W)] for j in range(self.H)]

    def check_borders(self,figure,i,field):
        if figure[i].x < 0 or figure[i].x > self.W - 1:
            return False
        elif figure[i].y > self.H - 1 or field[figure[i].y][figure[i].x]:
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
    
    def play_tetris(self):
        still_playing = True
        while still_playing:
            for i in range(self.W):
                if self.field[0][i]:
                    self.set_record(record, score)
                    still_playing = False


W, H = 10, 20

# Set Random Seed before working with this system
rnd = ControlledRNG()


grid = [0 for x in range(W) for y in range(H)]

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

figures = [[Coord(x + W // 2, y + 1) for x, y in fig_pos] for fig_pos in figures_pos]
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

figure, next_figure = deepcopy(rnd.choice(figures)), deepcopy(rnd.choice(figures))

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}




play = random_player(ControlledRNG())
last_move = 0
#timing = (FPS/60)

while True:
    record = get_record()
    dx, rotate = 0, False
    move_choice = play.get_move()

    if move_choice == Move.LEFT:
        dx = -1
    elif move_choice == Move.RIGHT:
        dx = 1
    elif move_choice == Move.DOWN:
        pass
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
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].y += 1
        if not check_borders():
            for i in range(4):
                field[figure_old[i].y][figure_old[i].x] = 1
            figure = next_figure
            next_figure = deepcopy(rnd.choice(figures))
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
    print(f"Current Score: {score}")
    # draw grid
    # draw figure
    current_fig = []
    for i in range(4):
        current_fig.append((figure[i].x,figure[i].y))
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
    
    print("AI Image:")
    for row in picture:
        print(row)
   


    # draw next figure
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
    
    # draw titles
    # game over

            #field = [[0 for i in range(W)] for i in range(H)]
            #anim_count, anim_speed, anim_limit = 0, 60, 2000
            #score = 0
