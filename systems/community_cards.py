# External
import pygame
from pygame.locals import *

# Internal
from assets import Images
from config import *
from systems import Card
from systems.hand import ease_in_out, lerp, ANIM_SPEED

class CommunityCards:
    def __init__(self):
        self.cards: list[Card] = []
        self.anim_data = {}

        # Render surface (same width as screen, full height)
        self.surface = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]), SRCALPHA)

        # Vertical placement
        self.y = SCREEN_SIZE[1] // 2 - CARD_SIZE[1] // 2

    def _compute_target(self, index: int):
        total_slots = 5
        spacing = CARD_SIZE[0] * 1.1

        total_width = spacing * (total_slots - 1) + CARD_SIZE[0]
        start_x = (self.surface.get_width() - total_width) / 2

        x = start_x + index * spacing
        return (x, self.y)

    def add(self, card: Card):
        if len(self.cards) >= 5:
            return  # Can't exceed 5 community cards

        index = len(self.cards)
        self.cards.append(card)

        target_pos = self._compute_target(index)

        # Start animation from center of screen (slightly above)
        start_pos = (self.surface.get_width() // 2, self.y - 80)

        self.anim_data[card] = {
            "progress": 0.0,
            "start_pos": start_pos,
            "target_pos": target_pos,
        }

    def render_surface(self, delta_time: float):
        self.surface.fill((0, 0, 0, 0))

        # First: always draw 5 empty slots
        for i in range(5):
            x, y = self._compute_target(i)
            surf = Images.get_image("borderless_card")
            self.surface.blit(surf, (x, y))

        # Then: draw actual cards (animated or placed) on top
        for i, card in enumerate(self.cards):
            if i >= 5:
                break

            anim = self.anim_data.get(card)
            if anim is None:
                # No animation data, just draw at its target slot
                x, y = self._compute_target(i)
                card.x = x
                card.y = y
                surf = card.render()
                self.surface.blit(surf, (x, y))
                continue

            # Update animation
            anim["progress"] = min(1.0, anim["progress"] + delta_time * ANIM_SPEED)
            t = ease_in_out(anim["progress"])

            start_x, start_y = anim["start_pos"]
            target_x, target_y = anim["target_pos"]

            x = lerp(start_x, target_x, t)
            y = lerp(start_y, target_y, t)

            card.x = x
            card.y = y

            surf = card.render()
            self.surface.blit(surf, (x, y))

            # When finished, snap to target and keep data for reuse if needed
            if anim["progress"] >= 1.0:
                card.x = target_x
                card.y = target_y

    def update(self, delta_time: float):
        self.render_surface(delta_time)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, (0, 0))
