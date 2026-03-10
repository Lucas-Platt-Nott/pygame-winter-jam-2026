# Built-In
import random

# External
import pygame
from pygame.locals import *

# Internal
from assets import Images, Sounds
from core import SceneManager, Scene, Button
from config import *

class Title(Scene):
    def __init__(self, scene_manager: SceneManager, player) -> None:
        self.scene_manager = scene_manager
        self.cards: list[AnimatedCard] = []

        self.width = SCREEN_SIZE[0] / 2
        self.intro_time_elapsed = 0
        self.alpha = 0

        self.title_image = Images.get_image("title")
        self.title_w = self.title_image.width
        self.title_h = self.title_image.height
        self.title_position = (
            (SCREEN_SIZE[0] - self.title_w) / 2,
            SCREEN_SIZE[1] / 2 - self.title_h / 2
        )

        self.time_elapsed = 0
        self.interval = 1/100

        self.screen_w, self.screen_h = SCREEN_SIZE
        self.card_w, self.card_h = CARD_SIZE

        self.base_background = Images.get_image("poker-background")
        
    def start(self):
        self.intro_time_elapsed = 0
        self.cards.clear()

        Sounds.get_sound("title-background").play(-1, -1, 500)

        for card_type in TYPES:
            if card_type not in ["frozen"]:
                continue

            for suit in SUITS:
                for rank in RANKS:
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
                            random.randint(0, self.screen_h - self.card_h // 2)
                        ),
                        tint
                    )
                    self.cards.append(card)

        self.cards.sort(key=lambda card: card.tint)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == MOUSEMOTION:
            mouse_pos = pygame.Vector2(event.pos)
            for card in self.cards:
                card.handle_motion(mouse_pos)

    def update(self, delta_time: float) -> None:
        self.intro_time_elapsed += delta_time

        if self.intro_time_elapsed < 1.5:
            self.alpha = 255 * (self.intro_time_elapsed / 1.5)
            self.title_image.set_alpha(self.alpha)

        elif 2.5 < self.intro_time_elapsed < 3.5:
            t = (self.intro_time_elapsed - 2.5)
            offset = (self.screen_h / 2 - self.title_h / 2) * 0.8 * t
            self.title_position = (
                (self.screen_w - self.title_w) / 2,
                (self.screen_h / 2 - self.title_h / 2) - offset
            )

        self.time_elapsed += delta_time
        if self.time_elapsed >= self.interval:
            for card in self.cards:
                card.update(self.interval)
            self.time_elapsed = 0

        return super().update(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        credits = Images.get_image("credits")
        title_background = self.base_background.copy()

        for card in self.cards:
            card.draw(title_background)

        surface.blit(title_background)
        surface.blit(credits, (SCREEN_SIZE[0] / 2 - credits.width / 2, 0))
        surface.blit(self.title_image, self.title_position)

    def stop(self):
        self.cards.clear()


class AnimatedCard:
    def __init__(self, surface: pygame.Surface, center: pygame.Vector2, tint: int) -> None:
        self.image = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.center = center
        self.tint = tint

        self.is_active = False
        self.velocity = pygame.Vector2()
        self.old_velocity = pygame.Vector2()

        self.separation_magnitude = 5
        self.collide_radius = 100
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

            # Smooth falloff (keeps original feel but removes choppy flip)
            strength = (self.collide_radius - dist_mag)
            strength *= 0.8  # soften the force slightly

            push = direction * strength * self.separation_magnitude

            self.velocity = (push + self.old_velocity) / 2

    def update(self, delta_time: float) -> None:
        self.center.y += self.falling_speed * delta_time

        if self.center.y - self.height / 2 > SCREEN_SIZE[1]:
            self.center.x = random.randint(0, SCREEN_SIZE[0] - self.width // 2)
            self.center.y = -self.height / 2

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
