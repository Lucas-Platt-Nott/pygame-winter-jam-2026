# External
import pygame

# Internal
from assets import Sounds
from config import *
from systems import Deck, Hand

# Poker Player Class
class PokerPlayer:
    def __init__(self) -> None:
        self._hand = Hand((0, -CARD_SIZE[1] * 0.5), True, True)
        self.freezes = 0
        self.chips = 0
        self.time_elapsed = 0
        self.cards_to_draw = 0
        self.draw_interval = 0.6
        
    @property
    def hand(self) -> Hand:
        return self._hand
    
    def queue_draw(self, amount: int) -> None:
        self.cards_to_draw += amount

    def draw_cards(self, deck: Deck, amount: int) -> None:
        for i in range(amount):
            card = deck.draw_card()
            self.hand.add(card)

    def update(self, deck: Deck, delta_time: float) -> None:

        if self.cards_to_draw > 0 and self.time_elapsed > self.draw_interval:
            self.time_elapsed = 0
            self.cards_to_draw -= 1
            self.draw_cards(deck, 1)
            Sounds.get_sound("card_draw").play()

        elif self.cards_to_draw > 0:
            self.time_elapsed += delta_time

        self.hand.update(delta_time)