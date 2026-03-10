# External
import pygame

# Internal
from assets import Images
from systems import PokerSystem

# Poker Renderer Class
class PokerRenderer:
    def __init__(self):
        pass

    def update(self, delta_time: float) -> None:
        pass

    def draw(self, surface: pygame.Surface, system: PokerSystem) -> None:
        player_hand = system.player.hand
        other_hand = system.opponent.hand

        surface.blit(Images.get_image("poker-background"), (0, 0))

        player_hand.draw(surface)
        other_hand.draw(surface)
        system.community_cards.draw(surface)