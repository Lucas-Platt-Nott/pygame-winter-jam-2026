# Built-In
import math

# External
import pygame
from pygame.locals import *

# Internal
from assets import Images, Sounds, alagard_medium
from core import SceneManager, Scene
from config import *
from systems import Player

# Victory Class
class Victory(Scene):
    def __init__(self, scene_manager: SceneManager, player: Player) -> None:
        self.scene_manager = scene_manager
        self.player = player

        self.animation_time = 0
        self.loading = False

        # Streaming intro text
        self.intro_text = (
            "The ice finally gives way.\n"
            "Your funds break free from the freeze and return to your hands.\n\n"
            "You pushed through every cold setback, every slow crack in the surface,\n"
            "and the table couldn't hold you any longer.\n\n"
            "The freeze is over.\n"
            "Your bankroll is yours again.\n\n"
            "Thanks for playing!!"
        )

        self.visible_text = ""
        self.text_timer = 0.0
        self.text_speed = 0.05  # seconds per character

        # Delay before text starts streaming
        self.text_delay = 1.5      # seconds
        self.delay_timer = 0.0

        # Fade-in effect
        self.fade_alpha = 255
        self.fade_duration = 2.0   # seconds
        self.fade_timer = 0.0

        # Create a surface big enough for the intro text
        self.intro_image = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]), pygame.SRCALPHA)

    def start(self) -> None:
        self.loading = True

        # Reset streaming text
        self.visible_text = ""
        self.text_timer = 0.0
        self.delay_timer = 0.0

        # Reset fade
        self.fade_alpha = 255
        self.fade_timer = 0.0

    def update(self, delta_time: float) -> None:
        if not self.loading:
            return

        # -------------------------
        # 1. Fade-in effect
        # -------------------------
        if self.fade_alpha > 0:
            self.fade_timer += delta_time
            progress = min(self.fade_timer / self.fade_duration, 1.0)
            self.fade_alpha = int(255 * (1 - progress))

        # -------------------------
        # 2. Delay before text starts
        # -------------------------
        if self.delay_timer < self.text_delay:
            self.delay_timer += delta_time
            return  # do not start text yet

        # -------------------------
        # 3. Streaming text
        # -------------------------
        self.text_timer += delta_time
        chars_to_show = int(self.text_timer / self.text_speed)

        if chars_to_show > len(self.visible_text):
            self.visible_text = self.intro_text[:chars_to_show]

            # Clear intro surface
            self.intro_image.fill((0, 0, 0, 0))

            # Split into lines (including partially revealed ones)
            lines = self.visible_text.split("\n")

            # Vertical centering
            line_height = alagard_medium.get_height()
            total_height = len(lines) * line_height
            y = SCREEN_SIZE[1] // 2 - total_height // 2

            # Render each line centered
            for line in lines:
                text_surface = alagard_medium.render(line, True, (255, 255, 255))
                x = (SCREEN_SIZE[0] - text_surface.get_width()) // 2
                self.intro_image.blit(text_surface, (x, y))
                y += line_height

        # Prompt animation (unchanged)
        self.animation_time += delta_time
        hue = (455 / 2) + (55 / 2) * math.cos(5 * self.animation_time)
        self.intro_prompt = Images.get_image("intro_prompt")
        self.intro_prompt.fill((hue, hue, hue), special_flags=BLEND_RGB_MULT)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.intro_image, (0, 0))

        # Fade overlay
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface(SCREEN_SIZE)
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            surface.blit(fade_surface, (0, 0))
