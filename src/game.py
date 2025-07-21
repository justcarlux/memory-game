import pygame
from storage import StorageDriver
from manager.fonts import FontManager
from manager.sounds import SoundManager
from screen.component.background import GameBackground
from manager.settings import SettingsManager
from handler.konami_code import KonamiCodeHandler

INITIAL_MUSIC_DELAY = 40
INITIAL_MAIN_MENU_TRANSITION_DELAY = 20

GAME_TIMER_EVENT = pygame.USEREVENT + 1


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((900, 650))
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.storage = StorageDriver()
        self.font_manager = FontManager()
        self.settings = SettingsManager(self.storage)
        self.sound_manager = SoundManager(self.settings)
        self.background = GameBackground(
            self.display, self.settings.transitions_enabled)
        self.__current_screen: GameScreen = MainMenuScreen(
            self, INITIAL_MAIN_MENU_TRANSITION_DELAY if self.settings.transitions_enabled else 0)
        self.__next_screen: GameScreen | None = None
        self.__music_tick_delay_left = INITIAL_MUSIC_DELAY if self.settings.music_enabled else -1
        self.konami_code_handler = KonamiCodeHandler(self.sound_manager)

    def handle_initial_music_playback(self):
        if (self.__music_tick_delay_left > 0):
            self.__music_tick_delay_left -= 1
        elif (self.__music_tick_delay_left == 0):
            self.__music_tick_delay_left = -1
            self.sound_manager.play_music()

    def run(self):
        while self.is_running:
            pygame.display.set_caption(
                f"Memoria - {int(self.clock.get_fps())} FPS")
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
        self.storage.close()
        self.is_running = False

    def handle_events(self):
        from screen.in_game_screen import InGameScreen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.__current_screen.is_transitioning():
                self.__current_screen.on_click()
            elif event.type == GAME_TIMER_EVENT:
                if isinstance(self.__current_screen, InGameScreen):
                    self.__current_screen.on_game_timer_tick()
            elif event.type == pygame.KEYDOWN:
                self.konami_code_handler.handle_key(event.key)
                
    def switch_screen(self, screen: "GameScreen"):
        if (self.settings.transitions_enabled):
            self.__current_screen.hide()
            self.__next_screen = screen
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.__current_screen = screen
        
from screen.base import GameScreen
from screen.main_menu_screen import MainMenuScreen