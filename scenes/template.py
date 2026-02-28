# External
import pygame

# Internal
from core import Scene

# Template Scene Class
class TemplateScene(Scene):
    def start(self) -> None:
        pass

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def draw(self, surface: pygame.surface.Surface) -> None:
        pass

    def stop(self) -> None:
        pass