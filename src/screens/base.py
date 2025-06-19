from abc import ABC, abstractmethod
from game import Game

class GameScreen(ABC):
    def __init__(self, game: Game):
        self.game = game
    
    @abstractmethod
    def draw(self):
        pass
    
    @abstractmethod
    def on_click(self):
        pass