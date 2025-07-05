import pygame
from util.asset_paths import image_path
from util.easing import ease_in_out_cubic

ENTER_TRANSITION_DELAY = 5
ENTER_TRANSITION_TOTAL_TICKS = 50

class GameBackground:
    def __init__(self, surface: pygame.Surface, should_transition: bool):
        self.surface = surface
        self.image = pygame.image.load(image_path("background.png"))
        self.__transition_delay = ENTER_TRANSITION_DELAY + 1 if should_transition else 0
        self.__transition_left_ticks = ENTER_TRANSITION_TOTAL_TICKS + 1 if should_transition else 0
        
    def transition_alpha(self):
        if (self.__transition_delay > 0):
            self.__transition_delay -= 1
            return 0
        if (self.__transition_left_ticks <= 0):
            return 255
        self.__transition_left_ticks -= 1
        max = ENTER_TRANSITION_TOTAL_TICKS
        progress = ENTER_TRANSITION_TOTAL_TICKS - self.__transition_left_ticks
        return int(ease_in_out_cubic(progress / max) * 255)
        
    def draw(self):
        alpha = self.transition_alpha()
        self.image.set_alpha(alpha)
        self.surface.blit(self.image, (0, 0))