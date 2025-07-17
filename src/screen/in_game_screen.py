import pygame
import random
from util.asset_paths import image_path
from screen.base import GameScreen
from game import Game, GameScreen
from util.easing import ease_in_out_cubic

FLIPPING_PROGRESS_STEP = 4

class InGameCard:
    def __init__(self, screen: "InGameScreen", identifier: str, width: int, height: int):
        self.width = width
        self.height = height
        self.is_mouse_hovering = False
        self.screen = screen
        self.identifier = identifier
        self.card_image = pygame.image.load(image_path(identifier + ".png"))
        self.rect = pygame.Rect(0, 0, width, height)
        self.is_flipped = False
        self.flipping_progress = 0
        
    def set_coords(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, self.rect.width, self.rect.height)

    def draw(self, y_offset: float):
        if (self.flipping_progress > 0):
            self.flipping_progress -= FLIPPING_PROGRESS_STEP
        
        width_progress = self.flipping_progress - 50 if self.flipping_progress > 50 else 50 - self.flipping_progress
        progress = ease_in_out_cubic(width_progress / 50) * 100
        
        if (self.is_flipped):
            image = self.card_image if self.flipping_progress <= 50 else self.screen.empty_card_image
        else:
            image = self.card_image if self.flipping_progress > 50 else self.screen.empty_card_image
        
        new_width = int(self.width * (progress / 100))
        target_image = pygame.transform.scale(image, (new_width, self.height))
       
        x_offset = self.width / 2 - target_image.get_width() / 2
        self.screen.game.display.blit(target_image, (self.rect.x + x_offset, self.rect.y + y_offset))
            
    def on_screen_click(self):
        if (self.rect.collidepoint(pygame.mouse.get_pos())):
            self.on_click()
            
    def flip(self):
        self.flipping_progress = 100
        self.is_flipped = not self.is_flipped
    
    def on_click(self):
        if (self.is_flipped): return
        self.screen.game.sound_manager.play_sfx("click")
        self.flip()
        
CARD_WIDTH = 80
CARD_HEIGHT = 80
            
class InGameCardGroup:
    def __init__(self, screen: "InGameScreen", rows: int, columns: int):
        self.screen = screen
        self.is_mouse_hovering = False
        self.rows = rows
        self.columns = columns
        self.margin = 15
        self.cards: list[InGameCard] = []
        for index in range(int(self.rows * self.columns / 2)):
             identifier = CARD_IDENTIFIERS[index]
             self.cards.append(InGameCard(self.screen, identifier, CARD_WIDTH, CARD_HEIGHT))
             self.cards.append(InGameCard(self.screen, identifier, CARD_WIDTH, CARD_HEIGHT))
        random.shuffle(self.cards)
        row = 0
        full_width = CARD_WIDTH * self.columns + (self.margin * (self.columns - 1))
        full_height = CARD_HEIGHT * self.rows + (self.margin * (self.rows - 1))
        horizontal_padding = int((self.screen.game.display.get_width() - full_width) / 2)
        vertical_padding = int((self.screen.game.display.get_height() - full_height) / 2)
        for index, card in enumerate(self.cards):
            if (index != 0 and index % self.columns == 0):
                row += 1
            col = index % self.columns
            card.set_coords(
                horizontal_padding + CARD_WIDTH * col + (self.margin * col),
                vertical_padding + CARD_HEIGHT * row + (self.margin * row)
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
    def __init__(self, game: Game, rows: int, columns: int):
        super().__init__(game)
        self.card_group = InGameCardGroup(self, rows, columns)
        self.empty_card_image = pygame.image.load(image_path("empty_card.png"))
        self.found_pairs: list[str] = []

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