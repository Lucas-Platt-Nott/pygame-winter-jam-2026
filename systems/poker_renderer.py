import pygame
import math
from config import *
from assets import Images, render_outlined, alagard_small
from systems import PokerSystem, PhaseState, RoundState

class PokerRenderer:
    def __init__(self):
        self.current_phase = None
        self.top_prompt = pygame.Surface((0, 0))
        self.bot_prompt = pygame.Surface((0, 0))
        self.alpha = 0
        self.time_elapsed = 0
        self.chip_image = Images.get_image("chip")

        self.player_balance = pygame.Surface((0, 0))
        self.opponent_balance = pygame.Surface((0, 0))

    def update_balance_text(self, system: PokerSystem) -> None:
        self.player_balance = render_outlined(alagard_small, f"Chips: {system.player.chips}", (255, 255, 255), (0, 0, 0), 1)
        self.opponent_balance = render_outlined(alagard_small, f"Chips: {system.opponent.chips}", (255, 255, 255), (0, 0, 0), 1)

    def update(self, delta_time: float, system: PokerSystem) -> None:
        phase = system.state["phase"]
        phase_name = phase.name

        if self.current_phase != phase:
            self.current_phase = phase
            self.alpha = 0
            self.time_elapsed = 0

        elif self.alpha < 255:
            self.alpha = min(self.alpha + 255 * delta_time, 255)
            self.top_prompt = Images.get_image(f"{phase_name}_top")

            if phase == PhaseState.DISCARD and system.state["round"] == RoundState.PRE_FLOP:
                self.top_prompt = Images.get_image(f"{phase_name}_top_preflop")
            
            self.top_prompt.set_alpha(self.alpha)
            self.bot_prompt = Images.get_image(f"{phase_name}_bot")
            self.bot_prompt.set_alpha(self.alpha)

        elif self.current_phase in [PhaseState.DISCARD, PhaseState.FREEZE]:
            self.bot_prompt = Images.get_image(f"{phase_name}_bot")
            
            if len(system.player.hand.get_selected_cards()) == system.to_discard and self.current_phase == PhaseState.DISCARD or len(system.player.hand.get_selected_cards()) > 0 and self.current_phase == PhaseState.FREEZE:
                self.time_elapsed += delta_time
                h = (455 / 2) + (55 / 2) * math.cos(20 * self.time_elapsed)
                self.bot_prompt.fill((h, h, h), special_flags=pygame.BLEND_RGB_MULT)

    def draw(self, surface: pygame.Surface, system: PokerSystem) -> None:
        player_hand = system.player.hand
        other_hand = system.opponent.hand

        toprect = self.top_prompt.get_rect()
        botrect = self.bot_prompt.get_rect()
        toprect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - CARD_SIZE[1] * 0.75)
        botrect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + CARD_SIZE[1] * 0.75)

        if system.tutorial_enabled:
            surface.blit(self.top_prompt, toprect)
            prompt = Images.get_image("input_prompt")
            prect = prompt.get_rect()
            prect.bottomright = (SCREEN_SIZE[0], SCREEN_SIZE[1])
            surface.blit(prompt, prect)

        surface.blit(self.bot_prompt, botrect)

        # Player balance
        surface.blit(self.chip_image, (SCREEN_SIZE[0] * 0.4 - self.chip_image.height // 2, SCREEN_SIZE[1] * 0.25))
        surface.blit(self.player_balance, (SCREEN_SIZE[0] * 0.4 - self.chip_image.height // 2, SCREEN_SIZE[1] * 0.25))

        # Opponent balance
        surface.blit(self.chip_image, (SCREEN_SIZE[0] * 0.4 - self.chip_image.width // 2, SCREEN_SIZE[1] * 0.7))
        surface.blit(self.opponent_balance, (SCREEN_SIZE[0] * 0.4 - self.chip_image.width // 2, SCREEN_SIZE[1] * 0.7))

        player_hand.draw(surface)
        other_hand.draw(surface)
        system.community_cards.draw(surface)
