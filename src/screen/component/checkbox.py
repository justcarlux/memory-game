import pygame
from screen.base import GameScreen
from util.asset_paths import image_path
from abc import abstractmethod
from screen.component.button import Button, DEFAULT_BUTTON_BG_COLOR, DEFAULT_HIGHLIGHT_COLOR, DEFAULT_BORDER_COLOR, Alignment

class Checkbox(Button):
    def __init__(self, screen: GameScreen, label: str, alignment: Alignment, text_size: int = 27, bg_color: tuple[int, int, int] = DEFAULT_BUTTON_BG_COLOR, highlight_color: tuple[int, int, int] = DEFAULT_HIGHLIGHT_COLOR, border_color: tuple[int, int, int] = DEFAULT_BORDER_COLOR, border_thickness: int = 4, margin: int = 10):
        super().__init__(screen, label, alignment, text_size, bg_color, highlight_color, border_color, border_thickness) 
        self.checked_image = pygame.image.load(image_path("checkbox_checked.png"))
        self.unchecked_image = pygame.image.load(image_path("checkbox_unchecked.png"))
        self.image_coords = (0, 0)
        self.margin = margin
        
    def set_rect(self, rect: pygame.Rect):
        super().set_rect(rect)
        total_width = self.checked_image.get_width() + self.text_surface.get_width() + self.margin
        image_y = self.rect.y + self.rect.height / 2 - self.checked_image.get_height() / 2
        text_y = self.rect.y + self.rect.height / 2 - self.text_surface.get_height() / 2
        horizontal_padding = image_y - self.rect.y
        match self.alignment:
            case Alignment.LEFT:
                self.image_coords = (
                    self.rect.x + horizontal_padding,
                    image_y
                )
                self.text_coords = (
                    self.rect.x +  self.checked_image.get_width() + self.margin + horizontal_padding,
                    text_y
                )
            case Alignment.CENTER:
                starting_x = self.rect.x + self.rect.width / 2 - total_width / 2
                self.image_coords = (
                    starting_x,
                    image_y
                )
                self.text_coords = (
                    starting_x + self.checked_image.get_width() + self.margin,
                    text_y
                )
            case Alignment.RIGHT:
                starting_x = self.rect.x + self.rect.width - total_width - horizontal_padding
                self.image_coords = (
                    starting_x,
                    image_y
                )
                self.text_coords = (
                    starting_x + self.checked_image.get_width() + self.margin,
                    text_y
                )
        
        
    def draw(self, y_offset: float):
        super().draw(y_offset)
        self.screen.game.display.blit(self.checked_image if self.is_checked() else self.unchecked_image, (self.image_coords[0], self.image_coords[1] + y_offset))
        
    @abstractmethod
    def is_checked(self) -> bool:
        pass