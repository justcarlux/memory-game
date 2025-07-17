import pygame
from screen.base import GameScreen
from game import Game, GameScreen
from screen.component.button import Button, Alignment
from screen.in_game_screen import InGameScreen, InGameDifficulty
from screen.component.game_title import GameTitleImage
from screen.component.back_to_main_menu_button import BackToMainMenuButton
from screen.component.image_wrappers import HorizontallyAlignedImage

class GameDifficultyScreen(GameScreen):
    def __init__(self, game: Game):
        super().__init__(game)
        self.game_title_image = GameTitleImage(self)
        self.button_group = GameDifficultyButtonGroup(self, 240, 30)
        self.select_difficulty_image = HorizontallyAlignedImage(self, "select_difficulty.png", 177)

    def draw(self):
        current_y_offset = self.transition_offset()
        if (current_y_offset < -600 and self._hiding):
            self.hidden = True
            return
            
        self.game_title_image.draw(current_y_offset)
        self.select_difficulty_image.draw(current_y_offset)
        self.button_group.draw(current_y_offset)
        
        if self.button_group.is_mouse_hovering and not self.is_transitioning():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def on_click(self):
        self.button_group.on_click()

class GameDifficultyEasyButton(Button):
    def __init__(self, screen: GameDifficultyScreen):
        super().__init__(screen, "Fácil", Alignment.CENTER) 
        
    def on_click(self):
        self.screen.game.switch_screen(InGameScreen(self.screen.game, InGameDifficulty.EASY))
        
class GameDifficultyMediumButton(Button):
    def __init__(self, screen: GameDifficultyScreen):
        super().__init__(screen, "Medio", Alignment.CENTER)
        
    def on_click(self):
        self.screen.game.switch_screen(InGameScreen(self.screen.game, InGameDifficulty.MEDIUM))
        
class GameDifficultyHardButton(Button):
    def __init__(self, screen: GameDifficultyScreen):
        super().__init__(screen, "Difícil", Alignment.CENTER) 
        
    def on_click(self):
        self.screen.game.switch_screen(InGameScreen(self.screen.game, InGameDifficulty.HARD))
        
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 60

class GameDifficultyButtonGroup():
    def __init__(self, screen: GameDifficultyScreen, initial_y: int, vertical_margin: int):
        self.screen = screen
        self.is_mouse_hovering = False
        self.buttons = (
            GameDifficultyEasyButton(screen),
            GameDifficultyMediumButton(screen),
            GameDifficultyHardButton(screen),
            BackToMainMenuButton(screen)
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
