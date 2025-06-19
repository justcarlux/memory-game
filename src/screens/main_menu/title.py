import pygame
import os
from game import Game
from game import ASSETS_PATH

class MainMenuTitle:
    def __init__(self, game: Game):
        self.game = game
        self.image = pygame.image.load(os.path.join(ASSETS_PATH, "images", "title.png"))
        self.x = self.game.screen.get_width() / 2 - self.image.get_width() / 2
        self.y = 60
        
    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))