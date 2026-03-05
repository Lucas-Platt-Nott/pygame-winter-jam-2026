# Built-In
import random

# External
import pygame
from pygame.locals import *

# Internal
from assets import Images
from core import SceneManager, Scene
from config import *

# Title Scene
class Title(Scene):
    def __init__(self, scene_manager: SceneManager) -> None:
        self.scene_manager = scene_manager
        self.cards: list[AnimatedCard] = []
        self.width = SCREEN_SIZE[0] / 2
        self.time_elapsed = 0
        self.interval = 1/60

        for card_type in TYPES:
            for suit in SUITS:
                for rank in RANKS:
                    card = AnimatedCard(
                        pygame.transform.rotate(Images.get_image(f"{card_type}_card"), random.randint(0, 180)),
                        pygame.Vector2(
                            random.randint(0, 1024 - CARD_SIZE[0] // 2),
                            random.randint(0, 576 - CARD_SIZE[1] // 2)
                        )
                    )
            
                    self.cards.append(card)

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == MOUSEMOTION and not pygame.mouse.get_pressed()[0]:
            for card in self.cards:
                card.handle_motion(event)

    def update(self, delta_time: float) -> None:
        self.time_elapsed += delta_time

        if self.time_elapsed >= self.interval:
            for card in self.cards:
                card.update(self.time_elapsed)

            self.time_elapsed = 0

        return super().update(delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        title_background = Images.get_image("title-background").copy()
        title_image = Images.get_image("title")

        for card in self.cards:
            card.draw(title_background)

        # pygame.transform.box_blur(title_background, 2, dest_surface=surface)
        surface.blit(title_background)
        surface.blit(title_image, ((SCREEN_SIZE[0] - title_image.width) / 2, SCREEN_SIZE[1] / 2 - title_image.height / 2))

class AnimatedCard:
    def __init__(self, surface: pygame.Surface, center: pygame.Vector2) -> None:
        self.image = surface
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.center = center
        
        # Simulation
        self.is_active = False

        self.old_velocity = pygame.Vector2()
        self.velocity = pygame.Vector2()

        self.separation_magnitude = 2.5
        self.collide_radius = 100
        self.friction = 5
        self.falling_speed = 100

    def handle_motion(self, event: pygame.Event) -> None:
        mouse_pos = pygame.Vector2(event.dict["pos"])
        distance = self.center - mouse_pos

        if distance.magnitude() < self.collide_radius:
            self.is_active = True
            self.old_velocity = self.velocity
            self.velocity = ((distance.normalize() * (self.collide_radius - distance.magnitude())) * self.separation_magnitude + self.old_velocity) / 2
            
    def update(self, delta_time: float) -> None:
        self.center.y += self.falling_speed * delta_time
        if self.center.y - self.height / 2 > SCREEN_SIZE[1]:
            self.center = pygame.Vector2(
                    random.randint(0, 1024 - self.width // 2),
                    -self.height // 2
                )
        
        if self.center.x - self.width / 2 < -self.width:
            self.center.x = SCREEN_SIZE[0] + self.width / 2

        elif self.center.x - self.width / 2 > SCREEN_SIZE[0] + self.width / 2:
            self.center.x = -self.width / 2

        if not self.is_active:
            return
        
        if self.velocity.magnitude() > 2:
            self.velocity = self.velocity - (self.friction * 9.8 * delta_time) * self.velocity.normalize()

        else:
            self.is_active = False
            self.velocity = pygame.Vector2()

        self.center += self.velocity * delta_time

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.center - pygame.Vector2(self.image.get_size()) / 2)