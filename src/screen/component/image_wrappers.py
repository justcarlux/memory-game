import pygame
from util.asset_paths import image_path

class HorizontallyAlignedImage:
    def __init__(self, screen: "GameScreen", name: str, y: int):
        self.screen = screen
        self.image = pygame.image.load(image_path(name))
        self.x = self.screen.game.display.get_width() / 2 - self.image.get_width() / 2
        self.y = y
        
    def draw(self, y_offset: float):
        self.screen.game.display.blit(self.image, (self.x, self.y + y_offset))
        
from screen.base import GameScreen