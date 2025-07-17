from screen.component.button import Button, Alignment

class BackToMainMenuButton(Button):
    def __init__(self, screen: "GameScreen", label: str = "Regresar"):
        super().__init__(screen, label, Alignment.CENTER) 
        
    def on_click(self):
        from screen.main_menu_screen import MainMenuScreen
        self.screen.game.switch_screen(MainMenuScreen(self.screen.game))
        
from screen.base import GameScreen