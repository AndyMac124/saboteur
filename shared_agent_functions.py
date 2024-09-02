"""
shared_agent_functions.py

Shared functions between Gold Digger and Saboteur Agents
"""

from deck import possible_cards

def setup_game_info(cards_played, saboteur, golddigger):

    def set_suspected_saboteur(player):
        suspected_saboteur = {}
        for i in range(8):
            suspected_saboteur[i] = False
        if player is not None:
            suspected_saboteur[player] = True
        return suspected_saboteur


    def set_suspected_golddigger(player):
        suspected_golddigger = {}
        for i in range(8):
            suspected_golddigger[i] = False
        if player is not None:
            suspected_golddigger[player] = True
        return suspected_golddigger


    # Creates a dictionary of all possible cards and the number of them and removes what has been played
    def set_cards_unplayed(cards_played):
        cards_unplayed = possible_cards.copy()
        for key in cards_played:
            played = cards_played[key]
            for card in played:
                cards_unplayed[card] -= 1
        return cards_unplayed

    saboteurs = set_suspected_saboteur(saboteur)
    golddiggers = set_suspected_golddigger(golddigger)
    unplayed = set_cards_unplayed(cards_played)

    return unplayed, saboteurs, golddiggers

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


def deduce_player_types(reported, suspected_saboteur, suspected_golddigger, gold_idx):
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

    saboteurs = deduce_saboteurs(gold_idx, reported, suspected_saboteur)
    golddiggers = deduce_golddiggers(gold_idx, reported, suspected_golddigger)
    return saboteurs, golddiggers

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