"""
This class is to implement a player for the tetris piece so that we can use it to run simulations of what is happening.
"""
from enum import Enum
import random

class Move(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class random_player():
    def __init__(self,seed=0):
        if not seed == 0:
            random.seed(seed)
    
    def get_move(self):
        num = random.randrange(3) + 1
        return Move(num)

