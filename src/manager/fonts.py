import pygame
from util.asset_paths import font_path

class FontManager:
    def __init__(self):
        self.font_map = {
            "comfortaa-bold": "comfortaa-bold.ttf"
        }
        self.cache: dict[str, pygame.font.Font] = {}
        
    def get(self, name: str, size: int):
        cached = self.cache.get(f"{name}-{size}")
        if (cached):
            return cached
        font = pygame.font.Font(font_path(self.font_map[name]), size)
        self.cache[f"{name}-{size}"] = font
        return font