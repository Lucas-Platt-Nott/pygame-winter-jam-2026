# External
import pygame

# Internal
from config import *
from systems.poker import Deck


class CardData:
    def __init__(self, card_name: str) -> None:
        self.card_name = card_name

        # animation / state
        self.time_elapsed = 0
        self.hovered = False

        # hitbox (set by renderer)
        self.rect: pygame.Rect | None = None

    def hover(self) -> None:
        self.time_elapsed = 0
        self.hovered = True

    def unhover(self) -> None:
        self.time_elapsed = 0
        self.hovered = False

    def contains_point(self, pos) -> bool:
        if self.rect is None:
            return False
        return self.rect.collidepoint(pos)

# Hand Class
class Hand:
    def __init__(self) -> None:
        self._surface = pygame.Surface(
            (CARD_SIZE[0] * 6, CARD_SIZE[1] * 2),
            pygame.SRCALPHA
        )

        self._cards: list[CardData] = []
        self.render_offset = (0, 0)

    @property
    def surface(self) -> pygame.Surface:
        return self._surface

    @surface.setter
    def surface(self, instance) -> None:
        self._surface = instance

    @property
    def cards(self) -> list[CardData]:
        return self._cards

    def clear(self) -> None:
        self._cards.clear()

    def add_card(self, card_name: str) -> None:
        self._cards.append(CardData(card_name))

    def draw_cards(self, deck: Deck, amount: int) -> None:
        for _ in range(amount):
            self.add_card(deck.draw_card())

    def remove_card(self, card: CardData) -> None:
        self._cards.remove(card)

    def get_card_at_pos(self, pos) -> CardData | None:
        for card in reversed(self._cards):
            if card.contains_point(pos):
                return card
        return None

    def update_hover(self, mouse_pos) -> None:
        hovered_card = self.get_card_at_pos(mouse_pos)

        for card in self._cards:
            if card is hovered_card:
                card.hover()
            else:
                card.unhover()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, (0, 0))