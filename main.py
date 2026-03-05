# Built-In
import asyncio

# Internal
from core import Game
from config import SCREEN_SIZE
from scenes import *

if __name__ == "__main__":
    game = Game(SCREEN_SIZE)

    # Load scenes
    game.add_scene(Title, "title")

    # Set scene
    game.set_scene("title")

    asyncio.run(game.start())