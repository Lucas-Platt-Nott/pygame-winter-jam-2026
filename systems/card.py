# External
import pygame

# Internal
from assets import Images
from config import VALUES

# Card Class
class Card:
    def __init__(self, card_type: str, card_suit: str, card_rank: str) -> None:
        self._type = card_type
        self._suit = card_suit
        self._rank = card_rank
        self._value = VALUES[self._rank]

    @property
    def type(self) -> str:
        return self._type
    
    @property
    def suit(self) -> str:
        return self._suit
    
    @property
    def rank(self) -> str:
        return self._rank

    @property
    def value(self) -> int:
        return self._value
    
    def draw(self, surface: pygame.Surface, position: tuple[int, int]) -> None:
        card_image = Images.get_image(f"{self.type}_{self.suit}_{self.rank}")
        surface.blit(card_image, position)