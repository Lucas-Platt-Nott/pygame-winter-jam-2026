# Built-In
from __future__ import annotations

# External
import pygame

# Internal
from config import *
from systems import PokerPlayer, Hand

# Player Class
class Player(PokerPlayer):
    def __init__(self) -> None:
        super().__init__()
        self._hand = Hand((0, SCREEN_SIZE[1] - CARD_SIZE[1] * 1.5))

    def reset(self) -> None:
        self.time_elapsed = 0
        self.cards_to_draw = 0
        self.hand.cards.clear()