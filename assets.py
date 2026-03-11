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

# Draw prompts
Images.register_image(render_outlined(alagard_small, "Cards are dealt at the start of each phase:", (125, 125, 125), (1, 1, 1), 1), "DRAWING_top")
Images.register_image(render_outlined(alagard_small, "Dealing cards..", (125, 125, 125), (1, 1, 1), 1), "DRAWING_bot")

Images.register_image(render_outlined(alagard_small, "Community Cards are dealt at the end of each phase:", (125, 125, 125), (1, 1, 1), 1), "DRAW_top")
Images.register_image(render_outlined(alagard_small, "[Press Enter to Advance to Next Phase]", (125, 125, 125), (1, 1, 1), 1), "DRAW_bot")

# Bet prompts
Images.register_image(render_outlined(alagard_small, "Would you like to raise the pot? If so by how much?", (125, 125, 125), (1, 1, 1), 1), "BET_top")
Images.register_image(render_outlined(alagard_small, "[Press Enter to Place Bet]", (125, 125, 125), (1, 1, 1), 1), "BET_bot")

# Freeze prompts
Images.register_image(render_outlined(alagard_small, "        Select one Regular Card to Freeze\nThe Frozen Card will no longer be discarded.", (125, 125, 125), (1, 1, 1), 1), "FREEZE_top")
Images.register_image(render_outlined(alagard_small, "[Press Enter to Freeze Selected]", (125, 125, 125), (1, 1, 1), 1), "FREEZE_bot")

# Discard prompts
Images.register_image(render_outlined(alagard_small, "Discard until you have no more than 2 Regular Cards.\n     (Discarded cards are NOT returned to The Deck)", (125, 125, 125), (1, 1, 1), 1), "DISCARD_top")
Images.register_image(render_outlined(alagard_small, "[Press Enter to Discard Selected]", (125, 125, 125), (1, 1, 1), 1), "DISCARD_bot")

# Keybind prompt(s)
Images.register_image(render_outlined(alagard_small, "1-9: Select card at Position\nENTER: Confirm selection", (200, 200, 200), (1, 1, 1), 1), "input_prompt")

# Load images
title_background = pygame.Surface(SCREEN_SIZE)
title_background.fill((10, 10, 20))
Images.register_image(title_background, "title-background")

# --- Load Poker Background ---
poker_background = pygame.transform.scale(
    pygame.image.load("assets/images/background.png"),
    (int(SCREEN_SIZE[0] * 1.2), int(SCREEN_SIZE[0] * 1.2))
).convert()

poker_background.fill((70, 70, 70), special_flags=pygame.BLEND_RGB_MULT)
poker_background = pygame.transform.gaussian_blur(poker_background, 10)

Images.register_image(poker_background, "poker-background")

# Load borderless card
borderless = pygame.transform.scale(
    pygame.image.load("assets/images/borderless_card.png"),
    CARD_SIZE
).convert_alpha()

borderless = pygame.transform.grayscale(borderless)
borderless.set_alpha(150)

Images.register_image(borderless, "borderless_card")

# Load card images
for file_path in os.listdir("assets/images/cards"):
    Images.register_image(
        pygame.transform.scale(
            pygame.image.load(f"assets/images/cards/{file_path}"),
            CARD_SIZE
        ).convert_alpha(),
        file_path.split(".")[0],
        colorkey=(0, 255, 255)
    )
