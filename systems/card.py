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
        self.highlighted = False
        self.anim = None

        # Highlight animation state
        self.highlight_thickness = 0.0
        self.max_highlight_thickness = 6
        self.highlight_speed = 12.0

    @property
    def name(self) -> str:
        return f"{self.type}_{self.suit}_{self.rank}"

    def update_image(self) -> None:
        self._rotation_cache = {}
        self._base_surface = None

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

    def update(self, dt: float):
        target = self.max_highlight_thickness if self.highlighted else 0.0
        self.highlight_thickness += (target - self.highlight_thickness) * self.highlight_speed * dt
        if abs(self.highlight_thickness) < 0.01:
            self.highlight_thickness = 0.0

    def render(self) -> pygame.Surface:
        surf = self.get_rotated(self.angle)

        if self.scale != 1.0:
            w = int(surf.get_width() * self.scale)
            h = int(surf.get_height() * self.scale)
            surf = pygame.transform.smoothscale(surf, (w, h))

        if self.alpha != 255:
            surf = surf.copy()
            surf.set_alpha(self.alpha)

        thickness = int(self.highlight_thickness)

        if thickness > 0:
            mask = pygame.mask.from_surface(surf)

            if self.type == "frozen":
                color = (80, 180, 255)

            elif self.suit in ["hearts", "diamonds"]:
                color = (255, 0, 80)

            else:
                color = (10, 10, 10)

            outline_surf = pygame.Surface(
                (surf.get_width() + thickness * 2, surf.get_height() + thickness * 2),
                pygame.SRCALPHA
            )

            mask_surf = mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))

            for dx in range(-thickness, thickness + 1):
                for dy in range(-thickness, thickness + 1):
                    if dx * dx + dy * dy <= thickness * thickness:
                        outline_surf.blit(mask_surf, (dx + thickness, dy + thickness))

            outline_surf.blit(surf, (thickness, thickness))
            surf = outline_surf

        return surf
