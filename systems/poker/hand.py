# External
import pygame

# Internal
from config import *
from systems.poker import Deck
from systems import Card

# Hand Class
class Hand:
    def __init__(self) -> None:
        self._surface = pygame.Surface((
            CARD_SIZE[0] * 6,
            CARD_SIZE[1] * 2
        ))

        self._cards: list[CardData] = []

    @property
    def surface(self) -> pygame.Surface:
        return self._surface
    
    @surface.setter
    def surface(self, instance) -> None:
        self._surface = instance

    @property
    def cards(self) -> list[str]:
        return self._cards
        
    def clear(self) -> None:
        self.cards.clear()

    def add_card(self, card_name: str) -> None:
        self.cards.append(card_name)

    def draw_cards(self, deck: Deck, amount: int) -> None:
        for i in range(amount):
            self.add_card(deck.draw_card())
    
    def remove_card(self, card_name: str) -> None:
        self.cards.remove(card_name)

    def draw(self, surface: pygame.Surface) -> None:
        pass

class CardData:
    def __init__(self, card_name) -> None:
        self.time_elapsed = 0
        self.hovered = False
        self.card_name = card_name

    def hover(self) -> None:
        self.time_elapsed = 0
        self.hovered = True

    def unhover(self) -> None:
        self.time_elapsed = 0
        self.hovered = False