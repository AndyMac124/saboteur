"""
logical_saboteur.py

Purpose: Chooses an action for a Saboteur based on logical rules for the Agents goal
"""

import random

from shared import Names
from deck import dead_ends


throwing_cards = [
    Names.CROSS_SECTION,
    Names.HOR_T,
    Names.HORIZONTAL_PATH,
    Names.VERT_T,
    Names.TURN_LEFT,
    Names.TURN_RIGHT,
    Names.VERTICAL_PATH
]

best_cards_down = [
    Names.DE_ALL,
    Names.DE_N,
    Names.DE_WN,
    Names.DE_3_E,
    Names.DE_3_S,
    Names.TURN_LEFT,
    Names.VERTICAL_PATH,
]

best_cards_down_rotated = [
    Names.DE_ALL,
    Names.DE_3_E,
    Names.DE_3_S,
    Names.DE_WS,
    Names.VERT_T,
]


# If player suspected of being GoldDigger, and player is not mining, play mend on them
def mend_player(legal_moves, suspected_saboteur, mining):
    for p in range(8):
        if suspected_saboteur[p] and not mining[p]:
            for c in range(4):
                action = (f"mend-{0}-{p}-{c}")
                if action in legal_moves:
                    return action
    return None


# If player suspected of being Saboteur, we will play Sabotage on them
def sabotage_player(legal_moves, suspected_golddigger, mining):
    for p in range(8):
        if suspected_golddigger[p] and mining[p]:
            for c in range(4):
                action = (f"sabotage-{0}-{p}-{c}")
                if action in legal_moves:
                    return action
    return None


# Will play a map card if the goal card hasn't been set to None
# (We set to None if we have previously peaked at it, or it's been flipped over)
def play_map_card(legal_moves, goal_cards):
    for i in range(3):
        if goal_cards[i] is not None:
            for j in range(4):
                for move in legal_moves:
                    if move == f"map-0-{i}-{j}":
                        return move
    return None


# If closest card is not a dead end, dynamite it.
def dynamite_dead_end(legal_moves, x, y):
    for move in legal_moves:
        if move.startswith(f"dynamite-{x}-{y}"):
            return move
    return None


def target_is_down(legal_moves, x, y, cards):
    for move in legal_moves:
        index = move[-1]
        ind = int(index)
        c = cards[ind]
        if c.name in best_cards_down:
            for i in range(-4, 4):
                if y+i < 20 and y+i >= 0:
                    if move.startswith(f"place-{x+1}-{y+i}"):
                        return move
        elif c.name in best_cards_down_rotated:
            for i in range(-4, 4):
                if y+i < 20 and y+i >= 0:
                    if move.startswith(f"rotate-{x+1}-{y+i}"):
                        return move
    return None


# If Cross section below start card, dynamite it
def dynamite_cross_sections(legal_moves, x, y, board, target, cards):
    start_row = 6
    start_col = 10
    for i in range(3):
        if board[(start_row, start_col+i)] is not None:
            if board[(start_row, start_col+i)].name is Names.CROSS_SECTION:
                for move in legal_moves:
                    if move.startswith(f"dynamite-6-{10+i}"):
                        return move
    return None


# Place a card across the lowest row
def place_across_lowest_row(legal_moves, x, y):
    for move in legal_moves:
        for i in range(-4, 4):
            if y+i < 20 and y+i >= 0:
                if move.startswith(f"place-{x}-{y+i}") or move.startswith(f"rotate-{x}-{y+i}"):
                    return move


# Discard any card in throwing_cards list
def discard_card(cards):
    for i in range(7):
        for j in range(len(cards)):
            if cards[j].name == throwing_cards[i]:
                return f"discard-0-0-{j}"
    return None


# Logical rules for saboteur agent
def play_a_logical_card(legal_moves, cards, mining, suspected_golddigger, suspected_saboteur, board, gold_loc,
                        goal_cards, x, y, closest, target):

    # Mend, Sabotage, Map are priorities
    action = mend_player(legal_moves, suspected_saboteur, mining)
    if action is not None:
        return action
    action = sabotage_player(legal_moves, suspected_golddigger, mining)
    if action is not None:
        return action
    if gold_loc is None:
        action = play_map_card(legal_moves, goal_cards)
        if action is not None:
            return action

    # If closest card is not a dead end, dynamite it.
    if closest.name not in dead_ends:
        action = dynamite_dead_end(legal_moves, x, y)
        if action is not None:
            return action

    # If target is down, play a card that goes up or blocks the path
    if x - target[0] < 0:
        action = target_is_down(legal_moves, x, y, cards)
        if action is not None:
            return action

    # If a cross-section is below the start card, dynamite it
    action = dynamite_cross_sections(legal_moves, x, y, board, target, cards)
    if action is not None:
        return action

    # If target is down, play any card across the lowest row
    if x - target[0] < 0:
        action = place_across_lowest_row(legal_moves, x, y)
        if action is not None:
            return action

    # Discard a throwable card
    action = discard_card(cards)
    if action is not None:
        return action

    action = random.choice(legal_moves)
    return action
