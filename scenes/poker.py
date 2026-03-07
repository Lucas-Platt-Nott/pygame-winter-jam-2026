# External
import pygame
from pygame.locals import *

# Internal
from assets import Images, Sounds
from core import SceneManager, Scene
from config import *
from systems import PokerSystem, PokerRenderer, PokerPlayer, Player

# Poker Class
class Poker(Scene):
    def __init__(self, scene_manager: SceneManager, player: Player) -> None:
        self.scene_manager = scene_manager
        self.player = player

        self.poker_system = PokerSystem(
            self.player,
            PokerPlayer()
        )

    def start(self) -> None:
        self.poker_system.start()

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == MOUSEMOTION:
            self.poker_system.handle_motion(event)

    def update(self, delta_time: float) -> None:
        self.poker_system.update(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        self.poker_system.draw(surface)