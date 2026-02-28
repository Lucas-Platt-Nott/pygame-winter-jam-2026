# Built-ins
from abc import ABC, abstractmethod

# External
import pygame

# Scene class
class Scene(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.surface.Surface) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass