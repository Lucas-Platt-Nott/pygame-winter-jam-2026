# Built-In
import random
from enum import Enum, auto

# External
import pygame
from pygame.locals import *

# Internal
from assets import Sounds
from config import *
from systems import PokerPlayer, Player, Deck, CommunityCards, HandCalculator


# Poker Round/Phase States
class RoundState(Enum):
    PRE_FLOP = auto()
    FLOP = auto()
    RIVER = auto()
    TURN = auto()
    SHOWDOWN = auto()
    NEXT_ROUND = auto()


class PhaseState(Enum):
    DRAW = auto()
    DRAWING = auto()
    BET = auto()
    FREEZE = auto()
    DISCARD = auto()
    NEXT_PHASE = auto()
    HAND_SELECTION = auto()
    EVALUATION = auto()
    SHOWDOWN = auto()


# Poker System Class
class PokerSystem:
    def __init__(self, player: Player, opponent: PokerPlayer):
        self.tutorial_enabled = True
        self.deck = Deck(["default"], SUITS, RANKS)
        self.community_cards = CommunityCards()
        self.player = player
        self.opponent = opponent
        self.to_discard = 0
        self.pot_chips = 1251
        self.calculator = HandCalculator()
        self.victory_timer = 0

        self.state = {
            "round": RoundState.PRE_FLOP,
            "phase": PhaseState.DRAW
        }

        # Showdown bookkeeping (to only apply pot change once per showdown)
        self.showdown_applied = False

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == MOUSEBUTTONDOWN and self.state["phase"] in [
            PhaseState.DISCARD,
            PhaseState.FREEZE,
            PhaseState.HAND_SELECTION
        ]:
            selected = self.player.hand.get_selected_cards()
            self.player.hand.handle_click(event)

            if (
                self.state["phase"] == PhaseState.FREEZE
                and len(selected) == 1
                and len(self.player.hand.get_selected_cards()) != 0
            ):
                self.player.hand.select(self.player.hand.cards.index(selected[0]))

            elif self.state["phase"] == PhaseState.DISCARD and len(selected) >= self.to_discard:
                self.player.hand.select(self.player.hand.cards.index(selected[0]))

            elif (
                self.state["phase"] == PhaseState.HAND_SELECTION
                and len(selected) == 5
                and len(self.player.hand.get_selected_cards()) != 4
            ):
                self.player.hand.select(self.player.hand.cards.index(selected[0]))

        elif event.type == KEYDOWN:
            nums = [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]
            key = event.dict["key"]

            if key == K_RETURN:
                if self.state["phase"] == PhaseState.DISCARD:
                    selected_num = len(self.player.hand.get_selected_cards())

                    if selected_num <= self.to_discard:
                        self.to_discard -= selected_num
                        for card in self.player.hand.get_selected_cards():
                            if card.type != "Frozen":
                                self.discarded.append(card)

                        self.player.hand.discard_selected()

                    if self.to_discard == 0:
                        self.state["phase"] = PhaseState.NEXT_PHASE

                elif self.state["phase"] == PhaseState.FREEZE:
                    self.player.hand.freeze_selected()
                    self.state["phase"] = PhaseState.DISCARD

                    if self.state["round"] == RoundState.PRE_FLOP:
                        self.to_discard = max(self.player.hand.num_cards - 2, 0)

                    else:
                        self.to_discard = 2

                elif self.state["phase"] == PhaseState.HAND_SELECTION:
                    self.calculator.calculate_score(self.player.hand, self.community_cards)
                    self.state["phase"] = PhaseState.EVALUATION

                elif self.state["phase"] == PhaseState.DRAW and self.state["round"] != RoundState.PRE_FLOP:
                    self.state["phase"] = PhaseState.DRAWING

                    if self.state["round"] not in [RoundState.SHOWDOWN, RoundState.TURN]:
                        self.player.queue_draw(2)
                        self.opponent.queue_draw(2)

                    elif self.state["round"] == RoundState.TURN:
                        self.state["phase"] = PhaseState.NEXT_PHASE

                elif self.state["phase"] == PhaseState.SHOWDOWN:
                    # Next round
                    for card in self.player.hand.get_selected_cards():
                        card.highlighted = False

                    self.player.hand.discard_selected()
                    self.opponent.hand.discard_selected()


                    self.opponent.hand.hide_selected = True
                    self.state["phase"] = PhaseState.DRAW
                    self.state["round"] = RoundState.PRE_FLOP
                    self.community_cards.cards = []

                    for discarded in self.discarded:
                        self.deck.add_card(discarded)

            elif key in nums and self.state["phase"] in [
                PhaseState.DISCARD,
                PhaseState.FREEZE,
                PhaseState.HAND_SELECTION
            ]:
                index = nums.index(key)
                selected = self.player.hand.get_selected_cards()

                if index < len(self.player.hand.cards):
                    if self.player.hand.cards[index].selected:
                        pass

                    elif self.state["phase"] == PhaseState.FREEZE:
                        if self.player.hand.cards[index].type == "frozen":
                            return

                        elif len(selected) == 1 and len(self.player.hand.get_selected_cards()) != 0:
                            self.player.hand.select(self.player.hand.cards.index(selected[0]))

                    elif self.state["phase"] == PhaseState.DISCARD and len(selected) >= self.to_discard and len(selected) > 0:
                        self.player.hand.select(self.player.hand.cards.index(selected[0]))

                    elif (
                        self.state["phase"] == PhaseState.HAND_SELECTION
                        and len(selected) == 5
                        and len(self.player.hand.get_selected_cards()) != 4
                    ):
                        self.player.hand.select(self.player.hand.cards.index(selected[0]))

                    self.player.hand.select(index)

            elif key == K_UP:
                if self.state["phase"] == PhaseState.BET:
                    pass

            elif key == K_DOWN:
                if self.state["phase"] == PhaseState.BET:
                    pass

    # PRE-FLOP
    def update_preflop(self, delta_time: float) -> None:
        phase_state = self.state["phase"]

        if phase_state == PhaseState.DRAW:
            self.player.queue_draw(4)
            self.opponent.queue_draw(4)

            self.state["phase"] = PhaseState.DRAWING

        elif phase_state == PhaseState.DRAWING and self.player.cards_to_draw == 0:
            self.state["phase"] = PhaseState.FREEZE

        elif phase_state == PhaseState.NEXT_PHASE:
            for i in range(max(self.opponent.hand.num_cards - 2, 0)):
                self.opponent.hand.select_random()
                self.opponent.hand.discard_selected()

            for card in self.opponent.hand.get_selected_cards():
                if card.type != "Frozen":
                    self.discarded.append(card)

            self.state["phase"] = PhaseState.DRAW
            self.state["round"] = RoundState.FLOP

            for i in range(3):
                card = self.deck.draw_card()
                card.type = random.choice(
                    ["frozen", "default", "default", "default", "default", "default"]
                )
                self.community_cards.add(card)

    # FLOP / RIVER / TURN
    def update_round(self, delta_time: float) -> None:
        phase_state = self.state["phase"]
        round_state = self.state["round"]

        if phase_state == PhaseState.DRAWING and self.player.cards_to_draw == 0:
            self.state["phase"] = PhaseState.BET

        elif phase_state == PhaseState.BET:
            if random.random() > 0.5:
                self.opponent.hand.select_random()
                self.opponent.hand.freeze_selected()

            self.state["phase"] = PhaseState.FREEZE

        elif phase_state == PhaseState.NEXT_PHASE:
            self.opponent.hand.select_random()
            self.opponent.hand.select_random()
            for card in self.opponent.hand.get_selected_cards():
                if card.type != "Frozen":
                    self.discarded.append(card)

            self.opponent.hand.discard_selected()

            self.state["phase"] = PhaseState.DRAW

            if round_state == RoundState.FLOP:
                self.state["round"] = RoundState.RIVER

            elif round_state == RoundState.RIVER:
                self.state["round"] = RoundState.TURN

            elif round_state == RoundState.TURN:
                self.state["round"] = RoundState.SHOWDOWN
                self.state["phase"] = PhaseState.HAND_SELECTION

            card = self.deck.draw_card()
            card.type = random.choice(
                ["frozen", "default", "default", "default", "default", "default"]
            )
            self.community_cards.add(card)

    # SHOWDOWN
    def update_showdown(self, delta_time: float) -> None:
        phase_state = self.state["phase"]

        if phase_state == PhaseState.HAND_SELECTION:
            # Player chooses their best 5; score is calculated when they confirm (ENTER)
            self.calculator.calculate_score(self.player.hand, self.community_cards)
            # Ensure pot logic will re-run when we actually enter SHOWDOWN
            self.showdown_applied = False

        elif phase_state == PhaseState.EVALUATION:
            # Let the opponent auto-select their optimal hand
            for card in self.calculator.get_optimal_selections(
                self.opponent.hand, self.community_cards
            ):
                self.opponent.hand.select(self.opponent.hand.cards.index(card))

            self.calculator.calculate_score(self.opponent.hand, self.community_cards)
            self.state["phase"] = PhaseState.SHOWDOWN
            # Reset flag so SHOWDOWN can apply pot change once
            self.showdown_applied = False
            Sounds.get_sound("counter").play()

        elif phase_state == PhaseState.SHOWDOWN:
            # Reveal opponent’s selected cards
            self.opponent.hand.hide_selected = False

            # Apply pot logic exactly once per showdown
            if not self.showdown_applied:
                print(self.opponent.hand.value, self.player.hand.value)

                # Decrease pot by how much more value the player's hand has
                diff = self.player.hand.value - self.opponent.hand.value
                self.pot_chips = max(0, self.pot_chips - diff)

                self.showdown_applied = True

    def update(self, delta_time: float) -> None:
        round_state = self.state["round"]

        if self.pot_chips <= 0:
            self.victory_timer += delta_time

        self.player.update(self.deck, delta_time)
        self.opponent.update(self.deck, delta_time)
        self.community_cards.update(delta_time)

        if self.victory_timer > 0:
            return
        
        if round_state == RoundState.PRE_FLOP:
            self.update_preflop(delta_time)

        elif round_state == RoundState.FLOP:
            self.update_round(delta_time)

        elif round_state == RoundState.RIVER:
            self.update_round(delta_time)

        elif round_state == RoundState.TURN:
            self.update_round(delta_time)

        elif round_state == RoundState.SHOWDOWN:
            self.update_showdown(delta_time)