import pygame
from util.asset_paths import image_path
from screen.base import GameScreen
from game import Game, GameScreen
from screen.component.button import Button, Alignment
from screen.component.checkbox import Checkbox

ENTER_TRANSITION_TOTAL_TICKS = 50
ENTER_TRANSITION_STEP = 12

EXIT_TRANSITION_TOTAL_TICKS = 60
EXIT_TRANSITION_STEP = 12

class OptionsTitle:
    def __init__(self, screen: "OptionsScreen"):
        self.screen = screen
        self.image = pygame.image.load(image_path("options_title.png"))
        self.x = self.screen.game.display.get_width() / 2 - self.image.get_width() / 2
        self.y = 60

    def draw(self, y_offset: float):
        self.screen.game.display.blit(self.image, (self.x, self.y + y_offset))
        
class OptionsMusicCheckbox(Checkbox):
    def __init__(self, screen: "OptionsScreen"):
        super().__init__(screen, "Música", Alignment.LEFT)
        
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
        super().__init__(screen, "SFX", Alignment.LEFT)
        
    def is_checked(self):
        return self.screen.game.settings.sfx_enabled
        
    def on_click(self):
        self.screen.game.settings.toggle_sfx()
        
class OptionsTransitionsCheckbox(Checkbox):
    def __init__(self, screen: "OptionsScreen"):
        super().__init__(screen, "Transiciones", Alignment.LEFT)
        
    def is_checked(self):
        return self.screen.game.settings.transitions_enabled
        
    def on_click(self):
        self.screen.game.settings.toggle_transitions()
        
class OptionsBackButton(Button):
    def __init__(self, screen: "OptionsScreen"):
        super().__init__(screen, "Regresar", Alignment.CENTER)
        
    def on_click(self):
        from screen.main_menu_screen import MainMenuScreen
        self.screen.game.switch_screen(MainMenuScreen(self.screen.game))

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
            OptionsBackButton(screen)
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
    def __init__(self, game: Game, transition_delay: int = 0):
        super().__init__(
            game,
            ENTER_TRANSITION_TOTAL_TICKS,
            ENTER_TRANSITION_STEP,
            EXIT_TRANSITION_TOTAL_TICKS,
            EXIT_TRANSITION_STEP
        )
        self.title = OptionsTitle(self)
        self.input_group = OptionsInputGroup(self, 200, 40)

    def draw(self):
        current_y_offset = self.transition_offset()
        if (current_y_offset < -400 and self._hiding):
            self.hidden = True
            return
        
        self.title.draw(current_y_offset)
        self.input_group.draw(current_y_offset)
    
        if self.input_group.is_mouse_hovering and not self.is_transitioning():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def on_click(self):
        self.input_group.on_click()