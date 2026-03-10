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

# Poker System Class
class PokerSystem:
    def __init__(self, player: Player, opponent: PokerPlayer):
        self.deck = Deck(["default"], SUITS, RANKS)
        self.community_cards = CommunityCards()
        self.player = player
        self.opponent = opponent

        self.state = {
            "round": RoundState.PRE_FLOP,
            "phase": PhaseState.DRAW
        }

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == MOUSEBUTTONDOWN and self.state["phase"] == PhaseState.DISCARD:
            self.player.hand.handle_click(event)

        elif event.type == KEYDOWN:
            key = event.dict["key"]

            # PLACEHOLDER DISCARD LOGIC BEFORE UI IS IMPLEMENTED
            if key == K_RETURN:
                self.player.hand.discard_selected()

                if self.player.hand.num_cards <= 2:
                    self.state["phase"] = PhaseState.NEXT_PHASE

            elif key == K_0:
                self.community_cards.add(self.deck.draw_card())

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
            
    # FLOP / RIVER / TURN
    def update_round(self, delta_time: float) -> None:
        phase_state = self.state["phase"]
        round_state = self.state["round"]

        n = 3 if round_state == RoundState.FLOP else 1

        if phase_state == PhaseState.DRAW:
            for i in range(n):
                self.community_cards.add(self.deck.draw_card())

            self.player.queue_draw(2)
            self.opponent.queue_draw(2)

            self.state["phase"] = PhaseState.DRAWING

        elif phase_state == PhaseState.DRAWING and self.player.cards_to_draw == 0:
            self.state["phase"] = PhaseState.BET

        elif phase_state == PhaseState.BET:
            self.state["phase"] = PhaseState.DISCARD
            
        elif phase_state == PhaseState.NEXT_PHASE:
            self.opponent.hand.select_random()
            self.opponent.hand.discard_selected()
            self.state["phase"] = PhaseState.DRAW

            if round_state == RoundState.FLOP:
                self.state["round"] = RoundState.RIVER

            elif round_state == RoundState.RIVER:
                self.state["round"] = RoundState.TURN

            elif round_state == RoundState.TURN:
                self.state["round"] = RoundState.SHOWDOWN

            print(round_state)

    # SHOWDOWN
    def update_showdown(self, delta_time: float) -> None:
        phase_state = self.state["phase"]

    def update(self, delta_time: float) -> None:
        round_state = self.state["round"]

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