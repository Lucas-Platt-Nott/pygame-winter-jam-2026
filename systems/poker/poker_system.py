# Built-In
from __future__ import annotations
import math

# External
import pygame
from pygame.locals import *

# Internal
from assets import Images
from config import *
import systems.player
from systems.poker import Deck, Hand, PokerPlayer

# Poker Renderer Class
class PokerRenderer:
    def __init__(self) -> None:
        self.hand_width = CARD_SIZE[0] * 5

    def render_hand(self, hand, hidden=False):
        width, height = CARD_SIZE
        num_cards = len(hand.cards)

        spacing = width * 0.75          # horizontal spacing
        max_angle = 8               # very small rotation
        curve_height = 20           # subtle vertical arc

        surface_width = int(width + spacing * (num_cards - 1) + 40)
        surface_height = height + curve_height + 40

        surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)

        mid = (num_cards - 1) / 2
        center_x = surface_width / 2

        card = Images.get_image("card_back")

        for index, card_name in enumerate(hand.cards):
            if not hidden:
                card = Images.get_image(card_name)

            position_magnitude = (index - mid) / mid if mid != 0 else 0  # -1 → 1

            # smoother rotation curve
            angle = -max_angle * (position_magnitude ** 3)

            # shallow vertical curve
            y_offset = curve_height * (position_magnitude ** 2)

            rotated = pygame.transform.rotate(card, angle)
            rect = rotated.get_rect()

            x = center_x + (index - mid) * spacing
            y = 20 + y_offset

            rect.center = (x, y + height/2)

            surface.blit(rotated, rect)

        return surface
    
    def draw(self, surface: pygame.Surface, poker: PokerSystem) -> None:
        center_y = SCREEN_SIZE[1] // 2
        center_x = SCREEN_SIZE[0] // 2

        player_hand = poker.player.hand
        surface.blit(player_hand.surface, (
            center_x - player_hand.surface.width // 2,
            SCREEN_SIZE[1] - player_hand.surface.height + 50
        ))

        opponent_hand = poker.opponent.hand
        surface.blit(opponent_hand.surface, (
            center_x - opponent_hand.surface.width // 2,
            -50
        ))

# Poker System Class
class PokerSystem:
    def __init__(self, player: systems.Player, opponent: PokerPlayer):
        self.renderer = PokerRenderer()

        self.player = player
        self.opponent = opponent

        self._deck = Deck(SUITS, RANKS)

    @property
    def deck(self) -> Deck:
        return self._deck
    
    def start(self) -> None:
        self.player.reset()
        self.opponent = PokerPlayer()

        self.deck.refill()
        self.draw_cards(self.player.hand, 5)
        self.draw_cards(self.opponent.hand, 5, hidden=True)

    def draw_cards(self, hand, amount, hidden=False) -> None:
        hand.draw_cards(self.deck, amount)
        hand.surface = self.renderer.render_hand(hand, hidden=hidden)

        if hidden:
            hand.surface = pygame.transform.rotate(hand.surface, 180)

    def handle_motion(self, event: pygame.Event) -> None:
        pass
    
    def update(self, delta_time: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.renderer.draw(surface, self)