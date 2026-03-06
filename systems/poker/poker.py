# External
import pygame

# Internal
from config import *
from systems import Player, Card
from systems.poker import Deck, Hand, PokerPlayer

# Poker System Class
class PokerSystem:
    def __init__(self, player: Player, opponent: PokerPlayer):
        self.renderer = PokerRenderSystem()

        self.player = player
        self.opponent = opponent

        self._deck = Deck(SUITS, RANKS)

    @property
    def deck(self) -> Deck:
        return self._deck
    
    def handle_event(self, event: pygame.Event) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.renderer.draw_player_hand(surface, self.player)
        self.renderer.draw_opponent_hand(surface, self.opponent)

        self.renderer.draw_deck(surface, self.deck)

# Poker Render System Class
class PokerRenderSystem:
    def __init__(self) -> None:
        pass

    def draw_deck(self, surface: pygame.Surface, deck: Deck) -> None:
        pass

    def draw_player_hand(self, surface: pygame.Surface, player: Player) -> None:
        pass
    
    def draw_opponent_hand(self, surface: pygame.Surface, opponent: PokerPlayer) -> None:
        pass