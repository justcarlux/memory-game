import pygame
from manager.fonts import FontManager
from manager.sounds import SoundManager
from background import GameBackground
from settings import GameSettings
        
pygame.init()

INITIAL_MUSIC_DELAY = 40
INITIAL_MAIN_MENU_TRANSITION_DELAY = 20
        
class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((900, 650))
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.font_manager = FontManager()
        self.settings = GameSettings()
        self.sound_manager = SoundManager(self.settings)
        self.background = GameBackground(self.display)
        self.__current_screen: GameScreen = MainMenuScreen(self, INITIAL_MAIN_MENU_TRANSITION_DELAY)
        self.__next_screen: GameScreen | None = None
        self.__music_tick_delay_left = INITIAL_MUSIC_DELAY
        
    def handle_initial_music_playback(self):
        if (self.__music_tick_delay_left > 0):
            self.__music_tick_delay_left -= 1
        elif (self.__music_tick_delay_left == 0):
            self.__music_tick_delay_left = -1
            self.sound_manager.play_music(fade_ms=500)

    def run(self):
        while self.is_running:
            pygame.display.set_caption(f"Memoria - {int(self.clock.get_fps())} FPS")
            self.handle_events()
            self.handle_initial_music_playback()    
            self.handle_screen_switch()
            
            self.display.fill((0, 0, 0))
            self.background.draw()
            self.__current_screen.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
            
    def handle_screen_switch(self):
        if (self.__next_screen == None):
            return
        if (self.__current_screen.hidden):
            self.__current_screen = self.__next_screen
            self.__next_screen = None

    def stop(self):
        self.is_running = False
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.__current_screen.on_click()
                
    def switch_screen(self, screen: "GameScreen"):
        if (self.settings.transitions_enabled):
            self.__current_screen.hide()
            self.__next_screen = screen
        else:
            self.__current_screen = screen
        
from screen.base import GameScreen
from screen.main_menu import MainMenuScreen