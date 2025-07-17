from screen.base import GameScreen
from screen.component.image_wrappers import HorizontallyAlignedImage

class GameTitleImage(HorizontallyAlignedImage):
    def __init__(self, screen: GameScreen):
        super().__init__(screen, "title.png", 60) 