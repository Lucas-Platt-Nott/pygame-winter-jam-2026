# Built-In
import random
from enum import Enum, auto

# External
import pygame
from pygame.locals import *

# Internal
from config import *
from systems import PokerPlayer, Player, Deck, CommunityCards

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

        self.state = {
            "round": RoundState.PRE_FLOP,
            "phase": PhaseState.DRAW
        }

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == MOUSEBUTTONDOWN and self.state["phase"] in [PhaseState.DISCARD, PhaseState.FREEZE]:
            self.player.hand.handle_click(event)

        elif event.type == KEYDOWN:
            nums = [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]
            key = event.dict["key"]

            if key == K_RETURN:
                if self.state["phase"] == PhaseState.DISCARD:
                    self.player.hand.discard_selected()

                    if self.player.hand.num_cards <= 2:
                        self.state["phase"] = PhaseState.NEXT_PHASE

                elif self.state["phase"] == PhaseState.FREEZE:
                    self.player.hand.freeze_selected()
                    self.state["phase"] = PhaseState.DISCARD

                elif self.state["phase"] == PhaseState.DRAW and self.state["round"] != RoundState.PRE_FLOP:
                    self.state["phase"] = PhaseState.DRAWING

                    if self.state["round"] != RoundState.SHOWDOWN:
                        self.player.queue_draw(2)
                        self.opponent.queue_draw(2)

            elif key in nums and self.state["phase"] in [PhaseState.DISCARD, PhaseState.FREEZE]:
                index = nums.index(key)

                if index < len(self.player.hand.cards):
                    self.player.hand.select(index)

    # PRE-FLOP
    def update_preflop(self, delta_time: float) -> None:
        phase_state = self.state["phase"]

        if phase_state == PhaseState.DRAW:
            self.player.queue_draw(5)
            self.opponent.queue_draw(5)

            self.state["phase"] = PhaseState.DRAWING

        elif phase_state == PhaseState.DRAWING and self.player.cards_to_draw == 0:
            self.state["phase"] = PhaseState.DISCARD

        elif phase_state == PhaseState.NEXT_PHASE:
            self.opponent.hand.select_random()
            self.opponent.hand.select_random()
            self.opponent.hand.select_random()
            self.opponent.hand.discard_selected()

            self.state["phase"] = PhaseState.DRAW
            self.state["round"] = RoundState.FLOP

            for i in range(3):
                self.community_cards.add(self.deck.draw_card())

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
            while self.opponent.hand.num_cards > 2:
                self.opponent.hand.select_random()
                self.opponent.hand.discard_selected()
                
            self.state["phase"] = PhaseState.DRAW

            if round_state == RoundState.FLOP:
                self.state["round"] = RoundState.RIVER

            elif round_state == RoundState.RIVER:
                self.state["round"] = RoundState.TURN

            elif round_state == RoundState.TURN:
                self.state["round"] = RoundState.SHOWDOWN
                self.state["phase"] = PhaseState.HAND_SELECTION

            self.community_cards.add(self.deck.draw_card())

    # SHOWDOWN
    def update_showdown(self, delta_time: float) -> None:
        phase_state = self.state["phase"]

        if phase_state == PhaseState.HAND_SELECTION:
            pass
        
        elif phase_state == PhaseState.EVALUATION:
            pass

        elif phase_state == PhaseState.SHOWDOWN:
            pass
        
    def update(self, delta_time: float) -> None:
        round_state = self.state["round"]
        print(round_state)

        self.player.update(self.deck, delta_time)
        self.opponent.update(self.deck, delta_time)
        self.community_cards.update(delta_time)

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