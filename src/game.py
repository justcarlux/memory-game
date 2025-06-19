import pygame
import os

pygame.init()

ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

class GameBackground:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.initial_transition_ticks = 0
        self.image = pygame.image.load(os.path.join(ASSETS_PATH, "images", "background.png"))
        
    def draw(self):
        self.surface.blit(self.image, (0, 0))
        
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((900, 650))
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.background = GameBackground(self.screen)
        self.current_screen: GameScreen = MainMenuScreen(self)

    def run(self):
        while self.is_running:
            pygame.display.set_caption(f"Memoria - {int(self.clock.get_fps())} FPS")
            self.handle_events()
            
            self.background.draw()
            self.current_screen.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def stop(self):
        self.is_running = False
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.current_screen.on_click()
                
from screens.main_menu.main_menu import MainMenuScreen
from screens.base import GameScreen