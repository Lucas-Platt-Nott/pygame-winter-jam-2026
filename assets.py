# Built-In
import os

# External
import pygame

# Internal
from core import ImageManager, SoundManager
from config import *

# Pre-Load window for asset initialisation
pygame.display.set_mode(flags=pygame.HIDDEN)

# Helper Functions
def load_cards():
    for suit in SUITS:
        for rank in RANKS:
            pass

def render_outlined(
    font: pygame.Font,
    text: str,
    text_color: pygame.typing.ColorLike,
    outline_color: pygame.typing.ColorLike,
    outline_width: int,
) -> pygame.Surface:
    old_outline = font.outline
    if old_outline != 0:
        font.outline = 0
    base_text_surf = font.render(text, True, text_color)
    font.outline = outline_width
    outlined_text_surf = font.render(text, True, outline_color)

    outlined_text_surf.blit(base_text_surf, (outline_width, outline_width))
    font.outline = old_outline
    return outlined_text_surf

# Asset-Manager(s)
Images = ImageManager()
Sounds = SoundManager()

# Load sounds
Sounds.load_sound("assets/sounds/title-bgm.wav", "title-background")

# Load fonts
pygame.font.init()
alagard_large = pygame.Font("assets/fonts/alagard.ttf", 128)
alagard = pygame.Font("assets/fonts/alagard.ttf", 64)
alagard_small = pygame.Font("assets/fonts/alagard.ttf", 16)

# Load text
Images.register_image(render_outlined(alagard_large, "FROZEN\n FUNDS", (255, 255, 255), (41, 51, 61), 4), "title")
Images.register_image(render_outlined(alagard_small, "(Made for Pygame Winter Jam 2026 by ImNottL & Commando)", (125, 125, 125), (1, 1, 1), 1), "credits")

Images.register_image(render_outlined(alagard, "Play", (255, 255, 255), (1, 1, 1), 4), "title-play-text")
Images.register_image(render_outlined(alagard, "Settings", (255, 255, 255), (1, 1, 1), 4), "title-settings-text")
Images.register_image(render_outlined(alagard, "Quit", (255, 255, 255), (1, 1, 1), 4), "title-quit-text")

# Load images
title_background = pygame.Surface(SCREEN_SIZE)
title_background.fill((10, 10, 20))

Images.register_image(
    title_background,
    "title-background"
)

poker_background = pygame.transform.scale(pygame.image.load(f"assets/images/poker_background.png"), SCREEN_SIZE)
poker_background.fill((112, 112, 112), special_flags=pygame.BLEND_RGB_MULT)
poker_background = pygame.transform.gaussian_blur(poker_background, 10)

Images.register_image(
    poker_background,
    "poker-background"
)

borderless = pygame.transform.scale(pygame.image.load(f"assets/images/borderless_card.png"), CARD_SIZE)
borderless = pygame.transform.grayscale(borderless)

borderless.set_alpha(150)

Images.register_image(
    borderless,
    "borderless_card"
)


# Load card images
for file_path in os.listdir("assets/images/cards"):
    Images.register_image(
        pygame.transform.scale(
            pygame.image.load(f"assets/images/cards/{file_path}"),
            CARD_SIZE
        ),
        file_path.split(".")[0],
        colorkey=(0, 255, 255)
    )