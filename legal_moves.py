"""
legal_moves.py

Purpose: Generates all legal moves for the given game state information
"""

from playing_cards import Card, TableCard, ActionCard, GoalCard, SpecialCard
from shared import Names, DECards, Dirs

# Function to recursively call the DFS
def is_connected_to_start(board, location, access, flipped_cards):
    seen = set()
    return depth_first_search(board, location, seen, access, flipped_cards)

# Aims to find a path from the given location back to the starting location
def depth_first_search(board, location, seen, access, flipped_cards):
    if location == (6, 10):
        return True

    # Add the current location so that we don't check it again
    seen.add(location)
    # Get the four coordinates surrounding our current location
    n, e, s, w = surrounding_locations(location)

    # For each direction, check it is in the board, has not been seen and has a card
    # Then find the access points, compare with the current cards access points to see if their paths join
    for char in (n, e, s, w):
        if is_within_boundary(char) and char not in seen and board[char] is not None:
            if ((board[char].name not in DECards) and (type(board[char]) is not GoalCard) and board[char].name
                    is not Names.DYNAMITE):
                if char in flipped_cards:
                    next_access = Card.static_access_points(board[char].name, flipped=True)
                else:
                    next_access = Card.static_access_points(board[char].name)
                if char is n:
                    if Dirs.SOUTH in next_access:
                        if Dirs.NORTH in access:
                            if depth_first_search(board, char, seen, next_access, flipped_cards):
                                return True
                elif char is e:
                    if Dirs.WEST in next_access:
                        if Dirs.EAST in access:
                            if depth_first_search(board, char, seen, next_access, flipped_cards):
                                return True
                elif char is s:
                    if Dirs.NORTH in next_access:
                        if Dirs.SOUTH in access:
                            if depth_first_search(board, char, seen, next_access, flipped_cards):
                                return True
                elif char is w:
                    if Dirs.EAST in next_access:
                        if Dirs.WEST in access:
                            if depth_first_search(board, char, seen, next_access, flipped_cards):
                                return True
    return False

# Just gets the four surrounding locations
def surrounding_locations(location):
    x, y = location
    n = (x-1, y)
    e = (x, y+1)
    s = (x+1, y)
    w = (x, y-1)
    return n, e, s, w

# Checks if a location is withing the boundary of the board
def is_within_boundary(location):
    x, y = location
    return 0 <= x < 20 and 0 <= y < 20

# Returns the access points for the given location, board, and rotated state
def get_access_points(board, loc, flipped_cards):
    if loc in flipped_cards:
        access = Card.static_access_points(board[loc].name, flipped=True)
    else:
        access = Card.static_access_points(board[loc].name)
    return access

# Checks if a location is valid and meets the game rules, using the DFS function above
def is_valid_placement_gs(board, col, row, card, flipped_cards, flipped=False):
    # Get the access points based on whether the card is flipped or not
    if flipped:
        access = Card.static_access_points(card.name, flipped=True)
    else:
        access = Card.static_access_points(card.name)

    loc = (row, col)
    # Check the card has a path back to the start
    if not is_connected_to_start(board, loc, access, flipped_cards):
        return False

    # Get the surrounding locations
    n, e, s, w = surrounding_locations(loc)

    # Now make sure all paths are connected as per the rules
    # For each of the four directions, if the location on the board and has a card on it
    # Then check if a path leads to a wall
    if is_within_boundary(n) and board[n] is not None:
        next_a = get_access_points(board, n, flipped_cards)
        if Dirs.SOUTH in next_a and Dirs.NORTH not in access:
            return False
        if Dirs.SOUTH not in next_a and Dirs.NORTH in access:
            return False

    if is_within_boundary(e) and board[e] is not None:
        next_a = get_access_points(board, e, flipped_cards)
        if Dirs.WEST in next_a and Dirs.EAST not in access:
            return False
        if Dirs.WEST not in next_a and Dirs.EAST in access:
            return False

    if is_within_boundary(s) and board[s] is not None:
        next_a = get_access_points(board, s, flipped_cards)
        if Dirs.NORTH in next_a and Dirs.SOUTH not in access:
            return False
        if Dirs.NORTH not in next_a and Dirs.SOUTH in access:
            return False

    if is_within_boundary(w) and board[w] is not None:
        next_a = get_access_points(board, w, flipped_cards)
        if Dirs.EAST in next_a and Dirs.WEST not in access:
            return False
        if Dirs.EAST not in next_a and Dirs.WEST in access:
            return False

    return True

# Builds a list of all legal actions for the given arguments
def get_legal_actions_gs(board, can_mine, player_cards, flipped_cards):
    legal_actions = []

    # Check for standard playing cards
    for i in range(len(player_cards)):
        # We can discard any card
        legal_actions.append(f'discard-{0}-{0}-{i}')
        card = player_cards[i]
        if type(card) is TableCard:
            if can_mine:
                for r in range(20):
                    for c in range(20):
                        if board[(r, c)] is None:
                            if r in [5, 7] and c in [9, 11] and card.name in DECards:
                                continue
                            # Check each TableCard in normal and flipped state
                            if is_valid_placement_gs(board, c, r, card, flipped_cards):
                                legal_actions.append(f'place-{r}-{c}-{i}')
                            if is_valid_placement_gs(board, c, r, card, flipped_cards, flipped=True):
                                legal_actions.append(f'rotate-{r}-{c}-{i}')
        # Now check the ActionCards
        elif type(card) is ActionCard:
            if card.name == Names.MAP:
                for index in range(3):
                    for b in range(2):
                        legal_actions.append(f'map-{b}-{index}-{i}')
            elif card.name == Names.MEND:
                for p in range(8):
                    legal_actions.append(f'mend-{0}-{p}-{i}')
            elif card.name == Names.SABOTAGE:
                for p in range(8):
                    legal_actions.append(f'sabotage-{0}-{p}-{i}')
            elif card.name == Names.DYNAMITE:
                for r in range(20):
                    for c in range(20):
                        # Can't use dynamite on special cards
                        card_type = type(board[(r, c)])
                        specials = [(6, 10), (14, 8), (14, 10), (14, 12)]
                        if board[(r, c)] is not None:
                            # Double-checking here, I had some issues
                            if card_type is not SpecialCard and (r, c) not in specials:
                                legal_actions.append(f'dynamite-{r}-{c}-{i}')
            else:
                raise ValueError(f"Unknown action card {card.name}")

    return legal_actions
