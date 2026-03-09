# External
import pygame

# Internal
from assets import Images

class Card:
    def __init__(self, card_type: str, card_suit: str, card_rank: str) -> None:
        self.type = card_type
        self.suit = card_suit
        self.rank = card_rank

        self._base_surface = None
        self._rotation_cache = {}

        self.x = 0
        self.y = 0
        self.angle = 0
        self.scale = 1.0
        self.alpha = 255

        self.selected = False
        self.anim = None

    @property
    def name(self) -> str:
        return f"{self.type}_{self.suit}_{self.rank}"

    def _get_base_surface(self):
        if self._base_surface is None:
            self._base_surface = Images.get_image(self.name)
        return self._base_surface

    def get_rotated(self, angle: int):
        angle = int(angle) % 360
        if angle not in self._rotation_cache:
            self._rotation_cache[angle] = pygame.transform.rotate(
                self._get_base_surface(), angle
            )
        return self._rotation_cache[angle]

    def render(self) -> pygame.Surface:
        surf = self.get_rotated(self.angle)

        if self.scale != 1.0:
            w = int(surf.get_width() * self.scale)
            h = int(surf.get_height() * self.scale)
            surf = pygame.transform.smoothscale(surf, (w, h))

        if self.alpha != 255:
            surf = surf.copy()
            surf.set_alpha(self.alpha)

        return surf
