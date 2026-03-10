# Built-In
import random

# Internal
from systems import Card

# Deck Class
class Deck:
    def __init__(self, types, suits, ranks) -> None:
        self.card_types = types
        self.card_suits = suits
        self.card_ranks = ranks

        self.cards: list[Card] = []
        self.standard_cards: list[Card] = [
            Card(type, suit, rank)
            for type in self.card_types
            for suit in self.card_suits
            for rank in self.card_ranks
        ]

        self.shuffle()
        
    def shuffle(self) -> None:
        self.cards = self.standard_cards.copy()

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self, card: Card) -> None:
        self.cards.remove(card)

    def draw_card(self) -> Card:
        card = random.choice(self.cards)
        self.remove_card(card)

        if len(self.cards) == 0:
            self.shuffle()
        
        return card