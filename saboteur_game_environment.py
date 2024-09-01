from typing import Dict, List, Optional
from playing_cards import Card, DeadEndCard, TableCard, ActionCard, GoalCard, GoldCard, StartCard, Names, SpecialCard, dirs
from une_ai.models import GameEnvironment
from game_board import GameBoard
from deck import Deck


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
                    next_access = board[char].get_access_points()
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
                        legal_actions.append(f'map-{j}-{b}-{i}')
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


class SaboteurGameEnvironment(GameEnvironment):

    def __init__(self):
        super().__init__("Saboteur Game Environment")
        self._game_board = GameBoard()
        self._players = []
        self._player_turn = 0
        self._mining_states = [True] * 8
        self._players_cards: List[List[Optional[Card]]] = [[] for _ in range(8)]
        self._deck = Deck()
        self._reported_cards: Dict[int, tuple[Optional[int], bool]] = {i: (None, False) for i in range(8)}
        self._played_cards = {}
        self._known_cards = [[None, None, None] for _ in range(8)]
        self._winner = "Draw"
        self.previous_move = "None"
        self.previous_player = "None"
        self.player_type_list = []

    def add_player(self, player):
        self._players.append(player)

    def add_player_cards(self, player, player_id, types):
        self.add_player(player)
        self.player_type_list.append(types)
        self._players_cards[player_id] = [self._deck.draw() for _ in range(4)]

    def get_game_board(self):
        return self._game_board

    def get_percepts(self):
        game_state = self.get_game_state()
        return {
            'game-board-sensor': game_state['game-board'],
            'turn-taking-indicator': game_state['player-turn'],
            'can-mine-sensor': game_state['mining-state'],
            'cards-in-hand-sensor': game_state['player-cards'],
            'reported-cards-sensor': game_state['reported-cards'],
            'deck-status': game_state['deck-status'],
            'cards-played-sensor': game_state['played_cards'],
            'flipped-cards-sensor': game_state['flipped_cards'],
            'known-cards-sensor': game_state['known_cards']
        }

    def get_legal_actions(game_state):
        return []

    def get_last_player_type(self):
        return str(self.previous_player)

    def get_previous_move(self):
        return str(self.previous_move)

    def get_player(self, player_id):
        if player_id in self._players:
            return self._players[player_id]
        else:
            raise KeyError(f"Player ID {player_id} not found in players dictionary")

    def turn(gamestate):
        player_id = gamestate['player-turn']
        return player_id

    def add_played_card(self, player_id, card):
        if player_id in self._played_cards:
            self._played_cards[player_id].append(card.name)
        else:
            self._played_cards[player_id] = [card.name]

    def get_game_state(self):
        game_state = {
            'game-board': self._game_board.copy(),
            'player-turn': self._player_turn,
            'mining-state': self._mining_states,
            'player-cards': self._players_cards[self._player_turn],
            'deck-status': self._deck.is_empty(),
            'deck': self._deck,
            'reported-cards': self._reported_cards, # Dict of player_id and  tuple (goal_index, bool)
            'played_cards': self._played_cards, # Dict of player_id and list of cards played
            'flipped_cards': self._game_board.get_flipped_cards(),
            'known_cards': self._known_cards[self._player_turn]
        }
        return game_state

    def get_winner(self):
        return self._winner

    def payoff(self, player_name):
        return 0

    def is_terminal(self):
        board = self._game_board.get_board()
        goal_locations = [(14,8), (14,10), (14,12)]

        for goal in goal_locations:
            if board[goal].name is Names.GOLD:
                access = Card.static_access_points(Names.GOLD)
                if is_connected_to_start(board, goal, access, self.get_game_board().get_flipped_cards()):
                    self._winner = "Gold Diggers"
                    return True

        if self._deck.is_empty():
            for i in range(8):
                pc = self._players_cards
                if pc[i] is not []:
                    return False
            self._winner = "Saboteurs"
            return True
        return False

    def _change_player_turn(self):
        self._player_turn = (self._player_turn + 1) % len(self._players)

    def _report_card(self, player_id, is_gold, index):
        # Dict of player_id and  tuple (goal_index, bool)
        if is_gold:
            self._reported_cards[player_id] = (int(index), True)
        else:
            self._reported_cards[player_id] = (int(index), False)


    def transition_result(self, game_state, action):
        game_board = self._game_board  # Use the existing GameBoard object
        new_gs = {
            'game-board': game_board,
            'player-turn': self._player_turn,
            'mining-state': self._mining_states,
            'player-cards': self._players_cards[self._player_turn],
            'reported-cards': self._reported_cards,
            'played-cards': self._played_cards,
            'known_cards': self._known_cards,
            'deck-status': self._deck.is_empty(),
            'deck': self._deck,
            'flipped_cards': self._game_board.get_flipped_cards(),
        }

        player_turn = game_state['player-turn']

        if action.startswith('place'):
            _, x, y, z = action.split('-')
            row = int(x)
            col = int(y)
            card_index = int(z)
            if card_index < 0 or card_index >= len(self._players_cards[player_turn]):
                raise IndexError(f"Card index {card_index} is out of range for player {player_turn}")
            card = self._players_cards[player_turn][card_index]
            self._game_board.add_path_card(row, col, card)
            self.add_played_card(player_turn, card)
            new_gs['player-cards'].remove(card)
            self.previous_move = f"Place Card at ({x},{y})"
            self.previous_player = self.previous_player = self.player_type_list[player_turn]
        elif action.startswith('pass'):
            self.previous_move = f"Pass (No cards left)"
            self.previous_player = self.previous_player = self.player_type_list[player_turn]
        elif action.startswith('rotate'):
            _, x, y, z = action.split('-')
            row = int(x)
            col = int(y)
            card_index = int(z)
            if card_index < 0 or card_index >= len(self._players_cards[player_turn]):
                raise IndexError(f"Card index {card_index} is out of range for player {player_turn}")
            card = self._players_cards[player_turn][card_index]
            self._game_board.add_flipped_path_card(row, col, card)
            self.add_played_card(player_turn, card)
            new_gs['player-cards'].remove(card)
            self.previous_move = f"Place Flipped Card at ({x},{y})"
            self.previous_player = self.previous_player = self.player_type_list[player_turn]
        elif action.startswith('discard'):
            _, _, _, index = action.split('-')
            card_index = int(index)
            card = self._players_cards[player_turn][card_index]
            new_gs['player-cards'].remove(card)
            self.previous_move = f"Discard index {card_index}"
            self.previous_player = self.previous_player = self.player_type_list[player_turn]
        elif action.startswith('mend'):
            _, _, p, z = action.split('-')
            card_index = int(z)
            if card_index < 0 or card_index >= len(self._players_cards[player_turn]):
                raise IndexError(f"Card index {card_index} is out of range for player {player_turn}")
            card = self._players_cards[player_turn][card_index]
            new_gs['player-cards'].remove(card)
            self.add_played_card(player_turn, card)
            self._mining_states[int(p)] = True
            self.previous_move = f"Mend player: {p}"
            self.previous_player = self.previous_player = self.player_type_list[player_turn]
        elif action.startswith('sabotage'):
            _, _, p, z = action.split('-')
            card_index = int(z)
            if card_index < 0 or card_index >= len(self._players_cards[player_turn]):
                raise IndexError(f"Card index {card_index} is out of range for player {player_turn}")
            card = self._players_cards[player_turn][card_index]
            new_gs['player-cards'].remove(card)
            self.add_played_card(player_turn, card)
            self._mining_states[int(p)] = False
            self.previous_move = f"Sabotage Player: {p}"
            self.previous_player = self.previous_player = self.player_type_list[player_turn]
        elif action.startswith('dynamite'):
            _, x, y, z = action.split('-')
            row = int(x)
            col = int(y)
            card_index = int(z)
            if card_index < 0 or card_index >= len(self._players_cards[player_turn]):
                raise IndexError(f"Card index {card_index} is out of range for player {player_turn}")
            card = self._players_cards[player_turn][card_index]
            self._game_board.remove_path_card(row, col)
            self.add_played_card(player_turn, card)
            new_gs['player-cards'].remove(card)
            self.previous_move = f"Drop Dynamite at ({x},{y})"
            self.previous_player = self.previous_player = self.player_type_list[player_turn]
        elif action.startswith('map'):
            _, y, index, z = action.split('-')
            card_index = int(z)
            y = int(y)
            if card_index < 0 or card_index >= len(self._players_cards[player_turn]):
                raise IndexError(f"Card index {card_index} is out of range for player {player_turn}")
            card = self._players_cards[player_turn][card_index]
            self.add_played_card(player_turn, card)
            new_gs['player-cards'].remove(card)
            is_gold = self._game_board.peak_goal_card(int(index))
            self._known_cards[player_turn][int(index)] = is_gold
            if y == 0:
                # Reveal Truth
                self._report_card(player_turn, is_gold, int(index))
            elif y == 1:
                # Reveal Lie
                self._report_card(player_turn, not is_gold, int(index))
            new_gs['reported-cards'] = self._reported_cards
            self.previous_move = f"Map for goal index:{index}"
            self.previous_player = self.player_type_list[player_turn]
        if not new_gs['deck-status']:
            new_card = self._deck.draw()
            new_gs['player-cards'].append(new_card)
        new_gs['player-turn'] = (player_turn + 1) % len(self._players)

        return new_gs

    def state_transition(self, agent_actuators):
        game_state = self.get_game_state()

        handling_type, x, y, z = agent_actuators['play-card']
        action = None

        if handling_type == 'pass':
            action = 'pass-{0}-{1}-{2}'.format(x, y, z)
        elif handling_type == 'rotate':
            action = 'rotate-{0}-{1}-{2}'.format(x, y, z)
        elif handling_type == 'place':
            action = 'place-{0}-{1}-{2}'.format(x, y, z)
        elif handling_type == 'discard':
            action = 'discard-{0}-{1}-{2}'.format(0, 0, z)
        elif handling_type == 'mend':
            action = 'mend-{0}-{1}-{2}'.format(0, x, z)
        elif handling_type == 'sabotage':
            action = 'sabotage-{0}-{1}-{2}'.format(0, x, z)
        elif handling_type == 'map':
            action = 'map-{0}-{1}-{2}'.format(x, y, z)
        elif handling_type == 'dynamite':
            action = 'dynamite-{0}-{1}-{2}'.format(x, y, z)

        if action is not None:
            new_state = self.transition_result(game_state, action)
            self._players_cards[self._player_turn] = new_state['player-cards']
            self._player_turn = new_state['player-turn']
