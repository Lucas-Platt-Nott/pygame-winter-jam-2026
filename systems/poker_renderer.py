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
        self.display_pot_chips = 0
        self.pot_shake_offset = 0.0

        # NEW: static pot change display (only during showdown)
        self.pot_change_surface = pygame.Surface((0, 0))
        self.pot_change_value = 0  # no animation

        # Deck count display
        self.deck_count_surface = pygame.Surface((0, 0))

        # Hand value/type text
        self.hand_value_text = None
        self.hand_type_text = None

        # NEW: opponent hand value display
        self.opponent_value_surface = pygame.Surface((0, 0))

        # NEW: player hand value display (bottom)
        self.player_value_surface = pygame.Surface((0, 0))

    # ---------------------------------------------------------
    # POT TEXT UPDATE (smooth + soft highlight)
    # ---------------------------------------------------------
    def update_balance_text(self, system: PokerSystem, highlight: bool = False) -> None:
        target = system.pot_chips

        # Smooth easing
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
    # STATIC POT CHANGE (only during showdown)
    # ---------------------------------------------------------
    def update_pot_change(self, system: PokerSystem) -> None:
        if (
            system.state["round"] == RoundState.SHOWDOWN
            and system.state["phase"] == PhaseState.SHOWDOWN
        ):
            # Difference between player and opponent hand values
            diff = system.player.hand.value - system.opponent.hand.value
            self.pot_change_value = diff

            # Color coding
            if diff < 0:
                color = (255, 120, 120)
            elif diff > 0:
                color = (120, 255, 120)
            else:
                color = (200, 200, 200)

            sign = "+" if diff > 0 else ""
            self.pot_change_surface = render_outlined(
                alagard_small,
                f"{sign}{diff}",
                color,
                (0, 0, 0),
                1
            )
        else:
            # Hide outside showdown
            self.pot_change_surface = pygame.Surface((0, 0))
            self.pot_change_value = 0

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
    # OPPONENT HAND VALUE UPDATE
    # ---------------------------------------------------------
    def update_opponent_value(self, system: PokerSystem) -> None:
        if (
            system.state["round"] == RoundState.SHOWDOWN
            and system.state["phase"] == PhaseState.SHOWDOWN
        ):
            val = system.opponent.hand.value
            self.opponent_value_surface = render_outlined(
                alagard_medium,
                f"Opponent Hand Value: {val}",
                (255, 200, 200),
                (0, 0, 0),
                1
            )
        else:
            self.opponent_value_surface = pygame.Surface((0, 0))

    # ---------------------------------------------------------
    # PLAYER HAND VALUE UPDATE (bottom)
    # ---------------------------------------------------------
    def update_player_value(self, system: PokerSystem) -> None:
        if (
            system.state["round"] == RoundState.SHOWDOWN
            and system.state["phase"] == PhaseState.SHOWDOWN
        ):
            val = system.player.hand.value
            self.player_value_surface = render_outlined(
                alagard_medium,
                f"Your Hand Value: {val}",
                (200, 255, 200),
                (0, 0, 0),
                1
            )
        else:
            self.player_value_surface = pygame.Surface((0, 0))

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

        # NEW: static pot change
        self.update_pot_change(system)

        # Update deck text
        self.update_deck_display(system)

        # Update opponent hand value
        self.update_opponent_value(system)

        # NEW: update player hand value
        self.update_player_value(system)

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

        # ---------------------------------------------------------
        # OPPONENT HAND VALUE (replaces top prompt during showdown)
        # ---------------------------------------------------------
        if (
            system.state["round"] == RoundState.SHOWDOWN
            and system.state["phase"] == PhaseState.SHOWDOWN
        ):
            opp_rect = self.opponent_value_surface.get_rect()
            opp_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - CARD_SIZE[1] * 0.8)
            surface.blit(self.opponent_value_surface, opp_rect)
        else:
            surface.blit(self.top_prompt, toprect)

        # ---------------------------------------------------------
        # PLAYER HAND VALUE (replaces bottom prompt during showdown)
        # ---------------------------------------------------------
        if (
            system.state["round"] == RoundState.SHOWDOWN
            and system.state["phase"] == PhaseState.SHOWDOWN
        ):
            player_rect = self.player_value_surface.get_rect()
            player_rect.center = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + CARD_SIZE[1] * 0.9)
            surface.blit(self.player_value_surface, player_rect)
            botrect.y -= self.player_value_surface.height
        surface.blit(self.bot_prompt, botrect)

        # ---------------------------------------------------------
        # POT DISPLAY (with gentle shake)
        # ---------------------------------------------------------
        base_y = SCREEN_SIZE[1] * 0.215 + self.pot_shake_offset

        # Left chip
        surface.blit(
            self.chip_image,
            (
                SCREEN_SIZE[0] * 0.465 - self.chip_image.height // 2 - self.pot_balance.width // 2,
                base_y
            )
        )

        # Pot balance text
        surface.blit(
            self.pot_balance,
            (
                SCREEN_SIZE[0] * 0.465 - self.chip_image.height // 2 - self.pot_balance.width // 2
                + self.chip_image.width * 1.25,
                base_y + self.pot_balance.height // 2
            )
        )

        # Right chip
        surface.blit(
            self.chip_image,
            (
                SCREEN_SIZE[0] * 0.465 - self.chip_image.height // 2 - self.pot_balance.width // 2
                + self.chip_image.width * 1.5 + self.pot_balance.width,
                base_y
            )
        )

        # ---------------------------------------------------------
        # POT CHANGE (static, only during showdown)
        # ---------------------------------------------------------
        if self.pot_change_value != 0:
            change_rect = self.pot_change_surface.get_rect()
            change_rect.center = (
                SCREEN_SIZE[0] * 0.465 + self.pot_balance.width * 0.25,
                base_y + self.pot_balance.height + 20
            )
            surface.blit(self.pot_change_surface, change_rect)

        # ---------------------------------------------------------
        # DECK DISPLAY (icon + count)
        # ---------------------------------------------------------
        deck_x = SCREEN_SIZE[0] * 0.025
        deck_y = SCREEN_SIZE[1] - self.deck_image.height - self.deck_count_surface.height - 25

        surface.blit(self.deck_image, (deck_x, deck_y))

        count_rect = self.deck_count_surface.get_rect()
        count_rect.center = (
            deck_x + self.deck_image.get_width() // 2,
            deck_y + self.deck_image.get_height() + 18
        )
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

        if system.victory_timer >= 0:
            h = 255 - 255/3 * min(system.victory_timer, 3)
            surface.fill((h, h, h), special_flags=pygame.BLEND_RGB_MULT)