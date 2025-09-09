# src/constants.py

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_AREA_WIDTH = 300
GAME_AREA_HEIGHT = 600

# Grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Tetromino shapes
TETROMINOES = {
    'i': [[1, 1, 1, 1]],
    'o': [[1, 1], [1, 1]],
    't': [[0, 1, 0], [1, 1, 1]],
    's': [[0, 1, 1], [1, 1, 0]],
    'z': [[1, 1, 0], [0, 1, 1]],
    'j': [[1, 0, 0], [1, 1, 1]],
    'l': [[0, 0, 1], [1, 1, 1]],
}

TETROMINO_COLORS = {
    'i': (0, 255, 255),   # Cyan
    'o': (255, 255, 0),   # Yellow
    't': (128, 0, 128),   # Purple
    's': (0, 255, 0),     # Green
    'z': (255, 0, 0),     # Red
    'j': (0, 0, 255),     # Blue
    'l': (255, 165, 0),   # Orange
}
