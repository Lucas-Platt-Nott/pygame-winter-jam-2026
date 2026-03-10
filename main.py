# Built-In
import asyncio

# External
import pygame
from pygame.locals import *

# Internal
from core import Application
from config import SCREEN_SIZE
from scenes import *
from systems import Player

# Frozen Funds Class
class FrozenFunds(Application):
    def __init__(self, screen_size: tuple[int, int], flags: int = 0, fps: int = 0):
        super().__init__(screen_size, flags, fps)
        self.player = Player()

    def add_scene(self, scene_type: type, scene_key: str) -> None:
        scene = scene_type(self.scene_manager, self.player)
        self.scene_manager.register_scene(scene, scene_key)

if __name__ == "__main__":
    # Initialise mixer
    pygame.mixer.init()

    # Initialise game
    application = FrozenFunds(SCREEN_SIZE)

    application.add_scene(Poker, "poker")
    application.add_scene(Title, "title")
    application.set_scene("poker")

    asyncio.run(application.start())