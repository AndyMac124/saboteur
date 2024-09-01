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

def saboteur_agent_program(percepts, actuators):
    global possible_cards

    actions = []

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

    dead_ends = [Names.DE_ALL, Names.DE_3_E, Names.DE_3_S, Names.DE_EW, Names.DE_N, Names.DE_NS, Names.DE_WN, Names.DE_WS, Names.DE_W]

    gs = {
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

    board = gs['game-board']  # Key is (x, y), value is TableCard
    cards = gs['player-cards']  # List of TableCard
    player = gs['player-turn']  # Int
    mining = gs['mining-state']  # List of Bool
    reported = gs['reported-cards']  # Dict of player_id and  tuple (goal_index, bool)
    cards_played = gs['cards-played']  # Dict of player_id and list of cards played
    deck_is_empty = gs['deck-status']  # Bool (isEmpty)
    known_cards = gs['known-cards']  # List of list of bools
    legal_moves = se.get_legal_actions_gs(gs)

    #print(f"REPORTED CARDS: {reported}")

    if len(cards) == 0 or len(legal_moves) == 0:
        move = f"pass-0-0-0"
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
    gold_idx = -1
    for loc in goal_cards:
        if board[loc].name is not Names.GOAL:
            goal_cards[goal_cards.index(loc)] = None

    # Location of gold card
    gold_loc = None

    for i in range(3):
        if known_cards[i] is not None:
            if known_cards[i] is False:
                goal_cards[i] = None
            else:
                gold_loc = goal_cards[i]
                gold_idx = i
                #print(f" GOLD LOC = {gold_loc}")

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
                    #print(f" GOLD LOC = {gold_loc}")

    # If we know the gold position and another player has reported it as true
    # They are likely a GoldDigger
    if gold_loc is not None:
        for i in range(8):
            if reported[i][0] == gold_idx and reported[i][1]:
                suspected_golddigger[i] = True

    # If we know the gold position and another player has reported it as false
    if gold_loc is not None:
        for i in range(8):
            if reported[i][0] == gold_idx and not reported[i][1]:
                suspected_saboteur[i] = True
            elif reported[i][0] != gold_idx and reported[i][1]:
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

    #print(f"Goal Cards: {goal_cards}")

    # If player suspected of being GoldDigger, and player is mining, play sabotage on them
    for p in range(8):
        if suspected_golddigger[p] and mining[p]:
            for c in range(4):
                action = (f"sabotage-{0}-{p}-{c}")
                if action in legal_moves:
                    actions.append(action)
                    #print(f"ACTION: {action}")
                    return actions

    # If player suspected of being Saboteur, and player not mining, mend them
    for p in range(8):
        if suspected_saboteur[p] and not mining[p]:
            for c in range(4):
                action = (f"mend-{0}-{p}-{c}")
                if action in legal_moves:
                    actions.append(action)
                    #print(f"ACTION: {action}")
                    return actions

    #print(f"SUSPECTED SABOTEUR: {suspected_saboteur}")
    #print(f"SUSPECTED GOLDDIGGER: {suspected_golddigger}")
    # If we have a Map card, play it. Could strongly help us find our enemies and allies
    if gold_loc is None:
        for i in range(3):
            if goal_cards[i] is not None:
                for j in range(4):
                    for move in legal_moves:
                        if move == f"map-1-{i}-{j}":
                            actions.append(move)
                            #print(f"ACTION: {move}")
                            return actions

    # Get the closest cell to center goal or gold card
    closest_card = None
    target = None if gold_loc is None else gold_loc
    if target is None:
        if goal_cards[1] is not None:
            target = goal_cards[1]
        elif goal_cards[0] is not None:
            target = goal_cards[0]
        elif goal_cards[2] is not None:
            target = goal_cards[2]

    for cell in board:
        #if str(board[cell]) == 'NONE' and str(board[cell]) not in [str(Names.GOAL), str(Names.GOLD)]:
        if board[cell] is not None and board[cell].name != Names.GOAL and board[cell].name != Names.GOLD:
            if closest_card is None:
                closest_card = cell
            else:
                if abs(cell[0] - target[0]) < abs(closest_card[0] - target[0]):
                    closest_card = cell
                if cell[0] == target[0]:
                    if abs(cell[1] - target[1]) <= abs(closest_card[1] - target[1]):
                        closest_card = cell

    # If closest card to goal is dead end, play dynamite
    x = closest_card[0]
    y = closest_card[1]
    closest = board[closest_card]
    #print(f"Closest card to goal: {closest.name} with {target[0]} and {target[1]}")
    #print(legal_moves)

    # startCard = board[(6, 10)]
    # if startCard.name is Names.START:
    # for card in cards: card.name is Names.CROSS_SECTION

    if x - target[0] < 0:
        #print("TARGET IS DOWN")
        #print(f"CHECKING FOR: place-{x+1}")
        for move in legal_moves:
            index = move[-1]
            ind = int(index)
            c = cards[ind]
            if c.name in best_cards_down:
                for i in range(-4, 4):
                    if y+i < 20 and y+i >= 0:
                        if move.startswith(f"place-{x+1}-{y+i}"):
                            actions.append(move)
                            #print(f"ACTION: {move}")
                            return actions
            elif c.name in best_cards_down_rotated:
                for i in range(-4, 4):
                    if y+i < 20 and y+i >= 0:
                        if move.startswith(f"rotate-{x+1}-{y+i}"):
                            actions.append(move)
                            #print(f"ACTION: {move}")
                            return actions

    # If closest card is not a dead end, dynamite it.
    if closest.name not in dead_ends:
        #print("Closest card is dead end")
        for move in legal_moves:
            if move.startswith(f"dynamite-{x}-{y}"):
                actions.append(move)
                #print(f"ACTION: {move}")
                return actions

    # If Cross section below start card, dynamite it
    start_row = 6
    start_col = 10
    for i in range(3):
        if board[(start_row, start_col+i)] is not None:
            if board[(start_row, start_col+i)].name is Names.CROSS_SECTION:
                for move in legal_moves:
                    if move.startswith(f"dynamite-6-{10+i}"):
                        actions.append(move)
                        #print(f"ACTION: {move}")
                        return actions

    if x - target[0] < 0:
        #print("TARGET IS DOWN-ACROSS")
        #print(f"CHECKING FOR: place-{x+1}")
        for move in legal_moves:
            for i in range(-4, 4):
                if y+i < 20 and y+i >= 0:
                    if move.startswith(f"place-{x}-{y+i}") or move.startswith(f"rotate-{x}-{y+i}" or move.startswith(f"place-{x}-{y-i}") or move.startswith(f"rotate-{x}-{y-i}")):
                        actions.append(move)
                        #print(f"ACTION: {move}")
                        return actions

    #print("THROWING least ranked card")
    for i in range(7):
        for j in range(len(cards)):
            if cards[j].name == throwing_cards[i]:
                actions.append(f"discard-0-0-{j}")
                return actions

    #print("No actions found")
    actions.append(random.choice(legal_moves))

    return actions


'''
    if y - target[1] > 0:
        # Go left
        print("TARGET IS LEFT")
        for move in legal_moves:
            if move.startswith(f"place-{x}-{y-1}") or move.startswith(f"rotate-{x}-{y-1}"):
                for card in cards:
                    if not card.name == Names.TURN_RIGHT:
                        actions.append(move)
                        print(f"ACTION: {move}")
                        return actions

    if y - target[1] < 0:
        # Go right
        print("TARGET IS RIGHT")
        for move in legal_moves:
            if move.startswith(f"place-{x}-{y+1}") or move.startswith(f"rotate-{x}-{y+1}"):
                for card in cards:
                    if card.name == Names.TURN_LEFT:
                        actions.append(move)
                        print(f"ACTION: {move}")
                        return actions

    if x - target[0] > 0:
        # Go up
        print("TARGET IS UP")
        for move in legal_moves:
            if move.startswith(f"place-{x-1}-{y}") or move.startswith(f"rotate-{x-1}-{y}"):
                for card in cards:
                    if card.name == Names.CROSS_SECTION:
                        actions.append(move)
                        print(f"ACTION: {move}")
                        return actions
'''
