# External
import pygame

# Internal
from systems import Card
from systems.poker import Hand

# Poker Player Class
class PokerPlayer:
    def __init__(self) -> None:
        self._hand = Hand()
        self.chips = 0

    @property
    def hand(self) -> Hand:
        return self._hand
    
    def draw(self, surface: pygame.Surface) -> None:
        pass