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

        self.system = PokerSystem(self.player, PokerPlayer())
        self.renderer = PokerRenderer()

    def start(self) -> None:
        self.player.reset()
        self.system = PokerSystem(self.player, PokerPlayer())

    def handle_event(self, event: pygame.Event) -> None:
        self.system.handle_event(event)

    def update(self, delta_time: float) -> None:
        self.system.update(delta_time)
        self.renderer.update(delta_time, self.system)

    def draw(self, surface: pygame.Surface) -> None:
        self.renderer.draw(surface, self.system)