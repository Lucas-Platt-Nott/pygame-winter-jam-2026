import pygame
import math
from config import *
from assets import Images, render_outlined, alagard_medium
from systems import PokerSystem, PhaseState, RoundState

class PokerRenderer:
    def __init__(self):
        self.current_phase = None
        self.top_prompt = pygame.Surface((0, 0))
        self.bot_prompt = pygame.Surface((0, 0))
        self.alpha = 0
        self.time_elapsed = 0
        self.chip_image = pygame.transform.scale_by(Images.get_image("chip"), 3/2)

        self.pot = pygame.Surface((0, 0))

    def update_balance_text(self, system: PokerSystem) -> None:
        self.pot_balance = render_outlined(alagard_medium, f"Frozen Funds Remaining: {system.pot_chips}", (255, 255, 255), (0, 0, 0), 1)

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
            self.bot_prompt = Images.get_image(f"{phase_name}_bot")

            if phase == PhaseState.DISCARD and system.state["round"] == RoundState.PRE_FLOP:
                self.top_prompt = Images.get_image(f"{phase_name}_top_preflop")
            
            self.top_prompt.set_alpha(self.alpha)
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

        if system.tutorial_enabled and system.state["phase"] in [PhaseState.DISCARD, PhaseState.FREEZE, PhaseState.HAND_SELECTION]:
            prompt = Images.get_image("input_prompt")
            prect = prompt.get_rect()
            prect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + CARD_SIZE[1] * 0.59)
            surface.blit(prompt, prect)

        surface.blit(self.top_prompt, toprect)
        surface.blit(self.bot_prompt, botrect)

        # Opponent balance
        surface.blit(self.chip_image, (SCREEN_SIZE[0] * 0.465 - self.chip_image.height // 2 - self.pot_balance.width // 2, SCREEN_SIZE[1] * 0.215))
        surface.blit(self.pot_balance, (SCREEN_SIZE[0] * 0.465 - self.chip_image.height // 2 - self.pot_balance.width // 2 + self.chip_image.width * 1.25, SCREEN_SIZE[1] * 0.215 + self.pot_balance.height // 2))
        surface.blit(self.chip_image, (SCREEN_SIZE[0] * 0.465 - self.chip_image.height // 2 - self.pot_balance.width // 2 + self.chip_image.width * 1.5 + self.pot_balance.width, SCREEN_SIZE[1] * 0.215))

        # Player balance

        player_hand.draw(surface)
        other_hand.draw(surface)
        system.community_cards.draw(surface)
