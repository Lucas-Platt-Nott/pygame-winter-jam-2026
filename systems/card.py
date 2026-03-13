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
        self.highlighted = False
        self.anim = None

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

    def render(self) -> pygame.Surface:
        surf = self.get_rotated(self.angle)

        # Apply scaling
        if self.scale != 1.0:
            w = int(surf.get_width() * self.scale)
            h = int(surf.get_height() * self.scale)
            surf = pygame.transform.smoothscale(surf, (w, h))

        # Apply alpha
        if self.alpha != 255:
            surf = surf.copy()
            surf.set_alpha(self.alpha)

        # --- MASK-BASED OUTLINE ---
        if self.highlighted:
            # Create mask from the card surface
            mask = pygame.mask.from_surface(surf)

            # Outline thickness
            thickness = 4
            color = (80, 180, 255)  # bright light blue

            # Create a new surface for the outline
            outline_surf = pygame.Surface(
                (surf.get_width() + thickness * 2, surf.get_height() + thickness * 2),
                pygame.SRCALPHA
            )

            # Draw outline by offsetting the mask in multiple directions
            for dx in range(-thickness, thickness + 1):
                for dy in range(-thickness, thickness + 1):
                    if dx * dx + dy * dy <= thickness * thickness:
                        outline_surf.blit(mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0)), (dx + thickness, dy + thickness))

            # Blit the card on top of the outline
            outline_surf.blit(surf, (thickness, thickness))
            surf = outline_surf

        return surf
