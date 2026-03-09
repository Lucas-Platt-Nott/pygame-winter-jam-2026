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
        self.opponent = PokerPlayer()
        self.deck = Deck(TYPES, SUITS, RANKS)


    def start(self) -> None:
        pass

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == KEYDOWN:
            key = event.dict["key"]
            if key == K_1:
                self.player.hand.add(self.deck.draw_card())

            elif key == K_2:
                self.player.hand.remove(self.player.hand.cards[-1])

            elif key == K_3:
                self.opponent.hand.add(self.deck.draw_card())

            elif key == K_4:
                self.opponent.hand.remove(self.opponent.hand.cards[-1])

        elif event.type == MOUSEBUTTONDOWN:
            self.player.hand.handle_click(event)

    def update(self, delta_time: float) -> None:
        self.player.hand.update(delta_time)
        self.opponent.hand.update(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        self.player.hand.draw(surface)
        self.opponent.hand.draw(surface)