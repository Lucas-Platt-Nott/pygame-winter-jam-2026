# Built-In
import asyncio

# External
import pygame
from pygame.locals import *

# Internal
from assets import *
from core import Application
from config import *
from scenes import *
from systems import Player

# Frozen Funds Class
class FrozenFunds(Application):
    def __init__(self, screen_size: tuple[int, int], flags: int = 0, fps: int = 0):
        super().__init__(screen_size, flags, fps)
        self.player = Player()

        self.background = Images.get_image("poker_background")
        self.rotated = self.background.copy()
        self.rotate_interval = 0.06
        self.angle = 0
        self.angle_step = 0.1
        self.time_elapsed = 0

        pygame.display.set_icon(Images.get_image("chip"))
    
    def add_scene(self, scene_type: type, scene_key: str) -> None:
        scene = scene_type(self.scene_manager, self.player)
        self.scene_manager.register_scene(scene, scene_key)

    def update(self, delta_time):
        pygame.display.set_caption(f"Frozen Funds - FPS : {int(self.clock.get_fps())}")
        self.time_elapsed += delta_time

        if self.time_elapsed >= self.rotate_interval:
            self.time_elapsed = 0
            self.angle += self.angle_step
            self.rotated = pygame.transform.rotate(self.background, self.angle)

        return super().update(delta_time)
    
    def draw(self):
        self.screen.fill((0, 255, 0))
        rect = self.rotated.get_frect()
        rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)

        self.screen.blit(self.rotated, rect)
        self.scene_manager.draw(self.screen)

        pygame.display.flip()

if __name__ == "__main__":
    # Initialise mixer
    pygame.mixer.init()

    # Initialise game
    application = FrozenFunds(SCREEN_SIZE, fps=0)

    application.add_scene(Victory, "victory")
    application.add_scene(Poker, "poker")
    application.add_scene(Title, "title")
    application.set_scene("title")

    # Run application
    asyncio.run(application.start())