import pygame
from screen.base import GameScreen
from game import Game, GameScreen
from screen.component.button import Alignment
from screen.component.back_to_main_menu_button import BackToMainMenuButton
from screen.component.checkbox import Checkbox
from screen.component.image_wrappers import HorizontallyAlignedImage
        
class OptionsMusicCheckbox(Checkbox):
    def __init__(self, screen: "OptionsScreen"):
        super().__init__(screen, "Música", Alignment.LEFT, 27)
        
    def is_checked(self):
        return self.screen.game.settings.music_enabled
        
    def on_click(self):
        self.screen.game.settings.toggle_music()
        if (self.screen.game.settings.music_enabled):
            self.screen.game.sound_manager.play_music()
        else:
            self.screen.game.sound_manager.stop_music()
        
class OptionsSFXCheckbox(Checkbox):
    def __init__(self, screen: "OptionsScreen"):
        super().__init__(screen, "Sonidos (SFX)", Alignment.LEFT, 27)
        
    def is_checked(self):
        return self.screen.game.settings.sfx_enabled
        
    def on_click(self):
        self.screen.game.settings.toggle_sfx()
        
class OptionsTransitionsCheckbox(Checkbox):
    def __init__(self, screen: "OptionsScreen"):
        super().__init__(screen, "Transiciones", Alignment.LEFT, 27)
        
    def is_checked(self):
        return self.screen.game.settings.transitions_enabled
        
    def on_click(self):
        self.screen.game.settings.toggle_transitions()

BUTTON_WIDTH = 310
BUTTON_HEIGHT = 60

class OptionsInputGroup():
    def __init__(self, screen: "OptionsScreen", initial_y: int, vertical_margin: int):
        self.screen = screen
        self.is_mouse_hovering = False
        self.inputs = (
            OptionsMusicCheckbox(screen),
            OptionsSFXCheckbox(screen),
            OptionsTransitionsCheckbox(screen),
            BackToMainMenuButton(screen)
        )
        for index, input in enumerate(self.inputs):
            input.set_rect(
                pygame.Rect(
                    screen.game.display.get_width() / 2 - BUTTON_WIDTH / 2,
                    initial_y + BUTTON_HEIGHT * index + vertical_margin * index,
                    BUTTON_WIDTH,
                    BUTTON_HEIGHT
                )
            )
    
    def draw(self, y_offset: float):
        is_mouse_hovering = False
        for input in self.inputs:
            input.is_mouse_hovering = input.rect.collidepoint(pygame.mouse.get_pos()) if not self.screen.is_transitioning() else False
            input.draw(y_offset)
            if input.is_mouse_hovering:
                is_mouse_hovering = True
        self.is_mouse_hovering = is_mouse_hovering if not self.screen.is_transitioning() else False
    
    def on_click(self):
        for input in self.inputs:
            input.on_screen_click()


class OptionsScreen(GameScreen):
    def __init__(self, game: Game):
        super().__init__(game)
        self.options_title_image = HorizontallyAlignedImage(self, "options_title.png", 60)
        self.input_group = OptionsInputGroup(self, 200, 40)

    def draw(self):
        current_y_offset = self.transition_offset()
        if (current_y_offset < -600 and self._hiding):
            self.hidden = True
            return
        
        self.options_title_image.draw(current_y_offset)
        self.input_group.draw(current_y_offset)
    
        if self.input_group.is_mouse_hovering and not self.is_transitioning():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def on_click(self):
        self.input_group.on_click()