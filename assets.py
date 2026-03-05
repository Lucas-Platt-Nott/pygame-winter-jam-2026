# External
import pygame

# Internal
from core import ImageManager
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

# Load fonts
pygame.font.init()
alagard = pygame.Font("assets/fonts/alagard.ttf", 128)

# Load text
Images.register_image(render_outlined(alagard, "FROZEN\n FUNDS", (255, 255, 255), (1, 1, 1), 4), "title")

# Load images
title_background = pygame.Surface(SCREEN_SIZE)
title_background.fill((20, 20, 40))

Images.register_image(
    title_background,
    "title-background"
)

Images.register_image(
    pygame.transform.scale(pygame.image.load("card.png"), CARD_SIZE),
    "default_card"
)

Images.register_image(
    pygame.transform.scale(pygame.image.load("frozen_card.png"), CARD_SIZE),
    "frozen_card"
)