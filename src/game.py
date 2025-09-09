# src/game.py
import pygame
import sys
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_AREA_WIDTH, BLACK, WHITE
from .board import Board
from .block import Block
from .assets import Assets

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('PythonGame Tetris')
        self.clock = pygame.time.Clock()
        self.assets = Assets()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.reset()

    def reset(self):
        self.board = Board(self.assets)
        self.current_block = self.new_block()
        self.running = True
        self.fall_time = 0
        self.fall_speed = 80  # milliseconds (bigger is slower)        
        self.state = 'start'
        self.start_time = pygame.time.get_ticks()

        # Key repeat settings
        self.key_timers = {}
        self.key_repeat_initial_delay = 200  # ms
        self.key_repeat_interval = 50       # ms

        self.assets.play_sound('start')
        
        # Load and play BGM
        bgm_path = self.assets.get_random_bgm_path()
        if bgm_path:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.set_volume(0.5) # 50% volume
            pygame.mixer.music.play(-1) # -1 loops indefinitely
        else:
            print("No BGM files found to play.")

    def new_block(self):
        return Block(x=3, y=0)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == 'game_over':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_q:
                        self.running = False
                return

            if self.state == 'playing':
                if event.type == pygame.KEYDOWN:
                    # Handle single press actions
                    if event.key == pygame.K_UP:
                        if self.board.is_valid_move(self.current_block, 0, 0, 1):
                            self.current_block.rotate()
                            self.assets.play_sound('rotate')
                    elif event.key == pygame.K_SPACE:
                        while self.board.is_valid_move(self.current_block, 0, 1, 0):
                            self.current_block.y += 1
                        self.fall_time = self.fall_speed # Insta-place
                    elif event.key == pygame.K_m:
                        bgm_path = self.assets.get_random_bgm_path()
                        if bgm_path:
                            pygame.mixer.music.load(bgm_path)
                            pygame.mixer.music.play(-1)
                        else:
                            print("No BGM files found to switch to.")
                    
                    # Handle repeatable keys
                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]:
                        self.key_timers[event.key] = {'start': pygame.time.get_ticks(), 'last_repeat': pygame.time.get_ticks()}
                        self.handle_movement(event.key) # First action on press

                elif event.type == pygame.KEYUP:
                    if event.key in self.key_timers:
                        del self.key_timers[event.key]

    def handle_movement(self, key):
        if key == pygame.K_LEFT:
            if self.board.is_valid_move(self.current_block, -1, 0, 0):
                self.current_block.x -= 1
                self.assets.play_sound('move')
        elif key == pygame.K_RIGHT:
            if self.board.is_valid_move(self.current_block, 1, 0, 0):
                self.current_block.x += 1
                self.assets.play_sound('move')
        elif key == pygame.K_DOWN:
            if self.board.is_valid_move(self.current_block, 0, 1, 0):
                self.current_block.y += 1
                self.assets.play_sound('move')

    def handle_key_repeats(self):
        current_time = pygame.time.get_ticks()
        for key, timers in list(self.key_timers.items()):
            if current_time - timers['start'] > self.key_repeat_initial_delay:
                if current_time - timers['last_repeat'] > self.key_repeat_interval:
                    self.handle_movement(key)
                    self.key_timers[key]['last_repeat'] = current_time

    def update(self):
        if self.state == 'start':
            if pygame.time.get_ticks() - self.start_time > 3000:
                self.state = 'playing'
            return

        if self.state == 'playing':
            self.handle_key_repeats()
            self.fall_time += self.clock.get_rawtime()
            if self.fall_time >= self.fall_speed:
                self.fall_time -= self.fall_speed
                if self.board.is_valid_move(self.current_block, 0, 1, 0):
                    self.current_block.y += 1
                else:
                    self.board.place_block(self.current_block)
                    if self.board.lines_cleared_this_turn > 0:
                        self.assets.play_sound('clear')
                    self.current_block = self.new_block()
                    if not self.board.is_valid_move(self.current_block, 0, 0, 0):
                        self.assets.play_sound('gameover')
                        pygame.mixer.music.stop()
                        self.state = 'game_over'

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def draw(self):
        self.screen.fill(BLACK)
        game_surface = self.screen.subsurface((0, 0, GAME_AREA_WIDTH, SCREEN_HEIGHT))

        if self.state == 'start':
            self.draw_text('TETRIS', self.font, WHITE, self.screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)
            self.draw_text('Controls:', self.font, WHITE, self.screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20)
            self.draw_text('Left/Right: Move', self.small_font, WHITE, self.screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20)
            self.draw_text('Up: Rotate', self.small_font, WHITE, self.screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
            self.draw_text('Down: Soft drop', self.small_font, WHITE, self.screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80)
            self.draw_text('Space: Hard drop', self.small_font, WHITE, self.screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 110)

        elif self.state == 'playing':
            self.board.draw(game_surface)
            if self.current_block:
                image = self.assets.images.get(self.current_block.color_key)
                if image:
                    for y, row in enumerate(self.current_block.shape):
                        for x, cell in enumerate(row):
                            if cell:
                                game_surface.blit(image, 
                                                ((self.current_block.x + x) * 30, 
                                                 (self.current_block.y + y) * 30))

        elif self.state == 'game_over':
            self.draw_text('GAME OVER', self.font, WHITE, self.screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
            self.draw_text(f'Score: {self.board.score}', self.font, WHITE, self.screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.draw_text('Press R to Retry or Q to Quit', self.small_font, WHITE, self.screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)

        pygame.display.flip()
