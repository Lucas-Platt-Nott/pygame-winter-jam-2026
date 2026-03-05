# External
import pygame

class Button:
    def __init__(self, surface: pygame.Surface, position: pygame.Vector2):
        self.image = surface
        self.position = position

    def set_alpha(self, alpha: int) -> None:
        self.image.set_alpha(alpha)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.position)