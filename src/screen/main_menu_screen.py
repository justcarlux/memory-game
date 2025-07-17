import pygame
from screen.base import GameScreen
from game import Game, GameScreen
from screen.options_screen import OptionsScreen
from screen.component.button import Button, Alignment
from screen.game_difficulty_screen import GameDifficultyScreen
from screen.instructions_screen import InstructionsScreen
from screen.component.game_title import GameTitleImage

class MainMenuScreen(GameScreen):
    def __init__(self, game: Game, transition_delay: int = 0):
        super().__init__(game)
        self.__transition_delay = transition_delay
        self.game_title_image = GameTitleImage(self)
        self.button_group = MainMenuButtonGroup(self, 230, 30)

    def draw(self):
        if (self.__transition_delay > 0):
            self.__transition_delay -= 1
            return
        current_y_offset = self.transition_offset()
        if (current_y_offset < -600 and self._hiding):
            self.hidden = True
            return
            
        self.game_title_image.draw(current_y_offset)
        self.button_group.draw(current_y_offset)
        
        if self.button_group.is_mouse_hovering and not self.is_transitioning():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def on_click(self):
        self.button_group.on_click()

class MainMenuPlayButton(Button):
    def __init__(self, screen: MainMenuScreen):
        super().__init__(screen, "Jugar", Alignment.CENTER) 
        
    def on_click(self):
        self.screen.game.switch_screen(GameDifficultyScreen(self.screen.game))
        
class MainMenuInstructionsButton(Button):
    def __init__(self, screen: MainMenuScreen):
        super().__init__(screen, "Instrucciones", Alignment.CENTER) 
        
    def on_click(self):
        self.screen.game.switch_screen(InstructionsScreen(self.screen.game))
        
class MainMenuSettingsButton(Button):
    def __init__(self, screen: MainMenuScreen):
        super().__init__(screen, "Opciones", Alignment.CENTER) 
        
    def on_click(self):
        self.screen.game.switch_screen(OptionsScreen(self.screen.game))
        
class MainMenuExitButton(Button):
    def __init__(self, screen: MainMenuScreen):
        super().__init__(screen, "Salir", Alignment.CENTER) 
        
    def on_click(self):
        self.screen.game.stop()
        
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 60

class MainMenuButtonGroup():
    def __init__(self, screen: MainMenuScreen, initial_y: int, vertical_margin: int):
        self.screen = screen
        self.is_mouse_hovering = False
        self.buttons = (
            MainMenuPlayButton(screen),
            MainMenuInstructionsButton(screen),
            MainMenuSettingsButton(screen),
            MainMenuExitButton(screen)
        )
        for index, button in enumerate(self.buttons):
            button.set_rect(
                pygame.Rect(
                    screen.game.display.get_width() / 2 - BUTTON_WIDTH / 2,
                    initial_y + BUTTON_HEIGHT * index + vertical_margin * index,
                    BUTTON_WIDTH,
                    BUTTON_HEIGHT
                )
            )
    
    def draw(self, y_offset: float):
        is_mouse_hovering = False
        for button in self.buttons:
            button.is_mouse_hovering = button.rect.collidepoint(pygame.mouse.get_pos()) if not self.screen.is_transitioning() else False
            button.draw(y_offset)
            if button.is_mouse_hovering:
                is_mouse_hovering = True
        self.is_mouse_hovering = is_mouse_hovering if not self.screen.is_transitioning() else False
    
    def on_click(self):
        for button in self.buttons:
            button.on_screen_click()
