# src/block.py
import random
from .constants import TETROMINOES, TETROMINO_COLORS

class Block:
    def __init__(self, x, y, shape_type=None):
        self.x = x
        self.y = y
        if shape_type:
            self.shape_type = shape_type
        else:
            self.shape_type = random.choice(list(TETROMINOES.keys()))
        
        self.shape = TETROMINOES[self.shape_type]
        self.color_key = self.shape_type

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
