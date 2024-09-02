"""
gold_digger_agent_programs.py
"""

from playing_cards import Names
from legal_moves import get_legal_actions_gs
from deck import possible_cards, dead_ends
from logical_gold_digger import play_a_logical_card
from shared_agent_functions import setup_game_info, get_game_state, deduce_player_types, deduce_gold_loc, use_golddigger_reports
from game_board import GOAL_LOCATIONS


# Gold Digger Agent Program
def gold_digger_agent_program(percepts, actuators):
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
    flipped_cards = gs['flipped-cards']  # List of tuples (x, y)

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
    unplayed, suspected_saboteur, suspected_golddigger = setup_game_info(cards_played, None, player)

    # Dictionary of goal cards we have ruled out
    goal_cards = GOAL_LOCATIONS.copy()
    for loc in goal_cards:
        if board[loc].name is not Names.GOAL:
            goal_cards[goal_cards.index(loc)] = None

    # Attempt to deduce gold location from known cards
    gold_loc, gold_idx = deduce_gold_loc(known_cards, goal_cards)

    # Attempt to deduce saboteurs and golddiggers
    if gold_loc is not None:
        suspected_saboteur, suspected_golddigger = deduce_player_types(reported, suspected_saboteur, suspected_golddigger, gold_idx)
    else:
        # Attempt to deduce gold location from reports and known player types
        goal_cards = use_golddigger_reports(reported, suspected_golddigger, goal_cards)

    # Choose a logical action
    action = play_a_logical_card(legal_moves, cards, mining, suspected_golddigger, suspected_saboteur, board, gold_loc, goal_cards, flipped_cards)
    actions.append(action)

    return actions
