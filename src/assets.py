# src/assets.py
import pygame
import os
import glob
import random

class Assets:
    def __init__(self):
        self.images = self.load_images()
        self.sounds = self.load_sounds()
        self.music_files = self.load_music_files()

    def load_images(self):
        images = {}
        image_dir = os.path.join('src', 'assets', 'images')
        # Assuming block images are named like 'blue.png', 'green.png', etc.
        for color_key in ['i', 'o', 't', 's', 'z', 'j', 'l']:
            try:
                path = os.path.join(image_dir, f'{color_key}.png')
                images[color_key] = pygame.image.load(path).convert_alpha()
            except pygame.error:
                print(f"Warning: Could not load image: {path}")
                images[color_key] = None # Placeholder
        return images

    def load_sounds(self):
        sounds = {}
        sound_dir = os.path.join('src', 'assets', 'sounds')
        sound_files = {
            'start': 'start.wav',
            'move': 'move.wav',
            'rotate': 'rotate.wav',
            'clear': 'clear.wav',
            'gameover': 'gameover.wav'
        }
        for name, filename in sound_files.items():
            try:
                path = os.path.join(sound_dir, filename)
                sounds[name] = pygame.mixer.Sound(path)
            except pygame.error:
                print(f"Warning: Could not load sound: {path}")
                sounds[name] = None # Placeholder
        return sounds

    def load_music_files(self):
        music_dir = os.path.join('src', 'assets', 'sounds')
        # Search for bgm*.mp3 files
        music_paths = glob.glob(os.path.join(music_dir, 'bgm*.mp3'))
        if not music_paths:
            print(f"Warning: No BGM files found in {music_dir}")
        return music_paths

    def get_random_bgm_path(self):
        if self.music_files:
            return random.choice(self.music_files)
        return None

    def play_sound(self, name):
        if self.sounds.get(name):
            self.sounds[name].play()
