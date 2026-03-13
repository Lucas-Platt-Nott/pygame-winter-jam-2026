import pygame
import math
from config import *
from assets import Images, render_outlined, alagard_medium, alagard_small
from systems import PokerSystem, PhaseState, RoundState


class PokerRenderer:
    def __init__(self):
        self.current_phase = None
        self.top_prompt = pygame.Surface((0, 0))
        self.bot_prompt = pygame.Surface((0, 0))
        self.alpha = 0
        self.time_elapsed = 0

        # Chip image
        self.chip_image = pygame.transform.scale_by(Images.get_image("chip"), 3/2)

        # Deck image
        self.deck_image = pygame.transform.scale_by(Images.get_image("card_back"), 1.2)

        # Pot display
        self.pot_balance = pygame.Surface((0, 0))
        self.display_pot_chips = 0  # animated pot value
        self.pot_shake_offset = 0.0

        # Deck count display
        self.deck_count_surface = pygame.Surface((0, 0))

        # Hand value/type text
        self.hand_value_text = None
        self.hand_type_text = None

    # ---------------------------------------------------------
    # POT TEXT UPDATE (smooth + soft highlight)
    # ---------------------------------------------------------
    def update_balance_text(self, system: PokerSystem, highlight: bool = False) -> None:
        target = system.pot_chips

        # Much smoother easing
        self.display_pot_chips += (target - self.display_pot_chips) * 0.08

        # Soft pulse when highlighted
        if highlight:
            t = self.time_elapsed
            pulse = 0.5 + 0.5 * math.sin(3 * t)
            r = 255
            g = int(220 + 35 * pulse)
            b = int(180 + 40 * pulse)
            color = (r, g, b)
        else:
            color = (255, 255, 255)

        self.pot_balance = render_outlined(
            alagard_medium,
            f"Frozen Funds Remaining: {int(self.display_pot_chips)}",
            color,
            (0, 0, 0),
            1
        )

    # ---------------------------------------------------------
    # DECK COUNT UPDATE
    # ---------------------------------------------------------
    def update_deck_display(self, system: PokerSystem) -> None:
        current = len(system.deck.cards)
        maximum = len(system.deck.standard_cards)

        self.deck_count_surface = render_outlined(
            alagard_small,
            f"{current}/{maximum}",
            (255, 255, 255),
            (0, 0, 0),
            1
        )

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------
    def update(self, delta_time: float, system: PokerSystem) -> None:
        phase = system.state["phase"]
        phase_name = phase.name

        # Detect phase change
        if self.current_phase != phase:
            self.current_phase = phase
            self.alpha = 0
            self.time_elapsed = 0
        else:
            self.time_elapsed += delta_time

        # Fade-in prompts
        if self.alpha < 255:
            self.alpha = min(self.alpha + 255 * delta_time, 255)
            self.top_prompt = Images.get_image(f"{phase_name}_top")
            self.bot_prompt = Images.get_image(f"{phase_name}_bot")

            if phase == PhaseState.DISCARD and system.state["round"] == RoundState.PRE_FLOP:
                self.top_prompt = Images.get_image(f"{phase_name}_top_preflop")

            self.top_prompt.set_alpha(self.alpha)
            self.bot_prompt.set_alpha(self.alpha)

        # Pulsing discard/freeze prompt
        elif self.current_phase in [PhaseState.DISCARD, PhaseState.FREEZE]:
            self.bot_prompt = Images.get_image(f"{phase_name}_bot")

            if (
                len(system.player.hand.get_selected_cards()) == system.to_discard
                and self.current_phase == PhaseState.DISCARD
            ) or (
                len(system.player.hand.get_selected_cards()) > 0
                and self.current_phase == PhaseState.FREEZE
            ):
                h = (455 / 2) + (55 / 2) * math.cos(20 * self.time_elapsed)
                self.bot_prompt.fill((h, h, h), special_flags=pygame.BLEND_RGB_MULT)

        # Hand value/type text during HAND_SELECTION
        if phase == PhaseState.HAND_SELECTION:
            hand = system.player.hand

            self.hand_value_text = render_outlined(
                alagard_small,
                f"Hand Value: {hand.value}",
                (255, 255, 255),
                (0, 0, 0),
                1
            )

            self.hand_type_text = render_outlined(
                alagard_small,
                f"Hand Type: {hand.hand_type.title()}",
                (255, 255, 255),
                (0, 0, 0),
                1
            )
        else:
            self.hand_value_text = None
            self.hand_type_text = None

        # ---------------------------------------------------------
        # SHOWDOWN POT ANIMATION (gentle)
        # ---------------------------------------------------------
        is_showdown = (
            system.state["round"] == RoundState.SHOWDOWN
            and system.state["phase"] == PhaseState.SHOWDOWN
        )

        if is_showdown:
            self.pot_shake_offset = 1.5 * math.sin(10 * self.time_elapsed)
        else:
            self.pot_shake_offset = 0.0

        # Update pot text
        self.update_balance_text(system, highlight=is_showdown)

        # Update deck text
        self.update_deck_display(system)

    # ---------------------------------------------------------
    # DRAW
    # ---------------------------------------------------------
    def draw(self, surface: pygame.Surface, system: PokerSystem) -> None:
        player_hand = system.player.hand
        other_hand = system.opponent.hand

        # Prompt positions
        toprect = self.top_prompt.get_rect()
        botrect = self.bot_prompt.get_rect()
        toprect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - CARD_SIZE[1] * 0.8)
        botrect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + CARD_SIZE[1] * 0.9)

        # Input prompt (tutorial)
        if system.tutorial_enabled and system.state["phase"] in [
            PhaseState.DISCARD,
            PhaseState.FREEZE,
            PhaseState.HAND_SELECTION
        ]:
            prompt = Images.get_image("input_prompt")
            prect = prompt.get_rect()
            prect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + CARD_SIZE[1] * 0.7)
            surface.blit(prompt, prect)

        # Draw prompts
        surface.blit(self.top_prompt, toprect)
        surface.blit(self.bot_prompt, botrect)

        # ---------------------------------------------------------
        # POT DISPLAY (with gentle shake)
        # ---------------------------------------------------------
        base_y = SCREEN_SIZE[1] * 0.215 + self.pot_shake_offset

        surface.blit(
            self.chip_image,
            (
                SCREEN_SIZE[0] * 0.465 - self.chip_image.height // 2 - self.pot_balance.width // 2,
                base_y
            )
        )

        surface.blit(
            self.pot_balance,
            (
                SCREEN_SIZE[0] * 0.465 - self.chip_image.height // 2 - self.pot_balance.width // 2
                + self.chip_image.width * 1.25,
                base_y + self.pot_balance.height // 2
            )
        )

        surface.blit(
            self.chip_image,
            (
                SCREEN_SIZE[0] * 0.465 - self.chip_image.height // 2 - self.pot_balance.width // 2
                + self.chip_image.width * 1.5 + self.pot_balance.width,
                base_y
            )
        )

        # ---------------------------------------------------------
        # DECK DISPLAY (icon + count)
        # ---------------------------------------------------------
        deck_x = SCREEN_SIZE[0] * 0.025
        deck_y = SCREEN_SIZE[1] - self.deck_image.height - self.deck_count_surface.height - 25

        # Draw deck icon
        surface.blit(self.deck_image, (deck_x, deck_y))

        # Draw deck count text
        count_rect = self.deck_count_surface.get_rect()
        count_rect.center = (deck_x + self.deck_image.get_width() // 2,
                             deck_y + self.deck_image.get_height() + 18)
        surface.blit(self.deck_count_surface, count_rect)

        # ---------------------------------------------------------
        # HAND VALUE + TYPE (during HAND_SELECTION)
        # ---------------------------------------------------------
        if system.state["phase"] == PhaseState.HAND_SELECTION:
            if self.hand_value_text:
                rect = self.hand_value_text.get_rect()
                rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] * 0.72)
                surface.blit(self.hand_value_text, rect)

            if self.hand_type_text:
                rect2 = self.hand_type_text.get_rect()
                rect2.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] * 0.75)
                surface.blit(self.hand_type_text, rect2)

        # ---------------------------------------------------------
        # CARDS
        # ---------------------------------------------------------
        player_hand.draw(surface)
        other_hand.draw(surface)
        system.community_cards.draw(surface)
