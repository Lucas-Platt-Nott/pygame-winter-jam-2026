import pygame
from config import *
from assets import Images
from systems import PokerSystem

class PokerRenderer:
    def __init__(self):
        self.angle = 0
        self.rotated = Images.get_image("poker-background-0")

    def update(self, delta_time: float) -> None:
        # Increase angle at a reasonable speed
        self.angle = (self.angle + delta_time * 10) % 360
        self.rotated = Images.get_image(f"poker-background-{int(self.angle)}")

    def draw(self, surface: pygame.Surface, system: PokerSystem) -> None:
        player_hand = system.player.hand
        other_hand = system.opponent.hand

        rect = self.rotated.get_rect()
        rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)

        surface.blit(self.rotated, rect)

        player_hand.draw(surface)
        other_hand.draw(surface)
        system.community_cards.draw(surface)
