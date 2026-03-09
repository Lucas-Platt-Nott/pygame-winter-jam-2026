# External
import pygame
from pygame.locals import *

# Internal
from assets import Images, Sounds
from core import SceneManager, Scene
from config import *
from systems import PokerPlayer, Player, Hand, Deck

# Poker Class
class Poker(Scene):
    def __init__(self, scene_manager: SceneManager, player: Player) -> None:
        self.scene_manager = scene_manager
        self.player = player

        # HAND DEMO CODE
        self.hand = Hand((0, 0), False, False)
        self.deck = Deck(TYPES, SUITS, RANKS)

        # HAND DEMO CODE

    def start(self) -> None:
        pass

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == KEYDOWN:
            if event.dict["key"] == K_0:
                self.hand.add(self.deck.draw_card())

        elif event.type == MOUSEBUTTONDOWN:
            self.hand.handle_click(event)

    def update(self, delta_time: float) -> None:
        self.hand.update(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        self.hand.draw(surface, (0, 0))