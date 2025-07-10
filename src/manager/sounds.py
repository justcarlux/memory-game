import pygame
from manager.settings import SettingsManager
from util.asset_paths import music_path, sfx_path

MUSIC_FILENAME = "bgm.mp3"

class SoundManager:
    def __init__(self, settings: SettingsManager):
        self.settings = settings
        pygame.mixer.music.load(music_path(MUSIC_FILENAME), "mp3")
        self.sfx = {
            "click": pygame.mixer.Sound(sfx_path("click.wav"))
        }
        
    def play_music(self):
        pygame.mixer.music.play(loops=-1, fade_ms=500)
        
    def stop_music(self):
        pygame.mixer.music.fadeout(500)
        
    def play_sfx(self, name: str):
        if (self.settings.sfx_enabled):
            self.sfx[name].play()