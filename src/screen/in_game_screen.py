import pygame
import random
from util.asset_paths import image_path
from screen.base import GameScreen
from game import Game, GameScreen
from util.easing import ease_in_out_cubic
from screen.component.back_to_main_menu_button import BackToMainMenuButton

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
        if (self.rect.collidepoint(pygame.mouse.get_pos()) and not self.is_flipping()):
            self.on_click()

    def is_flipping(self):
        return self.flipping_progress != 0
            
    def flip(self):
        self.flipping_progress = 100
        self.is_flipped = not self.is_flipped
    
    def on_click(self):
        if (self.is_flipped): return
        self.screen.game.sound_manager.play_sfx("click")
        self.flip()
        
CARD_WIDTH = 80
CARD_HEIGHT = 80

GAME_AVAILABLE_CARDS = 24
AVAILABLE_CARDS = [f"card{i}" for i in range(1, GAME_AVAILABLE_CARDS + 1)]
            
class InGameCardGroup:
    def __init__(self, screen: "InGameScreen", rows: int, columns: int):
        self.screen = screen
        self.is_mouse_hovering = False
        self.rows = rows
        self.columns = columns
        self.margin = 6
        self.cards: list[InGameCard] = []
        self.__populate_cards()
        self.__align_images_in_grid()
        self.interactive = False
        self.found_pairs: list[str] = []
        self.queued_card_flip_ticks = -1
        self.cards_queued_for_flipping: list[str] = []

    def __populate_cards(self):
        random.shuffle(AVAILABLE_CARDS) # mutating the original list is not a problem here
        for index in range(int(self.rows * self.columns / 2)):
             identifier = AVAILABLE_CARDS[index]
             self.cards.append(InGameCard(self.screen, identifier, CARD_WIDTH, CARD_HEIGHT))
             self.cards.append(InGameCard(self.screen, identifier, CARD_WIDTH, CARD_HEIGHT))
        random.shuffle(self.cards)
    
    def __align_images_in_grid(self):
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
        if (self.queued_card_flip_ticks > 0):
            self.queued_card_flip_ticks -= 1
        elif (self.queued_card_flip_ticks == 0):
            self.queued_card_flip_ticks = -1
            self.__flip_queued_cards()

        is_mouse_hovering = False
        for card in self.cards:
            card.is_mouse_hovering = card.rect.collidepoint(pygame.mouse.get_pos()) if not self.screen.is_transitioning() and not card.is_flipped and not card.is_flipping() else False
            card.draw(y_offset)
            if card.is_mouse_hovering:
                is_mouse_hovering = True
        self.is_mouse_hovering = is_mouse_hovering if not self.screen.is_transitioning() and self.interactive and len(self.get_selected_cards()) < 2 else False
        
    def on_click(self):
        if (not self.interactive or len(self.get_selected_cards()) >= 2): return
        for card in self.cards:
            card.on_screen_click()
        self.__queue_selected_flip_if_needed()
        # self.check_for_game_win()

    def flip_all(self):
        for card in self.cards:
            card.flip()

    def get_selected_cards(self):
        selected_cards: list[str] = []
        for card in self.cards:
            if (card.identifier in self.found_pairs): continue
            if (card.is_flipped):
                selected_cards.append(card.identifier)
        return selected_cards
    
    def __queue_selected_flip_if_needed(self):
        selected_cards = self.get_selected_cards()
        if (len(selected_cards) < 2): return
        if (selected_cards[0] == selected_cards[1]):
            self.found_pairs.append(selected_cards[0])
        else:
            self.cards_queued_for_flipping = selected_cards
            self.queued_card_flip_ticks = 35

    def __flip_queued_cards(self):
        for card in self.cards:
            if (card.identifier in self.cards_queued_for_flipping and card.is_flipped):
                card.flip()

class InGameScreen(GameScreen):
    def __init__(self, game: Game, rows: int, columns: int, initial_points: int):
        super().__init__(game)
        self.card_group = InGameCardGroup(self, rows, columns)
        self.empty_card_image = pygame.image.load(image_path("empty_card.png"))
        self.initial_card_display_time = 250
        self.initial_points = initial_points
        self.back_button = BackToMainMenuButton(self)
        self.back_button.set_rect(
            pygame.Rect(game.display.get_width() / 2 - 125, 563, 250, 60)
        )

    def draw(self):
        current_y_offset = self.transition_offset()
        if (current_y_offset < -400 and self._hiding):
            self.hidden = True
            return
        if (self.initial_card_display_time == 0):
            self.initial_card_display_time = -1
            self.card_group.flip_all()
            self.card_group.interactive = True
        elif (self.initial_card_display_time == 190):
            self.card_group.flip_all()

        if (self.initial_card_display_time > 0):
            self.initial_card_display_time -= 1

        self.card_group.draw(current_y_offset)

        self.back_button.is_mouse_hovering = self.back_button.rect.collidepoint(pygame.mouse.get_pos()) if not self.is_transitioning() else False
        self.back_button.draw(current_y_offset)

        if (self.card_group.is_mouse_hovering or self.back_button.is_mouse_hovering) and not self.is_transitioning():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def on_click(self):
        self.card_group.on_click()
        self.back_button.on_screen_click()