"""
logical_gold_digger.py

Purpose: Chooses an action for a Gold Digger based on logical rules for the Agents goal
"""

import random

from shared import Names
from shared_agent_functions import assess_board
from deck import dead_ends

# Cards that are best to throw away
throwing_cards = [
    Names.TURN_RIGHT,
    Names.TURN_LEFT,
    Names.VERTICAL_PATH,
    Names.HORIZONTAL_PATH,
    Names.VERT_T,
    Names.HOR_T,
    Names.CROSS_SECTION,
]

# Cards that are best to play
best_cards_down = [
    Names.CROSS_SECTION,
    Names.HOR_T,
    Names.HORIZONTAL_PATH,
    Names.TURN_RIGHT,
    Names.VERT_T,
]

# Cards that are best to play rotated
best_cards_down_rotated = [
    Names.CROSS_SECTION,
    Names.HOR_T,
    Names.HORIZONTAL_PATH,
    Names.TURN_LEFT,
]


# If player suspected of being GoldDigger, and player is not mining, play mend on them
def mend_player(legal_moves, suspected_golddigger, mining):
    for p in range(8):
        if suspected_golddigger[p] and not mining[p]:
            for c in range(4):
                action = (f"mend-{0}-{p}-{c}")
                if action in legal_moves:
                    return action
    return None


# If player suspected of being Saboteur, we will play Sabotage on them
def sabotage_player(legal_moves, suspected_saboteur, mining):
    for p in range(8):
        if suspected_saboteur[p] and mining[p]:
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


# If the same row as the closest card has a dead end, dynamite it
def dynamite_on_dead_end(legal_moves, board, closest, x, y):
    if closest.name in dead_ends:
        for move in legal_moves:
            if move.startswith(f"dynamite-{x}-{y}"):
                return move
    # If dead end in the lowest row, blow it out.
    for move in legal_moves:
        for i in range(-3, 3):
            if y+i < 20 and y+i >= 0:
                if move.startswith(f"dynamite-{x}-{y+i}"):
                    if board[(x, y+i)].name in dead_ends:
                        return move
    return None

# If the target is down, attempt best moves, or any move down.
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
    for move in legal_moves:
        for i in range(-4, 4):
            if y+i < 20 and y+i >= 0:
                if move.startswith(f"place-{x}-{y+i}") or move.startswith(f"rotate-{x}-{y+i}"):
                    return move
    return None


# If card on lowest row is turn right and is in flipped card, dynamite
def dynamite_last_row(board, legal_moves, flipped_cards, x, y):
    for i in range(-4, 4):
        if y+i < 20 and y+i >= 0:
            card = board[(x, y+i)]
            if card is not None:
                if card.name == Names.TURN_RIGHT and (x, y+i) in flipped_cards:
                    for move in legal_moves:
                        if move.startswith(f"dynamite-{x}-{y+i}"):
                            return move
                # If card on lowest row is turn left and is NOT in flipped card, dynamite
                if card.name == Names.TURN_LEFT and (x, y+i) not in flipped_cards:
                    for move in legal_moves:
                        if move.startswith(f"dynamite-{x}-{y+i}"):
                            return move
    return None


# Find a move one row above the lowest row
def try_row_above_lowest(legal_moves, x, y):
    for move in legal_moves:
        for i in range(-4, 4):
            if y+i < 20 and y+i >= 0:
                if move.startswith(f"place-{x-1}-{y+i}") or move.startswith(f"rotate-{x-1}-{y+i}"):
                    return move
    return None


# If target is left, can we continue left?
def target_is_left(legal_moves, x, y, cards):
    for move in legal_moves:
        if move.startswith(f"place-{x}-{y-1}") or move.startswith(f"rotate-{x}-{y-1}"):
            for card in cards:
                if not card.name == Names.TURN_RIGHT:
                    return move
    return None


# If target is right, can we continue right?
def target_is_right(legal_moves, x, y, cards):
    for move in legal_moves:
        if move.startswith(f"place-{x}-{y+1}") or move.startswith(f"rotate-{x}-{y+1}"):
            for card in cards:
                if card.name == Names.TURN_LEFT:
                    return move
    return None


# If target is up, can we continue up?
def target_is_up(legal_moves, x, y, cards):
    for move in legal_moves:
        if move.startswith(f"place-{x-1}-{y}") or move.startswith(f"rotate-{x-1}-{y}"):
            for card in cards:
                if card.name == Names.CROSS_SECTION:
                    return move
    return None


