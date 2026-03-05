# Built-In
import asyncio

# External
import pygame

# Internal
from core import Game
from config import SCREEN_SIZE
from scenes import *

if __name__ == "__main__":
    # Initialise mixer
    pygame.mixer.init()

    # Initialise game
    game = Game(SCREEN_SIZE)

    game.add_scene(Title, "title")
    game.set_scene("title")

    asyncio.run(game.start())