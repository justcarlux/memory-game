import pygame
from settings import GameSettings
from util.asset_paths import music_path

class MusicInfo:
    def __init__(self, label: str, filename: str):
        self.label = label
        self.filename = filename

class SoundManager:
    def __init__(self, settings: GameSettings):
        self.settings = settings
        self.music_list = (
            MusicInfo("Dire Dire Docks from Super Mario 64 (Slightly Slower Version)", "bgm1.mp3"),
        )
        self.__currently_played_music_index = -1
        
    def play_music(self, index: int = 0, fade_ms: int = 0):
        path = music_path(self.music_list[index].filename)
        pygame.mixer.music.unload()
        pygame.mixer.music.load(path, "mp3")
        pygame.mixer.music.play(loops=-1, fade_ms=fade_ms)
        self.__currently_played_music_index = index
        
    def get_currently_played_music(self):
        if (self.__currently_played_music_index == -1):
            return None
        return self.music_list[self.__currently_played_music_index]