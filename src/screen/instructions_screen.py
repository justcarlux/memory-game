import pygame
from screen.base import GameScreen
from game import Game, GameScreen
from screen.component.game_title import GameTitleImage
from screen.component.back_to_main_menu_button import BackToMainMenuButton
from screen.component.image_wrappers import HorizontallyAlignedImage

class InstructionsScreen(GameScreen):
    def __init__(self, game: Game, transition_delay: int = 0):
        super().__init__(game)
        self.game_title_image = GameTitleImage(self)
        self.instructions_image = HorizontallyAlignedImage(self, "instructions.png", 177)
        self.back_button = BackToMainMenuButton(self)
        self.back_button.set_rect(pygame.Rect(600, 545, 250, 60))

    def draw(self):
        current_y_offset = self.transition_offset()
        if (current_y_offset < -400 and self._hiding):
            self.hidden = True
            return
        self.game_title_image.draw(current_y_offset)
        self.instructions_image.draw(current_y_offset)
        self.back_button.is_mouse_hovering = self.back_button.rect.collidepoint(pygame.mouse.get_pos()) if not self.is_transitioning() else False
        self.back_button.draw(current_y_offset)
    
        if self.back_button.is_mouse_hovering and not self.is_transitioning():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
    def on_click(self):
        self.back_button.on_screen_click()