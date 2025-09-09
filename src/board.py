# src/board.py
import pygame
from .constants import GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE, BLACK, GRAY

class Board:
    def __init__(self, assets):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.lines_cleared = 0
        self.lines_cleared_this_turn = 0
        self.assets = assets

    def draw(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell = self.grid[y][x]
                if cell == 0:
                    # Draw grid lines
                    pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
                else:
                    # Draw block image
                    image = self.assets.images.get(cell)
                    if image:
                        screen.blit(image, (x * BLOCK_SIZE, y * BLOCK_SIZE))

    def is_valid_move(self, block, dx, dy, dr):
        temp_shape = [list(row) for row in block.shape]
        if dr:
            temp_shape = [list(row) for row in zip(*temp_shape[::-1])]

        for y, row in enumerate(temp_shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = block.x + x + dx
                    new_y = block.y + y + dy
                    if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and self.grid[new_y][new_x] == 0):
                        return False
        return True

    def place_block(self, block):
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[block.y + y][block.x + x] = block.color_key
        self.clear_lines()

    def clear_lines(self):
        self.lines_cleared_this_turn = 0
        lines_to_clear = []
        for y, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                lines_to_clear.append(y)

        if lines_to_clear:
            for y in lines_to_clear:
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            
            self.lines_cleared_this_turn = len(lines_to_clear)
            self.lines_cleared += self.lines_cleared_this_turn
            # Simple scoring
            self.score += self.lines_cleared_this_turn * 100
