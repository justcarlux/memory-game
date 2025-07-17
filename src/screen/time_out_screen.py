import pygame
from screen.base import GameScreen
from game import Game, GameScreen
from screen.component.game_title import GameTitleImage
from screen.component.back_to_main_menu_button import BackToMainMenuButton
from screen.component.image_wrappers import HorizontallyAlignedImage

class TimeOutScreen(GameScreen):
    def __init__(self, game: Game, points: int, new_record: bool):
        super().__init__(game, 50, 12)
        self.game_title_image = GameTitleImage(self)
        self.time_out_image = HorizontallyAlignedImage(self, "time_out.png", 190)
        self.back_button = BackToMainMenuButton(self)
        back_button_width = 250
        self.back_button.set_rect(
            pygame.Rect(game.display.get_width() / 2 - back_button_width / 2, 563, back_button_width, 60)
        )
        self.font = game.font_manager.get("comfortaa-bold", 24)
        self.points_text = self.font.render(f"¡NUEVO RECORD! Tus puntos: {points}" if new_record else f"Tus puntos: {points}", True, (255, 255, 255))
        self.points_text_x = game.display.get_width() / 2 - self.points_text.get_width() / 2

    def draw(self):
        current_y_offset = self.transition_offset()
        if (current_y_offset < -600 and self._hiding):
            self.hidden = True
            return
        self.game_title_image.draw(current_y_offset)
        self.time_out_image.draw(current_y_offset)
        self.game.display.blit(self.points_text, (self.points_text_x, 500 + current_y_offset))
        self.back_button.is_mouse_hovering = self.back_button.rect.collidepoint(pygame.mouse.get_pos()) if not self.is_transitioning() else False
        self.back_button.draw(current_y_offset)
    
        if self.back_button.is_mouse_hovering and not self.is_transitioning():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
    def on_click(self):
        self.back_button.on_screen_click()