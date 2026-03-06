# External
import pygame

# Internal
from systems import Card

# Hand Class
class Hand:
    def __init__(self) -> None:
        self.cards: list[Card] = []

    def clear(self) -> None:
        self.cards.clear()

    def add_card(self, card: Card) -> None:
        self.cards.append(card)
    
    def remove_card(self, card) -> None:
        self.cards.remove(card)

    def draw(self, surface: pygame.Surface) -> None:
        pass