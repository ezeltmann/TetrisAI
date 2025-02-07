from tetris_headless import Tetris
from player import AiPlayer

class TetrisAIRunner:
    def __init__(self, tetris: Tetris, aiplayer: AiPlayer):
        self._tetris = tetris
        self._ai_player = aiplayer

    @property
    def tetris(self):
        return self._tetris
    
    @property
    def ai_player(self):
        return self._ai_player

    def run_tetris(self):
        pass

    