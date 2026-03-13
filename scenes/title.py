# Built-In
import random
import math

# External
import pygame
from pygame.locals import *

# Internal
from assets import Images, Sounds
from core import SceneManager, Scene, Button
from config import *


class AnimatedCard:
    def __init__(self, surface: pygame.Surface, center: pygame.Vector2, tint: int) -> None:
        self.image = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.center = center
        self.tint = tint

        self.clear = False
        self.is_active = False
        self.velocity = pygame.Vector2()
        self.old_velocity = pygame.Vector2()

        # Tweaked responsiveness
        self.separation_magnitude = 3.5   # was 5
        self.collide_radius = 90          # was 100
        self.friction = 6
        self.falling_speed = 150

        self.half_size = pygame.Vector2(self.width / 2, self.height / 2)

    def handle_motion(self, mouse_pos: pygame.Vector2) -> None:
        distance = self.center - mouse_pos
        dist_mag = distance.length()

        if dist_mag < self.collide_radius:

            # Dead zone to prevent jitter when mouse crosses centre
            if dist_mag < 10:
                return

            self.is_active = True
            self.old_velocity = self.velocity

            # Safe normalize
            direction = distance / dist_mag

            # Softer falloff
            strength = (self.collide_radius - dist_mag)
            strength *= 0.55  # was 0.8

            push = direction * strength * self.separation_magnitude

            # Smoother blending (less snappy)
            self.velocity = (push + self.old_velocity * 4) / 5

    def update(self, delta_time: float) -> None:
        self.center.y += self.falling_speed * delta_time

        if self.center.y - self.height / 2 > SCREEN_SIZE[1]:
            self.clear = True

        if self.center.x < -self.width:
            self.center.x = SCREEN_SIZE[0] + self.width / 2
        elif self.center.x > SCREEN_SIZE[0] + self.width:
            self.center.x = -self.width / 2

        if not self.is_active:
            return

        vel_mag = self.velocity.length()

        if vel_mag > 2:
            self.velocity -= (self.friction * 9.8 * delta_time) * (self.velocity / vel_mag)
        else:
            self.is_active = False
            self.velocity.update(0, 0)

        self.center += self.velocity * delta_time

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.center - self.half_size)