# Play a cross-section around the closest card
def play_a_cross_section(legal_moves, cards, x, y):
    for move in legal_moves:
        if (move.startswith(f"place-{x+1}-{y}") or move.startswith(f"place-{x}-{y+1}")
                or move.startswith(f"rotate-{x}-{y-1}")):
            for card in cards:
                if card.name == Names.CROSS_SECTION:
                    return move
    return None


# Discard any dead end card
def discard_dead_end(legal_moves, cards):
    for move in legal_moves:
        if move.startswith("discard"):
            for card in cards:
                if card.name in dead_ends:
                    return move
    return None


# Just place a card anywhere
def place_any_card(legal_moves):
    for move in legal_moves:
        if move.startswith("place") or move.startswith("rotate"):
            return move
    return None


# Discard any card in throwing cards list
def discard_a_throwing_card(legal_moves, cards):
    for i in range(7):
        for j in range(len(cards)):
            if cards[j].name == throwing_cards[i]:
                return f"discard-0-0-{j}"
    return None


# Calculates at the absolute distance from each legal placement to the target card, returns closest
# Excludes dead-end cards
def play_closest_card_to_goal(legal_moves, target, cards):
    t_x = target[0]
    t_y = target[1]
    min_dist = 100
    best_move = None
    for move in legal_moves:
        if move.startswith("place") or move.startswith("rotate"):
            _, row_str, col_str, c_str = move.split('-')
            c = int(c_str)
            if cards[c].name in dead_ends:
                continue
            row = int(row_str)
            col = int(col_str)
            abs_dist = abs(row - t_x) + abs(col - t_y)
            if abs_dist < min_dist:
                min_dist = abs_dist
                best_move = move
    if best_move is not None:
        return best_move
    return None


def play_a_logical_card(legal_moves, cards, mining, suspected_golddigger, suspected_saboteur, board, gold_loc,
                        goal_cards, flipped_cards):

    # Mend, Sabotage, Map are priorities
    action = mend_player(legal_moves, suspected_golddigger, mining)
    if action is not None:
        return action
    action = sabotage_player(legal_moves, suspected_saboteur, mining)
    if action is not None:
        return action
    # If we have a Map card, play it. Could strongly help us find our enemies and allies
    if gold_loc is None:
        action = play_map_card(legal_moves, goal_cards)
        if action is not None:
            return action

    # Now we set up to choose a card to place down
    # Get the closest cell to center goal or gold card
    # Get the closest card to target and its (x, y) coordinates
    x, y, closest, target = assess_board(board, gold_loc, goal_cards)

    # Now we are looking for the best card to place down
    # If closest card to goal is dead end, play dynamite
    action = dynamite_on_dead_end(legal_moves, board, closest, x, y)
    if action is not None:
        return action

    # If target is down, play a card that goes down
    if x - target[0] < 0:
        action = target_is_down(legal_moves, x, y, cards)
        if action is not None:
            return action
    # If target is up
    elif x - target[0] > 0:
        action = target_is_up(legal_moves, x, y, cards)
        if action is not None:
            return action
    # If target is left
    elif y - target[1] > 0:
        action = target_is_left(legal_moves, x, y, cards)
        if action is not None:
            return action
    # If target is right
    elif y - target[1] < 0:
        action = target_is_right(legal_moves, x, y, cards)
        if action is not None:
            return action

    # If card on lowest row is pointing away from goal, dynamite
    action = dynamite_last_row(board, legal_moves, flipped_cards, x, y)
    if action is not None:
        return action

    # Check for move on row above the lowest
    if x - target[0] < 0:
        action = try_row_above_lowest(legal_moves, x, y)
        if action is not None:
            return action

    # Play a cross-section around the closest card
    action = play_a_cross_section(legal_moves, cards, x, y)
    if action is not None:
        return action

    # Throw away dead end cards
    action = discard_dead_end(legal_moves, cards)
    if action is not None:
        return action

    # If nothing found, play the absolute closest card we can (not a dead end)
    action = play_closest_card_to_goal(legal_moves, target, cards)
    if action is not None:
        return action

    # If no actions found, play any card
    action = place_any_card(legal_moves)
    if action is not None:
        return action

    # Discard any card in throwing cards
    action = discard_a_throwing_card(legal_moves, cards)
    if action is not None:
        return action

    # If no actions, play a random move
    action = random.choice(legal_moves)

    return action
