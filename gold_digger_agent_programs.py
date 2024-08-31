import random

from playing_cards import Names
from saboteur_game_environment import SaboteurGameEnvironment as se

possible_cards = {
    Names.MAP: 9,
    Names.SABOTAGE: 9,
    Names.MEND: 9,
    Names.DYNAMITE: 3,
    Names.CROSS_SECTION: 5,
    Names.VERTICAL_PATH: 4,
    Names.HORIZONTAL_PATH: 3,
    Names.TURN_LEFT: 4,
    Names.TURN_RIGHT: 5,
    Names.VERT_T: 5,
    Names.HOR_T: 5,
    Names.DE_ALL: 1,
    Names.DE_3_E: 1,
    Names.DE_3_S: 1,
    Names.DE_EW: 1,
    Names.DE_N: 1,
    Names.DE_NS: 1,
    Names.DE_WN: 1,
    Names.DE_WS: 1,
    Names.DE_W: 1,
}

def gold_digger_agent_program(percepts, actuators):
    global possible_cards

    actions = []

    card_ranks = [
        Names.CROSS_SECTION,
        Names.HOR_T,
        Names.VERT_T,
        Names.HORIZONTAL_PATH,
        Names.VERTICAL_PATH,
        Names.TURN_LEFT,
        Names.TURN_RIGHT,
    ]

    dead_ends = [Names.DE_ALL, Names.DE_3_E, Names.DE_3_S, Names.DE_EW, Names.DE_N, Names.DE_NS, Names.DE_WN, Names.DE_WS, Names.DE_W]

    gs = {
        'game-board': percepts['game-board-sensor'],
        'player-turn': percepts['turn-taking-indicator'],
        'mining-state': percepts['can-mine-sensor'],
        'player-cards': percepts['cards-in-hand-sensor'],
        'reported-cards': percepts['reported-cards-sensor'],
        'cards-played': percepts['cards-played-sensor'],
        'deck-status': percepts['deck-status'],
        'flipped-cards': percepts['flipped-cards-sensor']
    }

    board = gs['game-board']  # Key is (x, y), value is TableCard
    cards = gs['player-cards']  # List of TableCard
    player = gs['player-turn']  # Int
    mining = gs['mining-state']  # List of Bool
    reported = gs['reported-cards']  # Dict of player_id and  tuple (goal_index, bool)
    cards_played = gs['cards-played']  # Dict of player_id and list of cards played
    deck_is_empty = gs['deck-status']  # Bool (isEmpty)
    legal_moves = se.get_legal_actions_gs(gs)

    if len(cards) == 0 or len(legal_moves) == 0:
        move = ('pass', 0, 0, 0)
        actions.append(move)
        return actions

    # Dictionary of players and suspected saboteur
    suspected_saboteur = {}
    for i in range(8):
        suspected_saboteur[i] = False

    suspected_golddigger = {}
    for i in range(8):
        suspected_golddigger[i] = False
        suspected_golddigger[player] = True

    # List of all possible cards, remove what is on the board
    cards_unplayed = possible_cards.copy()
    for key in cards_played:
        played = cards_played[key]
        for card in played:
            cards_unplayed[card] -= 1

    # Dictionary of goal cards we have ruled out
    goal_cards = [(14,8), (14,10), (14,12)]

    # Location of gold card
    gold_loc = None

    # If we know the gold position and another player has reported it as true
    # They are likely a GoldDigger
    if gold_loc is not None:
        for i in range(8):
            if reported[i][0] == gold_loc and reported[i][1]:
                suspected_golddigger[i] = True

    # If we know the gold position and another player has reported it as false
    if gold_loc is not None:
        for i in range(8):
            if reported[i][0] == gold_loc and not reported[i][1]:
                suspected_saboteur[i] = True
            elif reported[i][0] != gold_loc and reported[i][1]:
                suspected_saboteur[i] = True

    # If trusted GoldDigger reports a card as false, remove it.
    if gold_loc is None:
        for i in range(8):
            if reported[i][0] is not None:
                if suspected_golddigger[i]:
                    if not reported[i][1]:
                        for j in range(3):
                            if goal_cards[j] == reported[i][0]:
                                goal_cards[j] = None

    # If player suspected of being GoldDigger, and player is not mining, play mend on them
    for p in range(8):
        if suspected_golddigger[p] and not mining[p]:
            for c in range(4):
                action = (f"mend-{0}-{p}-{c}")
                if action in legal_moves:
                    actions.append(action)
                    print(f"ACTION: {action}")
                    return actions

    # If player suspected of being Saboteur, we will play Sabotage on them
    for p in range(8):
        if suspected_saboteur[p]:
            for c in range(4):
                action = (f"sabotage-{0}-{p}-{c}")
                if action in legal_moves:
                    actions.append(action)
                    print(f"ACTION: {action}")
                    return actions

    # If we have a Map card, play it. Could strongly help us find our enemies and allies
    if gold_loc is None:
        for i in range(3):
            if goal_cards[i] is not None:
                for j in range(4):
                    for move in legal_moves:# Assuming the wildcard can be any value from 0 to 3
                        if move == f"map-0-{i}-{j}":
                            actions.append(move)
                            print(f"ACTION: {move}")
                            return actions

    # Get the closest cell to center goal or gold card
    goal_card = gold_loc if gold_loc is not None else goal_cards[1]
    closest_card = None
    target = (14, 10) if gold_loc is None else gold_loc
    for cell in board:
        #if str(board[cell]) == 'NONE' and str(board[cell]) not in [str(Names.GOAL), str(Names.GOLD)]:
        if board[cell] is not None and board[cell].name != Names.GOAL and board[cell].name != Names.GOLD:
            if closest_card is None:
                closest_card = cell
            else:
                if abs(cell[0] - target[0]) + abs(cell[1] - target[1]) < abs(closest_card[0] - target[0]) + abs(closest_card[1] - target[1]):
                    closest_card = cell

    # If closest card to goal is dead end, play dynamite
    x = closest_card[0]
    y = closest_card[1]
    closest = board[closest_card]
    if closest.name in dead_ends:
        print("Closest card is dead end")
        for move in legal_moves:
            if move.startswith(f"dynamite-{x}-{y}"):
                actions.append(move)
                print(f"ACTION: {move}")
                return actions

    print(f"Closest card to goal: {closest_card} and {x-target[0]}")

    if x - target[0] < 0:
        print("TARGET IS DOWN")
        for move in legal_moves:
            if move.startswith(f"place-{x}-{y+1}"):
                for card in cards:
                    if card == Names.CROSS_SECTION:
                        actions.append(move)
                        print(f"ACTION: {move}")
                        return actions
                    if card == Names.VERTICAL_PATH:
                        actions.append(move)
                        print(f"ACTION: {move}")
                        return actions
                    if card == Names.HOR_T:
                        actions.append(move)
                        print(f"ACTION: {move}")
                        return actions
                    else:
                        actions.append(move)
                        print(f"ACTION: {move}")
                        return actions
    elif x - target[0] > 0:
        # Go up
        for move in legal_moves:
            if move.startswith(f"place-{x}-{y-1}"):
                for card in cards:
                    if card == Names.CROSS_SECTION:
                        actions.append(move)
                        print(f"ACTION: {move}")
                        return actions
    elif y - target[1] < 0:
        # Go right
        for move in legal_moves:
            if move.startswith(f"place-{x+1}-{y}"):
                for card in cards:
                    if card == Names.TURN_LEFT:
                        actions.append(move)
                        print(f"ACTION: {move}")
                        return actions
    elif y - target[1] > 0:
        # Go left
        for move in legal_moves:
            if move.startswith(f"place-{x-1}-{y}"):
                for card in cards:
                    if not card == Names.TURN_RIGHT:
                        actions.append(move)
                        print(f"ACTION: {action}")
                        return actions


    # Play the closest path card to the goal row prioritising higher ranked cards
    for move in legal_moves:
        if move.startswith(f"place-{x}-{y}"):
            for card in cards:
                if card == Names.CROSS_SECTION:
                    actions.append(move)
                    print(f"ACTION: {action}")
                    return actions

    print("Throwing Dead end")
    # Throw away dead end cards
    for move in legal_moves:
        if move.startswith("discard"):
            for card in cards:
                if card in dead_ends:
                    actions.append(move)
                    return actions

    print("No actions found")
    actions.append(random.choice(legal_moves))

    return actions