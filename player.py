"""
This class is to implement a player for the tetris piece so that we can use it to run simulations of what is happening.
"""
from tetris_helpers.move import Move
from random import randrange

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
    def get_move(self):
        num = randrange(0,3) + 1
        return Move(num)

