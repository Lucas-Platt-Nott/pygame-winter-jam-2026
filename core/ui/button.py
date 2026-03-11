# External
import pygame

class Button:
    def __init__(self, surface: pygame.Surface, position: pygame.Vector2, on_click, *args):
        self.image = surface
        self.position = position
        self.on_click = on_click
        self.args = args

    def clicked(self) -> None:
        # self.on_click(*self.args)
        pass

    def set_alpha(self, alpha: int) -> None:
        self.image.set_alpha(alpha)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.position)