import pygame
from game import Game
from abc import ABC, abstractmethod

BORDER_THICKNESS = 4

class MainMenuButton(ABC):
    def __init__(self, game: Game, label: str):
        self.game = game
        self.font = pygame.font.SysFont("Century Gothic", 35)
        self.text_surface = self.font.render(label, True, (255, 255, 255))
        self.is_mouse_hovering = False
        
    def set_rect(self, rect: pygame.Rect):
        self.rect = rect
        self.border_rect = pygame.Rect(
            self.rect.x - BORDER_THICKNESS,
            self.rect.y - BORDER_THICKNESS,
            self.rect.width + BORDER_THICKNESS * 2,
            self.rect.height + BORDER_THICKNESS * 2
        )
        self.text_coords = (
            self.rect.x + self.rect.width / 2 - self.text_surface.get_width() / 2,
            self.rect.y + self.rect.height / 2 - self.text_surface.get_height() / 2
        )
        
    def draw(self):
        pygame.draw.rect(self.game.screen, [255, 255, 255], self.border_rect, border_radius=8)
        pygame.draw.rect(self.game.screen, [119, 154, 209] if not self.is_mouse_hovering else [153, 180, 224], self.rect, border_radius=8)
        self.game.screen.blit(self.text_surface, self.text_coords)
        
    def on_screen_click(self):
        if (self.rect.collidepoint(pygame.mouse.get_pos())):
            self.on_click()
        
    @abstractmethod
    def on_click(self):
        pass
        
class MainMenuPlayButton(MainMenuButton):
    def __init__(self, game: Game):
        super().__init__(game, "Jugar")
        
    def on_click(self):
        print("Play game")
        
class MainMenuTimeTrialButton(MainMenuButton):
    def __init__(self, game: Game):
        super().__init__(game, "Contrarreloj")
        
    def on_click(self):
        print("Time trial")
        
class MainMenuSettingsButton(MainMenuButton):
    def __init__(self, game: Game):
        super().__init__(game, "Opciones")
        
    def on_click(self):
        print("Settings")
        
class MainMenuExitButton(MainMenuButton):
    def __init__(self, game: Game):
        super().__init__(game, "Salir")
        
    def on_click(self):
        self.game.stop()
        
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 60

class MainMenuButtonGroup():
    def __init__(self, game: Game, initialY: int, verticalMargin: int):
        self.buttons = (
            MainMenuPlayButton(game),
            MainMenuTimeTrialButton(game),
            MainMenuSettingsButton(game),
            MainMenuExitButton(game)
        )
        for index, button in enumerate(self.buttons):
            button.set_rect(
                pygame.Rect(
                    game.screen.get_width() / 2 - BUTTON_WIDTH / 2,
                    initialY + BUTTON_HEIGHT * index + verticalMargin * index,
                    BUTTON_WIDTH,
                    BUTTON_HEIGHT
                )
            )
    
    def draw(self):
        is_mouse_hovering = False
        for button in self.buttons:
            button.is_mouse_hovering = button.rect.collidepoint(pygame.mouse.get_pos())
            button.draw()
            if button.is_mouse_hovering:
                is_mouse_hovering = True
                
        if is_mouse_hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def on_click(self):
        for button in self.buttons:
            button.on_screen_click()