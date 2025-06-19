from screens.base import GameScreen
from game import Game
from screens.main_menu.buttons import MainMenuButtonGroup
from screens.main_menu.title import MainMenuTitle

class MainMenuScreen(GameScreen):
    def __init__(self, game: Game):
        super().__init__(game)
        self.title = MainMenuTitle(game)
        self.button_group = MainMenuButtonGroup(game, 230, 30)

    def draw(self):
        self.title.draw()
        self.button_group.draw()
        
    def on_click(self):
        self.button_group.on_click()