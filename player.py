"""
This class is to implement a player for the tetris piece so that we can use it to run simulations of what is happening.
"""
from enum import Enum
from rng_handle.rand_inter import RandomNumberInterface

class Move(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class AiPlayer():
    def __init__(self):
        pass

    def get_move(self):
        pass

    def set_board_state(self):
        pass

    def set_next_piece(self):
        pass
    
    def set_score(self):
        pass



class random_player():
    def __init__(self, rng_provider: RandomNumberInterface):
        self.rnd = rng_provider
    
    def get_move(self):
        num = self.rnd.randrange(0,3) + 1
        return Move(num)

