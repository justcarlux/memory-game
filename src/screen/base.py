from abc import ABC, abstractmethod
from game import Game
from util.easing import ease_in_out_cubic

ENTER_TRANSITION_TOTAL_TICKS = 50
ENTER_TRANSITION_STEP = 12

EXIT_TRANSITION_TOTAL_TICKS = 60
EXIT_TRANSITION_STEP = 14

class GameScreen(ABC):
    def __init__(self, game: Game, enter_transition_total_ticks: int = ENTER_TRANSITION_TOTAL_TICKS, enter_transition_step: int = ENTER_TRANSITION_STEP, exit_transition_total_ticks: int = ENTER_TRANSITION_TOTAL_TICKS, exit_transition_step: int = EXIT_TRANSITION_STEP):
        self.game = game
        self._hiding = False
        self.hidden = False
        self.__transition_left_ticks = enter_transition_total_ticks + 1 if self.game.settings.transitions_enabled else 0
        self.__enter_transition_total_ticks = enter_transition_total_ticks
        self.__enter_transition_step = enter_transition_step
        self.__exit_transition_total_ticks = exit_transition_total_ticks
        self.__exit_transition_step = exit_transition_step
        
    def transition_offset(self):
        if (self.__transition_left_ticks <= 0):
            return 0
        self.__transition_left_ticks -= 1
        if (self._hiding):
            current = self.__exit_transition_total_ticks - self.__transition_left_ticks
            progress = current / self.__exit_transition_total_ticks
            return -(ease_in_out_cubic(progress) * self.__exit_transition_total_ticks * self.__exit_transition_step)
        else:
            max = self.__enter_transition_total_ticks * self.__enter_transition_step
            current = self.__transition_left_ticks * self.__enter_transition_step
            progress = (max - current) / max
            return max - (ease_in_out_cubic(progress) * max)
    
    def is_transitioning(self):
        return self.__transition_left_ticks > 0
    
    def hide(self):
        self._hiding = True
        self.__transition_left_ticks = self.__exit_transition_total_ticks + 1
    
    @abstractmethod
    def draw(self):
        pass
    
    @abstractmethod
    def on_click(self):
        pass
    
    