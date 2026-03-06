# Built-In
import json

# Sizes
SCREEN_SIZE = (1024, 576)
CARD_SIZE = (
    int(60 * 1.35),
    int(84 * 1.35)
)

# Card-Data
with open("data/cards.json", "r") as file:
    CARD_DATA = json.load(file)

    TYPES = CARD_DATA["types"]
    SUITS = CARD_DATA["suits"]
    RANKS = CARD_DATA["ranks"]

with open("data/values.json", "r") as file:
    VALUES = json.load(file)

# Hand-Data
with open("data/hands.json", "r") as file:
    HAND_DATA = json.load(file)