# Built-In
from __future__ import annotations
import math

# External
import pygame
from pygame.locals import *

# Internal
from assets import Images
from config import *
from systems.poker import Deck, Hand, PokerPlayer, CardData

class PokerRenderer:
    HOVER_LIFT = 20  # pixels to lift hovered cards

    def render_hand(self, hand, hidden=False):
        """Render a hand, update card rects and return the surface."""
        width, height = CARD_SIZE
        num = len(hand.cards)

        spacing = width * 0.75
        max_angle = 8
        curve_h = 20

        surf_w = int(width + spacing * (num - 1) + 40)
        surf_h = height + curve_h + 40 + self.HOVER_LIFT
        surface = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)

        mid = (num - 1) / 2 or 1
        cx = surf_w / 2

        for i, card_data in enumerate(hand.cards):

            # Choose back image if hidden
            card_image = Images.get_image(
                "card_back" if hidden else card_data.card_name
            )

            # normalized position: -1 (left) → 0 (center) → 1 (right)
            normalized_position = (i - mid) / mid

            angle = -max_angle * normalized_position**3
            y_off = curve_h * normalized_position**2

            # lift card if hovered
            lift = self.HOVER_LIFT if card_data.hovered else 0

            rotated = pygame.transform.rotate(card_image, angle)
            rect = rotated.get_rect(center=(
                cx + (i - mid) * spacing,
                20 + y_off + height / 2 - lift
            ))

            surface.blit(rotated, rect)

            # store hitbox
            card_data.rect = rect

        hand.surface = surface
        return surface

    def draw(self, surface: pygame.Surface, poker: PokerSystem) -> None:
        """Draw both player and opponent hands on the main surface."""
        center_x = SCREEN_SIZE[0] // 2

        player_hand = poker.player.hand
        opponent_hand = poker.opponent.hand

        # Render hands
        self.render_hand(player_hand, hidden=False)
        self.render_hand(opponent_hand, hidden=True)
        opponent_hand.surface = pygame.transform.rotate(opponent_hand.surface, 180)

        # Compute positions
        player_pos = (
            center_x - player_hand.surface.get_width() // 2,
            SCREEN_SIZE[1] - player_hand.surface.get_height() + 70
        )
        opponent_pos = (
            center_x - opponent_hand.surface.get_width() // 2,
            -70
        )

        # Blit surfaces
        surface.blit(player_hand.surface, player_pos)
        surface.blit(opponent_hand.surface, opponent_pos)

        # store offsets for click detection / hover
        player_hand.render_offset = player_pos
        opponent_hand.render_offset = opponent_pos

    # ----------------------------
    # Utility for interaction
    # ----------------------------

    def update_hover(self, hand: Hand, mouse_pos) -> None:
        altered_pos = pygame.Vector2(mouse_pos)
        altered_pos -= hand.render_offset

        for card in hand.cards:
            if card.rect and card.rect.collidepoint(altered_pos):
                card.hover()
            else:
                card.unhover()

    def get_clicked_card(self, hand: list[CardData], mouse_pos) -> CardData | None:
        for card in hand:
            if card.rect and card.rect.collidepoint(mouse_pos):
                return card
        return None

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
        self.draw_cards(self.opponent.hand, 5)

    def draw_cards(self, hand, amount) -> None:
        hand.draw_cards(self.deck, amount)

    def handle_motion(self, event: pygame.Event) -> None:
        self.renderer.update_hover(self.player.hand, event.dict["pos"])

    def update(self, delta_time: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.renderer.draw(surface, self)