# Built-In
import math

# External
import pygame
from pygame.locals import *

# Internal
from assets import Images, Sounds, alagard_medium
from core import SceneManager, Scene
from config import *
from systems import PokerSystem, PokerRenderer, PokerPlayer, Player, PhaseState


# Poker Class
class Poker(Scene):
    def __init__(self, scene_manager: SceneManager, player: Player) -> None:
        self.scene_manager = scene_manager
        self.player = player

        self.animation_time = 0
        self.loading = False
        self.system = PokerSystem(self.player, PokerPlayer())

        # Streaming intro text
        self.intro_prompt = Images.get_image("intro_prompt")
        self.intro_text = (
            "Your funds are locked in ice.\n"
            "Not lost - just frozen, out of reach until you earn them back.\n\n"
            "To thaw them, you'll have to take a seat at the table.\n"
            "Every hand you play pushes against the freeze holding your bankroll still.\n\n"
            "Win the hand, and the freeze begins to crack,\n"
            "small breaks forming as your money starts to loosen.\n\n"
            "Lose, and the cold holds on a little longer,\n"
            "keeping your funds sealed away until you try again."
        )

        self.visible_text = ""
        self.text_timer = 0.0
        self.text_speed = 0.05  # seconds per character

        # Create a surface big enough for the intro text
        self.intro_image = pygame.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1]), pygame.SRCALPHA)

        self.renderer = PokerRenderer()

    def start(self) -> None:
        self.loading = True
        self.player.reset()
        self.system = PokerSystem(self.player, PokerPlayer())

        # Reset streaming text
        self.visible_text = ""
        self.text_timer = 0.0

        Sounds.get_sound("background_music").play(-1, -1, 5000)
        self.renderer.update_balance_text(self.system)

    def handle_event(self, event: pygame.Event) -> None:
        if self.loading:
            if event.type == KEYDOWN and event.key == K_RETURN:
                self.loading = False
            return

        self.system.handle_event(event)

    def update(self, delta_time: float) -> None:
        if self.loading:
            # Update streaming text
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

            self.animation_time += delta_time
            hue = (455 / 2) + (55 / 2) * math.cos(5 * self.animation_time)
            self.intro_prompt = Images.get_image("intro_prompt")
            self.intro_prompt.fill((hue, hue, hue), special_flags=BLEND_RGB_MULT)

            return

        # Normal game logic
        if self.system.state["phase"] == PhaseState.BET:
            self.renderer.update_balance_text(self.system)

        self.system.update(delta_time)
        self.renderer.update(delta_time, self.system)

    def draw(self, surface: pygame.Surface) -> None:
        if self.loading:
            surface.blit(self.intro_image, (0, 0))
            surface.blit(self.intro_prompt, (SCREEN_SIZE[0] // 2 - self.intro_prompt.width // 2, SCREEN_SIZE[1] * 0.9 - self.intro_prompt.height))
            return

        self.renderer.draw(surface, self.system)
