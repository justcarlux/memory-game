from abc import ABC, abstractmethod
from game import Game

class GameScreen(ABC):
    def __init__(self, game: Game):
        self.game = game
        self._hiding = False
        self.hidden = False
    
    @abstractmethod
    def draw(self):
        pass
    
    def hide(self):
        self._hiding = True
    
    @abstractmethod
    def on_click(self):
        pass
    