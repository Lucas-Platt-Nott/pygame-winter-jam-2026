# External
import pygame

# Internal
from config import *
from systems import Hand

# Poker Player Class
class PokerPlayer:
    def __init__(self) -> None:
        self._hand = Hand((0, -CARD_SIZE[1] * 0.5), True, True)

    @property
    def hand(self) -> Hand:
        return self._hand