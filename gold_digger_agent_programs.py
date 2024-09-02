"""
gold_digger_agent_programs.py
"""

from playing_cards import Names
from legal_moves import get_legal_actions_gs
from deck import possible_cards, dead_ends
from logical_gold_digger import play_a_logical_card

# Get the current game state
def get_game_state(percepts):
    return {
        'game-board': percepts['game-board-sensor'],
        'player-turn': percepts['turn-taking-indicator'],
        'mining-state': percepts['can-mine-sensor'],
        'player-cards': percepts['cards-in-hand-sensor'],
        'reported-cards': percepts['reported-cards-sensor'],
        'cards-played': percepts['cards-played-sensor'],
        'deck-status': percepts['deck-status'],
        'known-cards': percepts['known-cards-sensor'],
        'flipped-cards': percepts['flipped-cards-sensor']
    }


# Creates a dictionary of all players and whether suspected of being a GoldDigger
def set_suspected_golddigger(player_index):
    suspected_golddigger = {}
    for i in range(8):
        suspected_golddigger[i] = False
    suspected_golddigger[player_index] = True
    return suspected_golddigger


# Creates a dictionary of all players and whether suspected of being a Saboteur
def set_suspected_saboteur():
    suspected_saboteur = {}
    for i in range(8):
        suspected_saboteur[i] = False
    return suspected_saboteur


# Creates a dictionary of all possible cards and the number of them and removes what has been played
def set_cards_unplayed(cards_played):
    cards_unplayed = possible_cards.copy()
    for key in cards_played:
        played = cards_played[key]
        for card in played:
            cards_unplayed[card] -= 1
    return cards_unplayed

# Attempt to deduce the gold diggers
def deduce_golddiggers(gold_idx, reported, suspected_golddigger):
    for i in range(8):
        if reported[i][0] == gold_idx and reported[i][1]:
            suspected_golddigger[i] = True
    return suspected_golddigger

# Attempt to deduce the saboteurs
def deduce_saboteurs(gold_idx, reported, suspected_saboteur):
    for i in range(8):
        if reported[i][0] == gold_idx and not reported[i][1]:
            suspected_saboteur[i] = True
        elif reported[i][0] != gold_idx and reported[i][1]:
            suspected_saboteur[i] = True
    return suspected_saboteur

# Attempt to deduce the location of the gold card using our known cards
def deduce_gold_loc(known_cards, goal_cards):
    gold_loc = None
    gold_idx = -1

    for i in range(3):
        if known_cards[i] is not None:
            if known_cards[i] is False:
                goal_cards[i] = None
            else:
                gold_loc = goal_cards[i]
                gold_idx = i

    if gold_loc is None:
        possibles = 0
        for loc in goal_cards:
            if loc is not None:
                possibles += 1
        if possibles == 1:
            for loc in goal_cards:
                if loc is not None:
                    gold_loc = loc
                    gold_idx = goal_cards.index(loc)

    return gold_loc, gold_idx

# Rule out goal cards based on suspected golddigger reports
def use_golddigger_reports(reported, suspected_golddigger, goal_cards):
    # If trusted GoldDigger reports a card as false, remove it.
    for i in range(8):
        if reported[i][0] is not None:
            if suspected_golddigger[i]:
                if not reported[i][1]:
                    for j in range(3):
                        if goal_cards[j] == reported[i][0]:
                            goal_cards[j] = None
    return goal_cards


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

    # Dictionaries of players and bools of whether suspected
    suspected_saboteur = set_suspected_saboteur()
    suspected_golddigger = set_suspected_golddigger(player)

    # List of all possible cards and removing what is on the board
    cards_unplayed = set_cards_unplayed(cards_played)

    # Dictionary of goal cards we have ruled out
    goal_cards = [(14,8), (14,10), (14,12)]
    gold_idx = -1
    for loc in goal_cards:
            if board[loc].name is not Names.GOAL:
                goal_cards[goal_cards.index(loc)] = None

    # Location of gold card
    gold_loc = None

    # Attempt to deduce gold location from known cards
    if gold_loc is None:
        gold_loc, gold_idx = deduce_gold_loc(known_cards, goal_cards)

    # Attempt to deduce saboteurs and golddiggers
    if gold_loc is not None:
        suspected_golddigger = deduce_golddiggers(gold_idx, reported, suspected_golddigger)
        suspected_saboteur = deduce_saboteurs(gold_idx, reported, suspected_saboteur)

    # Attempt to deduce gold location from reports and known player types
    if gold_loc is None:
        goal_cards = use_golddigger_reports(reported, suspected_golddigger, goal_cards)

    # Choose a logical action
    action = play_a_logical_card(legal_moves, cards, mining, suspected_golddigger, suspected_saboteur, board, gold_loc, goal_cards, flipped_cards)
    actions.append(action)

    return actions
