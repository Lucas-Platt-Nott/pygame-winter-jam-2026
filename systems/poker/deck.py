# Built-In
import random

# Internal
from systems import Card

# Deck Class
class Deck:
    def __init__(self, suits, ranks) -> None:
        self.card_suits = suits
        self.card_ranks = ranks

        self.cards: list[str] = []
        self.standard_cards: list[str] = [
            f"default_{suit}_{rank}"
            for suit in self.card_suits
            for rank in self.card_ranks
        ]

    def shuffle(self) -> None:
        self.cards = self.standard_cards.copy()

    def add_card(self, card_name: str) -> None:
        self.cards.append(card_name)

    def remove_card(self, card_name: str) -> None:
        self.cards.remove(card_name)

    def draw_card(self) -> str:
        card_name = random.choice(self.cards)
        self.remove_card(card_name)
        
        return card_name