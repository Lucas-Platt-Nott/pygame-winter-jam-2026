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

        # Vertical placement (row center based on base card size)
        self.y = SCREEN_SIZE[1] // 2 - CARD_SIZE[1] // 2

    def _compute_target(self, index: int):
        """Return the CENTER position for the given slot index."""
        total_slots = 5
        spacing = CARD_SIZE[0] * 1.1

        total_width = spacing * (total_slots - 1) + CARD_SIZE[0]
        start_x = (self.surface.get_width() - total_width) / 2

        center_x = start_x + index * spacing + CARD_SIZE[0] / 2
        center_y = self.y + CARD_SIZE[1] / 2

        return (center_x, center_y)

    def add(self, card: Card):
        if card == None:
            return
        
        if len(self.cards) >= 5:
            return  # Can't exceed 5 community cards

        index = len(self.cards)
        self.cards.append(card)

        target_pos = self._compute_target(index)

        # Start animation from center of screen (slightly above), using center coords
        start_pos = (
            self.surface.get_width() // 2,
            self.y - 80 + CARD_SIZE[1] // 2,
        )

        self.anim_data[card] = {
            "progress": 0.0,
            "start_pos": start_pos,
            "target_pos": target_pos,
        }

    def render_surface(self, delta_time: float):
        self.surface.fill((0, 0, 0, 0))

        # First: always draw 5 empty slots (these can stay based on CARD_SIZE)
        for i in range(5):
            cx, cy = self._compute_target(i)
            surf = Images.get_image("borderless_card")

            draw_x = cx - surf.get_width() // 2
            draw_y = cy - surf.get_height() // 2
            self.surface.blit(surf, (draw_x, draw_y))

        # Then: draw actual cards (animated or placed) on top
        for i, card in enumerate(self.cards):
            if i >= 5:
                break

            anim = self.anim_data.get(card)

            if anim is None:
                # No animation data, just draw at its target center
                cx, cy = self._compute_target(i)
                card.x = cx
                card.y = cy

                surf = card.render()
                draw_x = card.x - surf.get_width() // 2
                draw_y = card.y - surf.get_height() // 2
                self.surface.blit(surf, (draw_x, draw_y))
                continue

            # Update animation
            anim["progress"] = min(1.0, anim["progress"] + delta_time * ANIM_SPEED)
            t = ease_in_out(anim["progress"])

            start_x, start_y = anim["start_pos"]
            target_x, target_y = anim["target_pos"]

            cx = lerp(start_x, target_x, t)
            cy = lerp(start_y, target_y, t)

            card.x = cx
            card.y = cy

            surf = card.render()
            draw_x = card.x - surf.get_width() // 2
            draw_y = card.y - surf.get_height() // 2
            self.surface.blit(surf, (draw_x, draw_y))

            # When finished, snap to target center
            if anim["progress"] >= 1.0:
                card.x = target_x
                card.y = target_y

    def update(self, delta_time: float):
        for card in self.cards:
            card.update(delta_time)
            
        self.render_surface(delta_time)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, (0, 0))
