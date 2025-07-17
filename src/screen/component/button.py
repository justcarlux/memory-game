import pygame
from abc import ABC, abstractmethod
from screen.base import GameScreen
from enum import Enum

class Alignment(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

DEFAULT_BUTTON_BG_COLOR = (119, 154, 209)
DEFAULT_HIGHLIGHT_COLOR = (153, 180, 224)
DEFAULT_BORDER_COLOR = (255, 255, 255)
DEFAULT_BORDER_THICKNESS = 4

class Button(ABC):
    def __init__(self, screen: GameScreen, label: str, alignment: Alignment, text_size: int = 27, bg_color: tuple[int, int, int] = DEFAULT_BUTTON_BG_COLOR, highlight_color: tuple[int, int, int] = DEFAULT_HIGHLIGHT_COLOR, border_color: tuple[int, int, int] = DEFAULT_BORDER_COLOR, border_thickness: int = DEFAULT_BORDER_THICKNESS):
        self.screen = screen
        self.font = screen.game.font_manager.get("comfortaa-bold", text_size)
        self.text_surface = self.font.render(label, True, (255, 255, 255))
        self.alignment = alignment
        self.border_radius = 0
        self.bg_color = bg_color
        self.highlight_color = highlight_color
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.is_mouse_hovering = False
        
    def set_rect(self, rect: pygame.Rect):
        self.rect = rect
        self.border_rect = pygame.Rect(
            self.rect.x - self.border_thickness,
            self.rect.y - self.border_thickness,
            self.rect.width + self.border_thickness * 2,
            self.rect.height + self.border_thickness * 2
        )
        y = self.rect.y + self.rect.height / 2 - self.text_surface.get_height() / 2
        horizontal_padding = y - self.rect.y
        match self.alignment:
            case Alignment.LEFT:
                self.text_coords = (self.rect.x + horizontal_padding, y)
            case Alignment.CENTER:
                self.text_coords = (
                    self.rect.x + self.rect.width / 2 - self.text_surface.get_width() / 2,
                    y
                )
            case Alignment.RIGHT:
                self.text_coords = (self.rect.x + self.rect.width - self.text_surface.get_width() - horizontal_padding, y)
        
        
    def draw(self, y_offset: float):
        pygame.draw.rect(self.screen.game.display, self.border_color, self.border_rect.move(0, y_offset), border_radius=self.border_radius)
        pygame.draw.rect(self.screen.game.display, self.bg_color if not self.is_mouse_hovering else self.highlight_color, self.rect.move(0, y_offset), border_radius=self.border_radius)
        self.screen.game.display.blit(self.text_surface, (self.text_coords[0], self.text_coords[1] + y_offset))
        
    def on_screen_click(self):
        if (self.rect.collidepoint(pygame.mouse.get_pos())):
            self.screen.game.sound_manager.play_sfx("click")
            self.on_click()
        
    @abstractmethod
    def on_click(self):
        pass
    
