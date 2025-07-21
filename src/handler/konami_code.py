import pygame
from manager.sounds import SoundManager

class KonamiCodeHandler:
    def __init__(self, sound_manager: SoundManager):
        self.sound_manager = sound_manager
        self.sequence: tuple[int, int, int, int, int, int, int, int, int, int] = (
            pygame.K_UP,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_DOWN,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_b,
            pygame.K_a
        )
        self.current_key_index = 0
        
    def handle_key(self, key: int):
        if (self.sequence[self.current_key_index] == key):
            self.current_key_index += 1
        else:
            self.current_key_index = 0
            
        if (self.current_key_index >= len(self.sequence)):
            self.current_key_index = 0
            self.__on_done()
        
    def __on_done(self):
        self.sound_manager.play_sfx("goku")