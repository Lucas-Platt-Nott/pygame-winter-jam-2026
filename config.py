# Dimensions
SCREEN_SIZE = (1024, 576)
CARD_SIZE = (60, 84)

# Card config
TYPES: list[str] = ["default", "frozen"]
SUITS: list[str] = ["hearts", "diamonds", "spades", "clubs"]
RANKS: list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
VALUES: dict[str, int] = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}