import pygame
import random
from enum import Enum
from util.asset_paths import image_path
from screen.base import GameScreen
from game import Game, GameScreen
from util.easing import ease_in_out_cubic
from screen.component.button import Button, Alignment
from game import GAME_TIMER_EVENT
from screen.time_out_screen import TimeOutScreen

CARD_FLIPPING_PROGRESS_STEP = 4

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
            self.flipping_progress -= CARD_FLIPPING_PROGRESS_STEP
        
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
        self.reset_cards_ticks = -1

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

        if (self.reset_cards_ticks > 0):
            self.reset_cards_ticks -= 1
        if (self.reset_cards_ticks == 100):
            self.flip_all()
        if (self.reset_cards_ticks == 0):
            self.reset_cards_ticks = -1
            self.reset()

        is_mouse_hovering = False
        for card in self.cards:
            card.is_mouse_hovering = card.rect.collidepoint(pygame.mouse.get_pos()) if not self.screen.is_transitioning() and not card.is_flipped and not card.is_flipping() else False
            card.draw(y_offset)
            if card.is_mouse_hovering:
                is_mouse_hovering = True
        self.is_mouse_hovering = is_mouse_hovering if not self.screen.is_transitioning() and self.interactive and len(self.get_selected_cards()) < 2 else False
        
    def reset(self):
        self.cards.clear()
        self.__populate_cards()
        self.__align_images_in_grid()
        self.screen.card_display_time = self.screen.difficulty.card_display_time - 50
        self.found_pairs.clear()
        self.screen.elapsed_time = 0

    def on_click(self):
        if (not self.interactive or len(self.get_selected_cards()) >= 2): return
        for card in self.cards:
            card.on_screen_click()
        self.__queue_selected_flip_if_needed()
        self.__check_for_win()

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
            self.queued_card_flip_ticks = 25

    def __flip_queued_cards(self):
        for card in self.cards:
            if (card.identifier in self.cards_queued_for_flipping and card.is_flipped):
                card.flip()

    def __check_for_win(self):
        all_flipped = True
        for card in self.cards:
            if (not card.is_flipped):
                all_flipped = False
                break
        if (all_flipped):
            self.screen.timer_active = False
            self.interactive = False
            self.reset_cards_ticks = 200
            self.screen.level += 1
            self.screen.add_points()

class InGameInfoDisplay:
    def __init__(self, screen: "InGameScreen"):
        self.screen = screen
        self.font = screen.game.font_manager.get("comfortaa-bold", 22)

    def draw(self, y_offset: float):
        self.__update_info()
        self.__draw_centered_text(self.time_left, 20 + y_offset)
        self.__draw_centered_text(self.points, 45 + y_offset)
        self.__draw_centered_text(self.level, 70 + y_offset)

    def __draw_centered_text(self, label: str, y: float):
        text = self.font.render(label, True, (255, 255, 255))
        x = self.screen.game.display.get_width() / 2 - text.get_width() / 2
        self.screen.game.display.blit(text, (x, y))

    def __update_info(self):
        time_left_minutes = self.screen.time_left // 60
        time_left_seconds = self.screen.time_left - (time_left_minutes * 60)
        self.time_left = f"{str.rjust(str(time_left_minutes), 2, "0")}:{str.rjust(str(time_left_seconds), 2, "0")}"
        self.points = f"Puntos: {self.screen.points}"
        self.level = f"Nivel: {self.screen.level}"

class InGameDifficulty(Enum):
    EASY = (1, 1.0, 3, 4, 120, 220) 
    MEDIUM = (2, 1.5, 4, 7, 150, 290)
    HARD = (3, 2.0, 5, 8, 180, 400)

    def __init__(self, value: int, multiplier: float, rows: int, columns: int, game_time: int, card_display_time: int):
        self._value_ = value
        self.multiplier = multiplier
        self.rows = rows
        self.columns = columns
        self.game_time = game_time
        self.card_display_time = card_display_time
        
class BackToMainMenuButton(Button):
    def __init__(self, screen: "InGameScreen"):
        super().__init__(screen, "Salir", Alignment.CENTER)
        self.in_game_screen = screen
        
    def on_click(self):
        stored_points = self.screen.game.storage.get_difficulty_record(self.in_game_screen.difficulty.value)
        new_record = self.in_game_screen.points > stored_points
        if (new_record):
            self.screen.game.storage.set_difficulty_record(self.in_game_screen.difficulty.value, self.in_game_screen.points)
        from screen.main_menu_screen import MainMenuScreen
        self.screen.game.switch_screen(MainMenuScreen(self.screen.game))

class InGameScreen(GameScreen):
    def __init__(self, game: Game, difficulty: InGameDifficulty):
        super().__init__(game, 50, 14)
        self.difficulty = difficulty
        self.card_group = InGameCardGroup(self, difficulty.rows, difficulty.columns)
        self.empty_card_image = pygame.image.load(image_path("empty_card.png"))
        self.card_display_time = difficulty.card_display_time
        self.back_button = BackToMainMenuButton(self)
        back_button_width = 250
        self.back_button.set_rect(
            pygame.Rect(game.display.get_width() / 2 - back_button_width / 2, 563, back_button_width, 60)
        )
        self.points = 0
        self.level = 1
        self.time_left = difficulty.game_time
        self.elapsed_time = 0
        self.timer_active = False
        self.game_info_display = InGameInfoDisplay(self)

    def draw(self):
        current_y_offset = self.transition_offset()
        if (current_y_offset < -600 and self._hiding):
            self.hidden = True
            return
        if (not self.is_transitioning() and self.time_left == 0):
            stored_points = self.game.storage.get_difficulty_record(self.difficulty.value)
            new_record = self.points > stored_points
            if (new_record):
                self.game.storage.set_difficulty_record(self.difficulty.value, self.points)
            self.game.switch_screen(TimeOutScreen(self.game, self.points, new_record))
            
        if (self.card_display_time == 0):
            self.card_display_time = -1
            self.card_group.flip_all()
            self.card_group.interactive = True
            pygame.time.set_timer(GAME_TIMER_EVENT, millis=1000)
            self.timer_active = True
        elif (self.card_display_time == self.difficulty.card_display_time - 50):
            self.card_group.flip_all()

        if (self.card_display_time > 0):
            self.card_display_time -= 1

        self.game_info_display.draw(current_y_offset)
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

    def add_points(self):
        base_points = max(0, self.difficulty.game_time - self.elapsed_time)
        self.points += int(base_points * self.difficulty.multiplier)

    def on_game_timer_tick(self):
        if (self.timer_active):
            self.time_left -= 1
            self.elapsed_time += 1