# External
import pygame
from pygame.locals import *

# Internal
from core.assets import *

# Functions
def load_text(text: str, image_name: str, font: pygame.Font, font_colour: tuple = (255, 255, 255)):
    text_image = font.render(text, True, font_colour)
    Images.register_image(text_image, image_name)

def load_outlined_text(text: str, image_name: str, font: pygame.Font, font_colour: tuple = (255, 255, 255), outline_colour: tuple = (1, 1, 1), outline_width: int = 1):
    # Render main text
    text_surface = font.render(text, True, font_colour)
    width, height = text_surface.get_size()

    # Surface to hold text + outline
    image = pygame.Surface((width + 2*outline_width, height + 2*outline_width), pygame.SRCALPHA)

    # Render outline in all 8 surrounding positions
    for x_offset in range(-outline_width, outline_width + 1):
        for y_offset in range(-outline_width, outline_width + 1):
            if x_offset != 0 or y_offset != 0:
                outline = font.render(text, True, outline_colour)
                image.blit(outline, (x_offset + outline_width - 0.3, y_offset + outline_width - 0.3))

    # Blit main text on top
    image.blit(text_surface, (outline_width, outline_width))

    # Register the final image
    Images.register_image(image, image_name)

# Instantiate asset-manager(s)
Images = ImageManager()
Sounds = SoundManager()

# Initialise pygame for loading images
pygame.init()
pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))
loading_screen = pygame.display.set_mode((0, 0))

# Load Fonts
alagard_font = pygame.Font("assets/fonts/alagard.ttf", 16)

# Load Images
Images.load_image("assets/images/icon.png", "icon")
Images.load_image("assets/images/placeholder.webp", "placeholder_background", image_size=(640, 360))

# Load Text
load_text("Furnace: Smelts ore at a rate of 20/m.\n              Produces ingots at a rate of 10/m", "title", alagard_font)