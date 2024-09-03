"""
saboteur_agent_programs.py

Purpose: Executes the think component of the play step when the players turn is of type saboteur_agent_program.
"""


from shared import Names
from legal_moves import get_legal_actions_gs
from logical_saboteur import play_a_logical_card
from deceptive_saboteur import play_deceptively
from shared_agent_functions import (setup_game_info, get_game_state, deduce_player_types, deduce_gold_loc,
                                    use_gold_digger_reports, assess_board)
from game_board import GOAL_LOCATIONS
from shared import DEBUG


# List of cards a gold digger would play, saboteurs would throw these out.
def update_golddiggers(suspected_gold_digger, cards_played, player):
    bad_cards = [Names.HORIZONTAL_PATH, Names.CROSS_SECTION, Names.HOR_T]
    for p in range(8):
        if p != player and len(cards_played[p]) > 0:
            for i in range(len(cards_played[p])):
                if cards_played[p][i].name in bad_cards:
                    suspected_gold_digger[p] = True
    return suspected_gold_digger


def saboteur_agent_program(percepts, actuators):
    actions = []

    # Get game state and set variables
    gs = get_game_state(percepts)
    board = gs['game-board']  # Key is (x, y), value is TableCard
    cards = gs['player-cards']  # List of TableCard
    player = gs['player-turn']  # Int
    mining = gs['mining-state']  # List of Bool
    reported = gs['reported-cards']  # Dict of player_id and tuple (goal_index, bool)
    cards_played = gs['cards-played']  # Dict of player_id and list of cards played
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
    not_played, suspected_saboteur, suspected_gold_digger = setup_game_info(cards_played, player, None)

    # Update suspected gold diggers based on cards played
    suspected_gold_digger = update_golddiggers(suspected_gold_digger, cards_played, player)

    # Dictionary of goal cards we have ruled out
    goal_cards = GOAL_LOCATIONS.copy()
    for loc in goal_cards:
        if board[loc].name is not Names.GOAL:
            goal_cards[goal_cards.index(loc)] = None

    # Attempt to deduce gold location from known cards
    gold_loc, gold_idx = deduce_gold_loc(known_cards, goal_cards)

    # Attempt to deduce saboteurs and gold diggers using known gold location
    if gold_loc is not None:
        suspected_saboteur, suspected_gold_digger = deduce_player_types(reported, suspected_saboteur,
                                                                        suspected_gold_digger, gold_idx)
    else:
        # Attempt to deduce gold location from reports and known player types
        goal_cards = use_gold_digger_reports(reported, suspected_gold_digger, goal_cards)

    x, y, closest, target = assess_board(board, gold_loc, goal_cards)

    if x - target[0] < -3:
        if DEBUG:
            print("Saboteur Agent playing deceptively")
        # Choose a deceptive action (They aren't close to the goal cards yet)
        action = play_deceptively(legal_moves, cards, mining, suspected_gold_digger, suspected_saboteur, board, x, y,
                                  target)
        actions.append(action)
        return actions

    if DEBUG:
        print("Saboteur Agent playing logically")
    # Choose a logical action (They are close to the goal cards)
    action = play_a_logical_card(legal_moves, cards, mining, suspected_gold_digger, suspected_saboteur, board,
                                 gold_loc, goal_cards, x, y, closest, target)
    actions.append(action)
    return actions
