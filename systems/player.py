# Built-In
from __future__ import annotations

# External
import pygame

# Internal
from systems import PokerPlayer

# Player Class
class Player(PokerPlayer):
    def __init__(self) -> None:
        super().__init__()

    def reset(self) -> None:
        pass