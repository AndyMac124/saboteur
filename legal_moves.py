from playing_cards import Card, DeadEndCard, TableCard, ActionCard, GoalCard, Names, SpecialCard, dirs

def is_connected_to_start(board, location, access, flipped_cards):
    seen = set()
    return depth_first_search(board, location, seen, access, flipped_cards)


def depth_first_search(board, location, seen, access, flipped_cards):
    # If we've reached the start card, return True
    if location == (6, 10): # Assuming (6, 10) is the location of the start card
        return True

    DECards = {
        Names.DE_ALL,
        Names.DE_W,
        Names.DE_N,
        Names.DE_NS,
        Names.DE_WS,
        Names.DE_WN,
        Names.DE_EW,
        Names.DE_3_S,
        Names.DE_3_E
    }

    seen.add(location)
    n, e, s, w = surrounding_locations(location)

    for char in (n, e, s, w):
        if is_within_boundary(char) and char not in seen and board[char] is not None:
            if (board[char].name not in DECards) and (type(board[char]) is not GoalCard) and board[char].name is not Names.DYNAMITE:
                if char in flipped_cards:
                    next_access = Card.static_access_points(board[char].name, flipped=True)
                else:
                    next_access = Card.static_access_points(board[char].name)
                if char is n:
                    if dirs.SOUTH in next_access:
                        if dirs.NORTH in access:
                            if depth_first_search(board, char, seen, next_access, flipped_cards):
                                return True
                elif char is e:
                    if dirs.WEST in next_access:
                        if dirs.EAST in access:
                            if depth_first_search(board, char, seen, next_access, flipped_cards):
                                return True
                elif char is s:
                    if dirs.NORTH in next_access:
                        if dirs.SOUTH in access:
                            if depth_first_search(board, char, seen, next_access, flipped_cards):
                                return True
                elif char is w:
                    if dirs.EAST in next_access:
                        if dirs.WEST in access:
                            if depth_first_search(board, char, seen, next_access, flipped_cards):
                                return True
    return False


def surrounding_locations(location):
    x, y = location
    n = (x-1, y)
    e = (x, y+1)
    s = (x+1, y)
    w = (x, y-1)
    return n, e, s, w


def is_within_boundary(location):
    x, y = location
    return 0 <= x < 20 and 0 <= y < 20


def is_valid_placement_gs(board, col, row, card, flipped_cards, flipped=False):
    if flipped:
        access = Card.static_access_points(card.name, flipped=True)
    else:
        access = Card.static_access_points(card.name)

    if not is_connected_to_start(board, (row, col), access, flipped_cards):
        return False

    loc = (row, col)
    n, e, s, w = surrounding_locations(loc)
    paths = 0

    if is_within_boundary(n) and board[n] is not None:
        if n in flipped_cards:
            next_a = Card.static_access_points(board[n].name, flipped=True)
        else:
            next_a = Card.static_access_points(board[n].name)
        if (dirs.SOUTH in next_a) and dirs.NORTH in access:
            if type(board[n]) is not DeadEndCard:
                paths += 1
        else:
            return False

    if is_within_boundary(e) and board[e] is not None:
        if e in flipped_cards:
            next_a = Card.static_access_points(board[e].name, flipped=True)
        else:
            next_a = Card.static_access_points(board[e].name)
        if (dirs.WEST in next_a) and dirs.EAST in access:
            if type(board[e]) is not DeadEndCard:
                paths += 1
        else:
            return False

    if is_within_boundary(s) and board[s] is not None:
        if s in flipped_cards:
            next_a = Card.static_access_points(board[s].name, flipped=True)
        else:
            next_a = Card.static_access_points(board[s].name)
        if (dirs.NORTH in next_a) and dirs.SOUTH in access:
            if type(board[s]) is not DeadEndCard:
                paths += 1
        else:
            return False

    if is_within_boundary(w) and board[w] is not None:
        if w in flipped_cards:
            next_a = Card.static_access_points(board[w].name, flipped=True)
        else:
            next_a = Card.static_access_points(board[w].name)
        if (dirs.EAST in next_a) and dirs.WEST in access:
            if type(board[w]) is not DeadEndCard:
                paths += 1
        else:
            return False
    return paths > 0


def get_legal_actions_gs(board, mining, player_cards, flipped_cards):
    legal_actions = []

    for i in range(len(player_cards)):
        legal_actions.append(f'discard-{0}-{0}-{i}')
        card = player_cards[i]
        if type(card) is TableCard:
            if mining:
                for r in range(20):
                    for c in range(20):
                        if board[(r, c)] is None:
                            if is_valid_placement_gs(board, c, r, card, flipped_cards):
                                legal_actions.append(f'place-{r}-{c}-{i}')
                            if is_valid_placement_gs(board, c, r, card, flipped_cards, flipped=True):
                                legal_actions.append(f'rotate-{r}-{c}-{i}')

        elif type(card) is ActionCard:
            if card.name == Names.MAP:
                # Could check if any are unknown
                for j in range(3):
                    for b in range(2):
                        legal_actions.append(f'map-{b}-{j}-{i}')
            elif card.name == Names.MEND:
                for j in range(8):
                    legal_actions.append(f'mend-{0}-{j}-{i}')
            elif card.name == Names.SABOTAGE:
                for j in range(8):
                    legal_actions.append(f'sabotage-{0}-{j}-{i}')
            elif card.name == Names.DYNAMITE:
                for r in range(20):
                    for c in range(20):
                        card_type = type(board[(r, c)])
                        specials = [(6, 10), (14, 8), (14, 10), (14, 12)]
                        if board[(r, c)] is not None:
                            if card_type is not SpecialCard and (r, c) not in specials:
                                legal_actions.append(f'dynamite-{r}-{c}-{i}')
            else:
                raise ValueError(f"Unknown action card {card.name}")
    return legal_actions