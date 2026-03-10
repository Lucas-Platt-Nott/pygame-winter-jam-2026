# Built-In
import math
import random

# External
import pygame
from pygame.locals import *

# Internal
from config import *
from systems import Card
from assets import Images


def cubic_bezier(t, p0, p1, p2, p3):
    u = 1 - t
    return (
        u*u*u*p0 +
        3*u*u*t*p1 +
        3*u*t*t*p2 +
        t*t*t*p3
    )

def ease_in_out(t):
    return cubic_bezier(t, 0.0, 0.25, 0.75, 1.0)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_angle(a, b, t):
    diff = (b - a + 180) % 360 - 180
    return a + diff * t


class Hand:
    def __init__(self, position=(0, 0), hidden=False, flip=False) -> None:
        self._cards: list[Card] = []
        self.surface = pygame.Surface((SCREEN_SIZE[0], CARD_SIZE[1] * 2), SRCALPHA)
        self.anim_data = {}
        self.hitboxes = []
        self.position = position

        self.flip = flip
        self.is_hidden = hidden
        self.baseline_y = 60

        self.arc_radius = 350
        self.arc_center = (
            self.surface.get_width() // 2,
            self.baseline_y + CARD_SIZE[1] + 150
        )

        # Cards currently animating out
        self.discarding = []

    @property
    def cards(self) -> list[Card]:
        return self._cards

    @property
    def num_cards(self) -> int:
        count = 0
        for card in self.cards:
            if card.type != "frozen":
                count += 1
        return count

    def _compute_target(self, index: int, hand_size: int):
        if hand_size <= 0:
            return (0, self.baseline_y), 0

        center = (hand_size - 1) / 2
        step = (2 * MAX_ANGLE) / max(hand_size - 1, 1)
        angle = int((index - center) * step)

        spacing = CARD_SIZE[0] * 0.8
        hand_width = spacing * (hand_size - 1) + CARD_SIZE[0]
        start_x = (self.surface.get_width() - hand_width) / 2

        pos = (
            start_x + index * spacing,
            self.baseline_y + 2 * abs(angle)
        )
        return pos, angle

    def get_selected_cards(self):
        return [card for card in self._cards if card.selected]

    def select(self, index: int) -> None:
        if 0 <= index < len(self._cards):
            card = self._cards[index]
            anim = self.anim_data[card]

            current_offset = anim.get("current_select_offset", 0.0)
            card.selected = not card.selected
            target_offset = -25 if card.selected else 0

            anim["select_progress"] = 0.0
            anim["select_start_offset"] = current_offset
            anim["select_target_offset"] = target_offset

    def select_random(self) -> None:
        while True:
            index = random.randint(0, len(self.cards) - 1)
            if self.cards[index].type != "frozen" and not self.cards[index].selected:
                break

        self.select(index)

    def handle_click(self, event: pygame.Event) -> None:
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        mx, my = event.pos
        local_x = mx - self.position[0]
        local_y = my - self.position[1]

        if self.flip:
            local_x = self.surface.get_width() - local_x
            local_y = self.surface.get_height() - local_y

        for i, rect in enumerate(self.hitboxes):
            if rect.collidepoint(local_x, local_y):
                self.select(i)
                break

    def add(self, card: Card) -> None:
        index = len(self._cards)
        self._cards.append(card)

        target_pos, target_angle = self._compute_target(index, len(self._cards))

        self.anim_data[card] = {
            "mode": "arc",
            "start_theta": math.radians(0),
            "end_theta": math.radians(-target_angle),
            "start_angle": 45,
            "progress": 0.0,
            "start_pos": target_pos,
            "current_angle": 45,
            "last_base_pos": target_pos,

            # selection animation
            "select_progress": 1.0,
            "select_start_offset": 0.0,
            "select_target_offset": 0.0,
            "current_select_offset": 0.0,
        }

        for i, c in enumerate(self._cards):
            if c == card:
                continue

            target_pos, target_angle = self._compute_target(i, len(self._cards))
            anim = self.anim_data[c]
            anim["start_pos"] = anim.get("last_base_pos", target_pos)
            anim["start_angle"] = anim.get("current_angle", -target_angle)
            anim["progress"] = 0.0
            anim["mode"] = "lerp"

    def render_surface(self, delta_time: float) -> None:
        self.surface.fill((0, 0, 0, 0))
        self.hitboxes = []

        # Draw discarding cards (fade only, no movement)
        for card in list(self.discarding):
            anim = self.anim_data.get(card)
            if not anim:
                continue

            anim["progress"] = min(1.0, anim["progress"] + delta_time * 1.8)
            t = ease_in_out(anim["progress"])

            base_x, base_y = anim["discard_start_pos"]
            angle = lerp_angle(anim["discard_start_angle"], anim["discard_end_angle"], t)

            surf = card.render().copy()
            surf = pygame.transform.rotate(surf, angle)

            fade_t = min(1.0, t * 2.2)
            alpha = int(255 * (1 - fade_t))
            surf.set_alpha(alpha)

            self.surface.blit(surf, (base_x, base_y))

            if anim["progress"] >= 1.0:
                self.discarding.remove(card)
                self.anim_data.pop(card, None)

        if not self._cards:
            return

        total = len(self._cards)

        # Draw normal cards
        for index, card in enumerate(self._cards):
            target_pos, target_angle = self._compute_target(index, len(self._cards))
            anim = self.anim_data[card]

            anim["progress"] = min(1.0, anim["progress"] + delta_time * ANIM_SPEED)
            t = ease_in_out(anim["progress"])

            if anim["mode"] == "arc":
                theta = lerp(anim["start_theta"], anim["end_theta"], t)
                arc_x = self.arc_center[0] + math.cos(theta) * self.arc_radius
                arc_y = self.arc_center[1] + math.sin(theta) * self.arc_radius
                base_x = lerp(arc_x, target_pos[0], t)
                base_y = lerp(arc_y, target_pos[1], t)
            else:
                base_x = lerp(anim["start_pos"][0], target_pos[0], t)
                base_y = lerp(anim["start_pos"][1], target_pos[1], t)

            angle = lerp_angle(anim["start_angle"], -target_angle, t)

            # Selection animation
            anim["select_progress"] = min(1.0, anim["select_progress"] + delta_time * 4.0)
            s_t = ease_in_out(anim["select_progress"])
            offset = lerp(anim["select_start_offset"], anim["select_target_offset"], s_t)
            anim["current_select_offset"] = offset

            card.x = base_x
            card.y = base_y + offset
            card.angle = angle

            # Draw card normally
            surf = Images.get_image("card_back") if self.is_hidden else card.render()
            self.surface.blit(surf, (card.x, card.y))

            # --- FIXED TINT USING BLEND_RGB_MULT ---
            depth = (total - 1) - index  # 0 = topmost
            if depth > 0:
                # Lerp tint between 255 (no tint) and ~215 (slightly darker)
                tint_value = int(lerp(255, 215, min(1.0, depth * 0.25)))

                tint = pygame.Surface(surf.get_size(), SRCALPHA)
                tint.fill((tint_value, tint_value, tint_value))

                self.surface.blit(
                    tint,
                    (card.x, card.y),
                    special_flags=pygame.BLEND_RGB_MULT
                )

            rect = pygame.Rect(card.x, card.y, surf.get_width(), surf.get_height())
            self.hitboxes.append(rect)

            anim["current_angle"] = angle
            anim["last_base_pos"] = (base_x, base_y)
            anim["last_draw_pos"] = (card.x, card.y)

    def discard_selected(self) -> None:
        for card in self.get_selected_cards():
            self.remove(card)

        # Reflow remaining cards
        for i, c in enumerate(self._cards):
            anim = self.anim_data[c]
            target_pos, target_angle = self._compute_target(i, len(self._cards))
            anim["start_pos"] = anim["last_base_pos"]
            anim["start_angle"] = anim["current_angle"]
            anim["progress"] = 0.0
            anim["mode"] = "lerp"

    def remove(self, card: Card) -> None:
        if card not in self._cards:
            return

        self._cards.remove(card)

        anim = self.anim_data.get(card)
        if not anim:
            return

        anim["mode"] = "discard"
        anim["progress"] = 0.0

        discard_pos = anim.get("last_draw_pos", anim.get("last_base_pos", (card.x, card.y)))
        anim["discard_start_pos"] = discard_pos
        anim["discard_start_angle"] = anim["current_angle"]
        anim["discard_end_angle"] = anim["current_angle"] + random.randint(60, 140)

        self.discarding.append(card)

    def update(self, delta_time: float) -> None:
        self.render_surface(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        if self.flip:
            flipped = pygame.transform.rotate(self.surface, 180)
            surface.blit(flipped, self.position)
        else:
            surface.blit(self.surface, self.position)
