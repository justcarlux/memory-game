import pygame
from abc import ABC, abstractmethod
from util.easing import ease_in_out_cubic
from util.asset_paths import image_path
from screen.base import GameScreen
from game import Game, GameScreen

ENTER_TRANSITION_TOTAL_TICKS = 50
ENTER_TRANSITION_STEP = 12

EXIT_TRANSITION_TOTAL_TICKS = 60
EXIT_TRANSITION_STEP = 12

class MainMenuScreen(GameScreen):
    def __init__(self, game: Game, transition_delay: int = 0):
        super().__init__(game)
        self.title = MainMenuTitle(self)
        self.button_group = MainMenuButtonGroup(self, 230, 30)
        self.__transition_delay = transition_delay
        self.__transition_left_ticks = ENTER_TRANSITION_TOTAL_TICKS + 1 if self.game.settings.transitions_enabled else 0
        self.__hidden = False

    def transition_offset(self):
        if (self.__transition_delay > 0):
            self.__transition_delay -= 1
            return ENTER_TRANSITION_TOTAL_TICKS * ENTER_TRANSITION_STEP
        if (self.__transition_left_ticks <= 0):
            return 0
        self.__transition_left_ticks -= 1
        if (self._hiding):
            current = EXIT_TRANSITION_TOTAL_TICKS - self.__transition_left_ticks
            progress = current / EXIT_TRANSITION_TOTAL_TICKS
            return -(ease_in_out_cubic(progress) * EXIT_TRANSITION_TOTAL_TICKS * EXIT_TRANSITION_STEP)
        else:
            max = ENTER_TRANSITION_TOTAL_TICKS * ENTER_TRANSITION_STEP
            current = self.__transition_left_ticks * ENTER_TRANSITION_STEP
            progress = (max - current) / max
            return max - (ease_in_out_cubic(progress) * max)

    def draw(self):
        current_y_offset = self.transition_offset()
        if (current_y_offset < -400 and self._hiding):
            self.hidden = True
            return
            
        self.title.draw(current_y_offset)
        self.button_group.draw(current_y_offset)
        
        if self.button_group.is_mouse_hovering and not self.is_transitioning():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
    def is_transitioning(self):
        return self.__transition_left_ticks > 0
    
    def hide(self):
        super().hide()
        self.__transition_left_ticks = EXIT_TRANSITION_TOTAL_TICKS + 1
        
    def on_click(self):
        self.button_group.on_click()

class MainMenuTitle:
    def __init__(self, screen: MainMenuScreen):
        self.screen = screen
        self.image = pygame.image.load(image_path("title.png"))
        self.x = self.screen.game.display.get_width() / 2 - self.image.get_width() / 2
        self.y = 60
        
    def draw(self, y_offset: float):
        self.screen.game.display.blit(self.image, (self.x, self.y + y_offset))

BUTTON_BORDER_THICKNESS = 4

class MainMenuButton(ABC):
    def __init__(self, screen: MainMenuScreen, label: str):
        self.screen = screen
        self.font = screen.game.font_manager.get("comfortaa-bold", 27)
        self.text_surface = self.font.render(label, True, (255, 255, 255))
        self.border_radius = 0
        self.is_mouse_hovering = False
        
    def set_rect(self, rect: pygame.Rect):
        self.rect = rect
        self.border_rect = pygame.Rect(
            self.rect.x - BUTTON_BORDER_THICKNESS,
            self.rect.y - BUTTON_BORDER_THICKNESS,
            self.rect.width + BUTTON_BORDER_THICKNESS * 2,
            self.rect.height + BUTTON_BORDER_THICKNESS * 2
        )
        self.text_coords = (
            self.rect.x + self.rect.width / 2 - self.text_surface.get_width() / 2,
            self.rect.y + self.rect.height / 2 - self.text_surface.get_height() / 2
        )
        
    def draw(self, y_offset: float):
        pygame.draw.rect(self.screen.game.display, [255, 255, 255], self.border_rect.move(0, y_offset), border_radius=self.border_radius)
        pygame.draw.rect(self.screen.game.display, [119, 154, 209] if not self.is_mouse_hovering else [153, 180, 224], self.rect.move(0, y_offset), border_radius=self.border_radius)
        self.screen.game.display.blit(self.text_surface, (self.text_coords[0], self.text_coords[1] + y_offset))
        
    def on_screen_click(self):
        if (self.rect.collidepoint(pygame.mouse.get_pos())):
            self.on_click()
        
    @abstractmethod
    def on_click(self):
        pass
        
class MainMenuPlayButton(MainMenuButton):
    def __init__(self, screen: MainMenuScreen):
        super().__init__(screen, "Jugar")
        
    def on_click(self):
        print("Play game")
        
class MainMenuTimeTrialButton(MainMenuButton):
    def __init__(self, screen: MainMenuScreen):
        super().__init__(screen, "Contrarreloj")
        
    def on_click(self):
        print("Time trial")
        
class MainMenuSettingsButton(MainMenuButton):
    def __init__(self, screen: MainMenuScreen):
        super().__init__(screen, "Opciones")
        
    def on_click(self):
        self.screen.game.switch_screen(MainMenuScreen(self.screen.game))
        
class MainMenuExitButton(MainMenuButton):
    def __init__(self, screen: MainMenuScreen):
        super().__init__(screen, "Salir")
        
    def on_click(self):
        self.screen.game.stop()
        
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 60

class MainMenuButtonGroup():
    def __init__(self, screen: MainMenuScreen, initialY: int, vertical_margin: int):
        self.screen = screen
        self.is_mouse_hovering = False
        self.buttons = (
            MainMenuPlayButton(screen),
            MainMenuTimeTrialButton(screen),
            MainMenuSettingsButton(screen),
            MainMenuExitButton(screen)
        )
        for index, button in enumerate(self.buttons):
            button.set_rect(
                pygame.Rect(
                    screen.game.display.get_width() / 2 - BUTTON_WIDTH / 2,
                    initialY + BUTTON_HEIGHT * index + vertical_margin * index,
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
