import pygame
import random
from util.asset_paths import image_path
from screen.base import GameScreen
from game import Game, GameScreen

ENTER_TRANSITION_TOTAL_TICKS = 50
ENTER_TRANSITION_STEP = 12

EXIT_TRANSITION_TOTAL_TICKS = 60
EXIT_TRANSITION_STEP = 12

class InGameCard:
    def __init__(self, screen: "InGameScreen", identifier: str, width: int, height: int):
        self.is_mouse_hovering = False
        self.screen = screen
        self.identifier = identifier
        self.loaded_empty_card_image = pygame.image.load(image_path("empty_card.png"))
        self.empty_card_image = pygame.transform.scale(self.loaded_empty_card_image, (width, height))
        self.loaded_image = pygame.image.load(image_path(identifier + ".png"))
        self.image = pygame.transform.scale(self.loaded_image, (width, height))
        self.rect = pygame.Rect(0, 0, width, height)
        self.is_flipped = False
        
    def set_coords(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, self.rect.width, self.rect.height)

    def draw(self, y_offset: float):
        if (self.is_flipped):
            self.screen.game.display.blit(self.image, (self.rect.x, self.rect.y + y_offset))
        else:
            self.screen.game.display.blit(self.empty_card_image, (self.rect.x, self.rect.y + y_offset))
            
    def on_screen_click(self):
        if (self.rect.collidepoint(pygame.mouse.get_pos())):
            self.on_click()
    
    def on_click(self):
        if (self.is_flipped): return
        self.screen.game.sound_manager.play_sfx("click")
        self.is_flipped = True
            
class InGameCardGroup:
    def __init__(self, screen: "InGameScreen"):
        self.screen = screen
        self.is_mouse_hovering = False
        self.rows = 3
        self.columns = 6
        self.card_width = 80
        self.card_height = 80
        self.margin = 15
        self.cards: list[InGameCard] = []
        for index in range(int(self.rows * self.columns / 2)):
            identifier = CARD_IDENTIFIERS[index]
            self.cards.append(InGameCard(self.screen, identifier, self.card_width, self.card_height))
            self.cards.append(InGameCard(self.screen, identifier, self.card_width, self.card_height))
        random.shuffle(self.cards)
        row = 0
        full_width = self.card_width * self.columns + (self.margin * (self.columns - 1))
        full_height = self.card_height * self.rows + (self.margin * (self.rows - 1))
        horizontal_padding = int((self.screen.game.display.get_width() - full_width) / 2)
        vertical_padding = int((self.screen.game.display.get_height() - full_height) / 2)
        for index, card in enumerate(self.cards):
            if (index != 0 and index % self.columns == 0):
                row += 1
            col = index % self.columns
            card.set_coords(
                horizontal_padding + self.card_width * col + (self.margin * col),
                vertical_padding + self.card_height * row + (self.margin * row)
            )
            
    def draw(self, y_offset: float):
        is_mouse_hovering = False
        for card in self.cards:
            card.is_mouse_hovering = card.rect.collidepoint(pygame.mouse.get_pos()) if not self.screen.is_transitioning() and not card.is_flipped else False
            card.draw(y_offset)
            if card.is_mouse_hovering:
                is_mouse_hovering = True
        self.is_mouse_hovering = is_mouse_hovering if not self.screen.is_transitioning() else False
        
    def on_click(self):
        for card in self.cards:
            card.on_screen_click()
        
CARD_IDENTIFIERS = ["card1", "card2", "card3", "card4", "card5", "card6", "card7", "card8", "card9"]

class InGameScreen(GameScreen):
    def __init__(self, game: Game, transition_delay: int = 0):
        super().__init__(
            game,
            ENTER_TRANSITION_TOTAL_TICKS,
            ENTER_TRANSITION_STEP,
            EXIT_TRANSITION_TOTAL_TICKS,
            EXIT_TRANSITION_STEP
        )
        self.card_group = InGameCardGroup(self)

    def draw(self):
        current_y_offset = self.transition_offset()
        if (current_y_offset < -400 and self._hiding):
            self.hidden = True
            return

        self.card_group.draw(current_y_offset)
        
        if self.card_group.is_mouse_hovering and not self.is_transitioning():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def on_click(self):
        self.card_group.on_click()