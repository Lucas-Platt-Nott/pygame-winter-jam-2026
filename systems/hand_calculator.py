from collections import Counter
from itertools import combinations

from config import *

class HandCalculator:
    def __init__(self):
        self.values = VALUES
        self.hand_values = HAND_DATA

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------
    def calculate_score(self, hand, community_cards):
        cards = hand.get_selected_cards() + community_cards.cards
        best_hand_name, best_hand_cards = self._evaluate_best_hand(cards)

        # -----------------------------------------------------
        # HIGHLIGHT CONTRIBUTING CARDS
        # -----------------------------------------------------
        contributing_set = set(best_hand_cards)

        for card in hand.cards + community_cards.cards:
            card.highlighted = card in contributing_set

        # -----------------------------------------------------
        # SCORE ONLY CONTRIBUTING CARDS
        # -----------------------------------------------------
        total_value = 0
        for card in best_hand_cards:
            if card.type == "default":
                total_value += self.values[card.rank]
            elif card.type == "frozen":
                total_value += self.values[card.rank] + 1

        multiplier = self.hand_values[best_hand_name]
        hand.value = total_value * multiplier
        hand.hand_type = best_hand_name
        return total_value * multiplier

    # ---------------------------------------------------------
    # AI: GET OPTIMAL SELECTIONS
    # ---------------------------------------------------------
    def get_optimal_selections(self, hand, community_cards):
        best_score = -1
        best_selection = []

        # Try all non-empty subsets of the hand
        for r in range(1, len(hand.cards) + 1):
            for subset in combinations(hand.cards, r):
                score = self._simulate_selection(subset, community_cards)
                if score > best_score:
                    best_score = score
                    best_selection = list(subset)

        return best_selection

    # ---------------------------------------------------------
    # INTERNAL: SIMULATE A SELECTION WITHOUT MODIFYING HAND
    # ---------------------------------------------------------
    def _simulate_selection(self, selected_cards, community_cards):
        cards = list(selected_cards) + community_cards.cards
        best_hand_name, best_hand_cards = self._evaluate_best_hand(cards)

        # Score only contributing cards
        total_value = 0
        for card in best_hand_cards:
            if card.type == "default":
                total_value += self.values[card.rank]
            elif card.type == "frozen":
                total_value += self.values[card.rank] + 1

        multiplier = self.hand_values[best_hand_name]
        return total_value * multiplier

    # ---------------------------------------------------------
    # HAND EVALUATION
    # ---------------------------------------------------------
    def _evaluate_best_hand(self, cards):
        best_rank = -1
        best_name = "high card"
        best_contributors = None

        for combo in combinations(cards, 5):
            name = self._classify_hand(combo)
            rank = self.hand_values[name]

            if rank > best_rank:
                best_rank = rank
                best_name = name
                best_contributors = self._extract_contributing_cards(name, combo)

        return best_name, best_contributors

    # ---------------------------------------------------------
    # EXTRACT CONTRIBUTING CARDS
    # ---------------------------------------------------------
    def _extract_contributing_cards(self, hand_name, cards):
        ranks = [c.rank for c in cards]
        rank_counts = Counter(ranks)

        # Four of a Kind
        if hand_name == "four of a kind":
            quad_rank = next(r for r, c in rank_counts.items() if c == 4)
            return [c for c in cards if c.rank == quad_rank]

        # Full House
        if hand_name == "full house":
            triple_rank = next(r for r, c in rank_counts.items() if c == 3)
            pair_rank = next(r for r, c in rank_counts.items() if c == 2)
            return [c for c in cards if c.rank in (triple_rank, pair_rank)]

        # Three of a Kind
        if hand_name == "three of a kind":
            triple_rank = next(r for r, c in rank_counts.items() if c == 3)
            return [c for c in cards if c.rank == triple_rank]

        # Two Pair
        if hand_name == "two pair":
            pair_ranks = [r for r, c in rank_counts.items() if c == 2]
            return [c for c in cards if c.rank in pair_ranks]

        # Pair
        if hand_name == "pair":
            pair_rank = next(r for r, c in rank_counts.items() if c == 2)
            return [c for c in cards if c.rank == pair_rank]

        # Straight / Flush / Straight Flush / Royal Flush
        if hand_name in ("straight", "flush", "straight flush", "royal flush"):
            return list(cards)

        # High Card
        if hand_name == "high card":
            return [max(cards, key=lambda c: self._rank_to_num(c.rank))]

        return list(cards)

    # ---------------------------------------------------------
    # CLASSIFY HAND
    # ---------------------------------------------------------
    def _classify_hand(self, cards):
        ranks = [c.rank for c in cards]
        suits = [c.suit for c in cards]

        numeric = sorted([self._rank_to_num(r) for r in ranks])
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        is_flush = max(suit_counts.values()) == 5
        is_straight = self._is_straight(numeric)

        if is_flush and numeric == [10, 11, 12, 13, 14]:
            return "royal flush"
        if is_flush and is_straight:
            return "straight flush"
        if 4 in rank_counts.values():
            return "four of a kind"
        if sorted(rank_counts.values()) == [2, 3]:
            return "full house"
        if is_flush:
            return "flush"
        if is_straight:
            return "straight"
        if 3 in rank_counts.values():
            return "three of a kind"
        if list(rank_counts.values()).count(2) == 2:
            return "two pair"
        if 2 in rank_counts.values():
            return "pair"
        return "high card"

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def _rank_to_num(self, r):
        if r == "A": return 14
        if r == "K": return 13
        if r == "Q": return 12
        if r == "J": return 11
        return int(r)

    def _is_straight(self, nums):
        if nums == [2, 3, 4, 5, 14]:
            return True
        return all(nums[i] + 1 == nums[i + 1] for i in range(4))
