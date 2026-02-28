# External
import pygame
from pygame.locals import *

# Internal
from assets import Images
from core import Scene

# Title Scene Class
class TitleScene(Scene):
    def __init__(self):
        self.background = Images.get_image("placeholder_background")
        self.title = Images.get_image("title")

    def start(self) -> None:
        pass

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == KEYDOWN:
                pass

    def update(self, delta_time: float) -> None:
        pass

    def draw(self, surface: pygame.surface.Surface) -> None:
        # surface.blit(self.background, (0, 0))
        surface.blit(self.title, (0, 0))

    def stop(self) -> None:
        pass