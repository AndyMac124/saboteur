"""
saboteur_agent_programs.py
"""

import random

from playing_cards import Names
from legal_moves import get_legal_actions_gs
from deck import possible_cards, dead_ends
from logical_saboteur import play_a_logical_card
from deceptive_saboteur import play_deceptively
from shared_agent_functions import setup_game_info, get_game_state, deduce_player_types, deduce_gold_loc, use_golddigger_reports, assess_board
from game_board import GOAL_LOCATIONS

# List of cards a gold digger would play, saboteurs would throw these out.
def update_golddiggers(suspected_golddigger, cards_played, player):
    bad_cards = [Names.HORIZONTAL_PATH, Names.CROSS_SECTION, Names.HOR_T]
    for p in range(8):
        if p != player and len(cards_played[p]) > 0:
            for i in range(len(cards_played[p])):
                if cards_played[p][i].name in bad_cards:
                    suspected_golddigger[p] = True
    return suspected_golddigger


def saboteur_agent_program(percepts, actuators):
    actions = []

    # Get game state and set variables
    gs = get_game_state(percepts)
    board = gs['game-board']  # Key is (x, y), value is TableCard
    cards = gs['player-cards']  # List of TableCard
    player = gs['player-turn']  # Int
    mining = gs['mining-state']  # List of Bool
    reported = gs['reported-cards']  # Dict of player_id and  tuple (goal_index, bool)
    cards_played = gs['cards-played']  # Dict of player_id and list of cards played
    deck_is_empty = gs['deck-status']  # Bool (isEmpty)
    known_cards = gs['known-cards']  # List of list of bools
    flipped_cards = gs['flipped-cards']

    # Get all legal moves
    legal_moves = get_legal_actions_gs(board, mining[player], cards, flipped_cards)

    # If no cards or no legal moves, we pass
    if len(cards) == 0 or len(legal_moves) == 0:
        move = f"pass-0-0-0"
        actions.append(move)
        return actions

    # List of all possible cards and removing what is on the board
    # Dictionary of players and suspected saboteur
    # Dictionary of players and suspected gold digger
    unplayed, suspected_saboteur, suspected_golddigger = setup_game_info(cards_played, player, None)

    # Update suspected gold diggers based on cards played
    suspected_golddigger = update_golddiggers(suspected_golddigger, cards_played, player)

    # Dictionary of goal cards we have ruled out
    goal_cards = GOAL_LOCATIONS.copy()
    for loc in goal_cards:
        if board[loc].name is not Names.GOAL:
            goal_cards[goal_cards.index(loc)] = None

    # Attempt to deduce gold location from known cards
    gold_loc, gold_idx = deduce_gold_loc(known_cards, goal_cards)

    # Attempt to deduce saboteurs and golddiggers using known gold location
    if gold_loc is not None:
        suspected_saboteur, suspected_golddigger = deduce_player_types(reported, suspected_saboteur, suspected_golddigger, gold_idx)
    else:
        # Attempt to deduce gold location from reports and known player types
        goal_cards = use_golddigger_reports(reported, suspected_golddigger, goal_cards)

    x, y, closest, target = assess_board(board, gold_loc, goal_cards)
    print(f"{x}, {y}, {target}")
    if x - target[0] < -2:
        print("Playing deceptively")
        # Choose a deceptive action (They aren't close to the goal cards yet)
        action = play_deceptively(legal_moves, cards, mining, suspected_golddigger, suspected_saboteur, board, gold_loc, goal_cards, x, y, closest, target)
        actions.append(action)
        return actions

    print("playing logically")
    # Choose a logical action (They are close to the goal cards)
    action = play_a_logical_card(legal_moves, cards, mining, suspected_golddigger, suspected_saboteur, board, gold_loc, goal_cards, x, y, closest, target)
    actions.append(action)
    return actions
