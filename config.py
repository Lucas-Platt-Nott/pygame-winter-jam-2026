# Built-In
import json

# Card-Data
with open("data/cards.json", "r") as file:
    CARD_DATA = json.load(file)

    TYPES = CARD_DATA["types"]
    SUITS = CARD_DATA["suits"]
    RANKS = CARD_DATA["ranks"]

# Card-Values
with open("data/values.json", "r") as file:
    VALUES = json.load(file)

# Hand-Data
with open("data/hands.json", "r") as file:
    HAND_DATA = json.load(file)


# Sizes
ANIM_SPEED = 1.5
SCREEN_SIZE = (1024, 576)
CARD_SIZE = (
    int(60 * 4/3),
    int(84 * 4/3)
)

# Hand-Rendering Settings
MAX_ANGLE = 5