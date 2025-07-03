import pygame
from abc import ABC, abstractmethod
from screen.base import GameScreen
from util.asset_paths import image_path

DEFAULT_BUTTON_BG_COLOR = (119, 154, 209)
DEFAULT_HIGHLIGHT_COLOR = (153, 180, 224)
DEFAULT_BORDER_COLOR = (255, 255, 255)
DEFAULT_BORDER_THICKNESS = 4

class Button(ABC):
    def __init__(self, screen: GameScreen, label: str, bg_color: tuple[int, int, int] = DEFAULT_BUTTON_BG_COLOR, highlight_color: tuple[int, int, int] = DEFAULT_HIGHLIGHT_COLOR, border_color: tuple[int, int, int] = DEFAULT_BORDER_COLOR, border_thickness: int = DEFAULT_BORDER_THICKNESS):
        self.screen = screen
        self.font = screen.game.font_manager.get("comfortaa-bold", 27)
        self.text_surface = self.font.render(label, True, (255, 255, 255))
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
        self.text_coords = (
            self.rect.x + self.rect.width / 2 - self.text_surface.get_width() / 2,
            self.rect.y + self.rect.height / 2 - self.text_surface.get_height() / 2
        )
        
    def draw(self, y_offset: float):
        pygame.draw.rect(self.screen.game.display, self.border_color, self.border_rect.move(0, y_offset), border_radius=self.border_radius)
        pygame.draw.rect(self.screen.game.display, self.bg_color if not self.is_mouse_hovering else self.highlight_color, self.rect.move(0, y_offset), border_radius=self.border_radius)
        self.screen.game.display.blit(self.text_surface, (self.text_coords[0], self.text_coords[1] + y_offset))
        
    def on_screen_click(self):
        if (self.rect.collidepoint(pygame.mouse.get_pos())):
            self.on_click()
        
    @abstractmethod
    def on_click(self):
        pass
    
class Checkbox(Button):
    def __init__(self, screen: GameScreen, label: str, bg_color: tuple[int, int, int] = DEFAULT_BUTTON_BG_COLOR, highlight_color: tuple[int, int, int] = DEFAULT_HIGHLIGHT_COLOR, border_color: tuple[int, int, int] = DEFAULT_BORDER_COLOR, border_thickness: int = 4, margin: int = 10):
        super().__init__(screen, label, bg_color, highlight_color, border_color, border_thickness)
        self.checked_image = pygame.image.load(image_path("checkbox_checked.png"))
        self.unchecked_image = pygame.image.load(image_path("checkbox_unchecked.png"))
        self.image_coords = (0, 0)
        self.margin = margin
        
    def set_rect(self, rect: pygame.Rect):
        super().set_rect(rect)
        total_width = self.checked_image.get_width() + self.text_surface.get_width() + self.margin
        starting_x = self.rect.x + self.rect.width / 2 - total_width / 2
        self.image_coords = (
            starting_x,
            self.rect.y + self.rect.height / 2 - self.checked_image.get_height() / 2
        )
        self.text_coords = (
            starting_x + self.checked_image.get_width() + self.margin,
            self.rect.y + self.rect.height / 2 - self.text_surface.get_height() / 2
        )
        
    def draw(self, y_offset: float):
        super().draw(y_offset)
        self.screen.game.display.blit(self.checked_image if self.is_checked() else self.unchecked_image, (self.image_coords[0], self.image_coords[1] + y_offset))
        
    @abstractmethod
    def is_checked(self) -> bool:
        pass