class Title(Scene):
    def __init__(self, scene_manager: SceneManager, player) -> None:
        self.scene_manager = scene_manager
        self.cards: list[AnimatedCard] = []

        self.width = SCREEN_SIZE[0] / 2
        self.intro_time_elapsed = 0
        self.alpha = 0
        self.original_prompt = Images.get_image("title_prompt")
        self.prompt = Images.get_image("title_prompt")
        self.title_image = Images.get_image("title")
        self.title_w = self.title_image.width
        self.title_h = self.title_image.height
        self.title_position = (
            (SCREEN_SIZE[0] - self.title_w) / 2,
            SCREEN_SIZE[1] / 2 - self.title_h / 2
        )

        self.time_elapsed = 0
        self.animation_time = 0
        self.interval = 0

        self.screen_w, self.screen_h = SCREEN_SIZE
        self.card_w, self.card_h = CARD_SIZE

        self.exiting = False
        self.exit_progress = 0.0
        self.exit_duration = 1.0

    def kill_offscreen_cards(self):
        self.cards = [
            c for c in self.cards
            if -c.height < c.center.y < SCREEN_SIZE[1] + c.height
        ]

    def start(self):
        self.intro_time_elapsed = 0
        self.cards.clear()

        Sounds.get_sound("title_music").play(-1, -1, 500)

        for i in range(52):
            self.spawn_card()

    def spawn_card(self):
        if self.exiting:
            return

        card_type = random.choice(TYPES)
        suit = random.choice(SUITS)
        rank = random.choice(RANKS)
        tint = random.randint(80, 140)

        card_image = pygame.transform.rotate(
            Images.get_image(f"{card_type}_{suit}_{rank}"),
            random.randint(0, 180)
        )
        card_image.fill((tint, tint, tint), special_flags=BLEND_RGB_MULT)

        card = AnimatedCard(
            card_image,
            pygame.Vector2(
                random.randint(0, self.screen_w - self.card_w // 2),
                random.randint(-self.screen_h, self.screen_h)
            ),
            tint
        )
        card.fade_alpha = 255
        self.cards.append(card)
        self.cards.sort(key=lambda card: card.tint)

    def new_card(self):
        if self.exiting:
            return

        card_type = random.choice(TYPES)
        suit = random.choice(SUITS)
        rank = random.choice(RANKS)
        tint = random.randint(80, 140)

        card_image = pygame.transform.rotate(
            Images.get_image(f"{card_type}_{suit}_{rank}"),
            random.randint(0, 180)
        )
        card_image.fill((tint, tint, tint), special_flags=BLEND_RGB_MULT)

        card = AnimatedCard(
            card_image,
            pygame.Vector2(
                random.randint(0, self.screen_w - self.card_w // 2),
                random.randint(-self.screen_h, -self.card_h // 2)
            ),
            tint
        )
        card.fade_alpha = 255
        self.cards.append(card)
        self.cards.sort(key=lambda card: card.tint)

    def handle_event(self, event: pygame.Event) -> None:
        if self.exiting:
            return

        if event.type == MOUSEMOTION:
            mouse_pos = pygame.Vector2(event.pos)
            for card in self.cards:
                card.handle_motion(mouse_pos)

        elif event.type == KEYDOWN:
            if event.dict["key"] == K_RETURN:
                self.exiting = True
                self.exit_progress = 0.0
                self.kill_offscreen_cards()

    def update(self, delta_time: float) -> None:
        if self.exiting:
            self.exit_progress += delta_time / self.exit_duration
            t = min(self.exit_progress, 1.0)

            self.title_position = (
                self.title_position[0],
                (SCREEN_SIZE[1] / 2 - self.title_h / 2) - t * SCREEN_SIZE[1]
            )

            prompt_y = SCREEN_SIZE[1] * 0.9 - self.prompt.height + t * SCREEN_SIZE[1]
            self.prompt_pos = (
                SCREEN_SIZE[0] / 2 - self.prompt.width / 2,
                prompt_y
            )

            for card in self.cards:
                card.update(delta_time)

                # Fade out
                card.fade_alpha -= 300 * delta_time
                if card.fade_alpha < 0:
                    card.fade_alpha = 0
                card.image.set_alpha(int(card.fade_alpha))

            self.cards = [
                c for c in self.cards
                if not c.clear and c.fade_alpha > 0
            ]

            title_off = self.title_position[1] + self.title_h < 0
            prompt_off = self.prompt_pos[1] > SCREEN_SIZE[1]
            cards_off = len(self.cards) == 0

            if title_off and prompt_off and cards_off:
                self.scene_manager.set_scene("poker")

            return

        self.intro_time_elapsed += delta_time

        if self.intro_time_elapsed < 1.5:
            self.alpha = 255 * (self.intro_time_elapsed / 1.5)
            self.title_image.set_alpha(self.alpha)

        # elif 2.5 < self.intro_time_elapsed < 3.5:
        #     t = (self.intro_time_elapsed - 2.5)
        #     offset = (self.screen_h / 2 - self.title_h / 2) * 0.8 * t
        #     self.title_position = (
        #         (self.screen_w - self.title_w) / 2,
        #         (self.screen_h / 2 - self.title_h / 2) - offset
        #     )

        self.time_elapsed += delta_time
        self.animation_time += delta_time
        hue = (455 / 2) + (55 / 2) * math.cos(5 * self.animation_time)
        self.prompt = self.original_prompt.copy()
        self.prompt.fill((hue, hue, hue), special_flags=BLEND_RGB_MULT)

        self.prompt_pos = (
            SCREEN_SIZE[0] / 2 - self.prompt.width / 2,
            SCREEN_SIZE[1] * 0.9 - self.prompt.height
        )

        if self.time_elapsed >= self.interval:
            for card in self.cards:
                card.update(self.time_elapsed)

                if card.clear:
                    self.cards.remove(card)
                    self.new_card()

            self.time_elapsed = 0

        return super().update(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        credits = Images.get_image("credits")

        for card in self.cards:
            card.draw(surface)

        surface.blit(credits, (SCREEN_SIZE[0] / 2 - credits.width / 2, 0))
        surface.blit(self.prompt, self.prompt_pos)
        surface.blit(self.title_image, self.title_position)

    def stop(self):
        self.cards.clear()
        Sounds.get_sound("title_music").fadeout(500)
