import random

from typing import Dict, List, Optional
from playing_cards import Card, DeadEndCard, TableCard, ActionCard, GoalCard, GoldCard, StartCard, Names, SpecialCard, dirs
from une_ai.models import GameEnvironment
from game_board import GameBoard
from deck import Deck

class SaboteurGameEnvironment(GameEnvironment):

    def __init__(self):
        super().__init__("Saboteur Game Environment")
        self._game_board = GameBoard()
        self._players = []
        self._player_turn = 0
        self._mining_states = [True] * 8
        self._players_cards: List[List[Optional[Card]]] = [[] for _ in range(8)]
        self._deck = Deck()
        self._reported_cards = {}
        self._played_cards = {}

    def add_player(self, player):
        self._players.append(player)

    def add_player_cards(self, player, player_id):
        self.add_player(player)
        self._players_cards[player_id] = [self._deck.draw() for _ in range(4)]

    def get_game_board(self):
        return self._game_board

    def get_percepts(self):
        game_state = self.get_game_state()
        return {
            'game-board-sensor': game_state['game-board'],
            'turn-taking-indicator': game_state['player-turn'],
            'can-mine-sensor': game_state['mining-state'][self._player_turn],
            'cards-in-hand-sensor': game_state['player-cards'],
            'reported-cards-sensor': game_state['reported-cards'],
            'cards-played-sensor': game_state['player-cards']
        }

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
            self._played_cards[player_id].append(card)
        else:
            self._played_cards[player_id] = [card]

    def get_game_state(self):
        game_state = {
            'game-board': self._game_board.copy(),
            'player-turn': self._player_turn,
            'mining-state': self._mining_states,
            'player-cards': self._players_cards[self._player_turn],
            'deck': self._deck,
            'reported-cards': self._reported_cards, # Dict of player_id and  tuple (goal_index, bool)
            'players': self._played_cards # Dict of player_id and list of cards played
        }
        return game_state

    def get_winner(self):
        gold_location = self._game_board.gold_loc
        g_x, g_y = gold_location
        game_board = self._game_board.get_board()

        if (game_board[g_x + 1, g_y] is None
                and game_board[(g_x - 1, g_y)] is None
                and game_board[(g_x, g_y + 1)] is None
                and game_board[(g_x, g_y - 1)] is None):
            return 'saboteurs'

        if self._game_board.is_connected_start(gold_location):
            return 'gold-diggers'


    # TODO determine payoff for a player based on game state
    def payoff(self, player_name):
        return 0

    def is_terminal(self):
        if self._deck.is_empty():
            for player in self._players:
                if not player.has_legal_moves():
                    return True
        return False

    def is_valid_placement(self, game_board, col, row, card, flipped=False):
        if flipped:
            access = Card.static_access_points(card.name, flipped=True)
        else:
            access = Card.static_access_points(card.name)

        paths = 0

        if col > 0:
            W = (game_board[col - 1, row] is not None)
        else:
            W = False

        if row > 0:
            N = (game_board[col, row - 1] is not None)
        else:
            N = False

        if col < 19:
            E = (game_board[col + 1, row] is not None)
        else:
            E = False

        if row < 19:
            S = (game_board[col, row + 1] is not None)
        else:
            S = False

        if N:
            n_card = game_board[col, row - 1]
            n_card_access = n_card.get_access_points()
            if dirs.SOUTH in n_card_access:
                if dirs.NORTH in access:
                    if type(n_card) is not DeadEndCard:
                        paths += 1
                else:
                    return False

        if E:
            e_card = game_board[col + 1, row]
            e_card_access = e_card.get_access_points()
            if dirs.WEST in e_card_access:
                if dirs.EAST in access:
                    if type(e_card) is not DeadEndCard:
                        paths += 1
                else:
                    return False

        if S:
            s_card = game_board[col, row + 1]
            s_card_access = s_card.get_access_points()
            if dirs.NORTH in s_card_access:
                if dirs.SOUTH in access:
                    if type(s_card) is not DeadEndCard:
                        paths += 1
                else:
                    return False

        if W:
            w_card = game_board[col - 1, row]
            w_card_access = w_card.get_access_points()
            if dirs.EAST in w_card_access:
                if dirs.WEST in access:
                    if type(w_card) is not DeadEndCard:
                        paths += 1
                else:
                    return False

        return True

    def get_legal_actions(self):
        player_cards = self._players_cards[self._player_turn]
        deck = self._deck
        board = self._game_board.get_board()

        legal_actions = []

        if not deck.is_empty():
            legal_actions.append('draw')

        for i in range(len(player_cards)):
            legal_actions.append(f'discard-card-{i}')
            card = player_cards[i]
            if type(card) is TableCard:
                if self._mining_states[self._player_turn]:
                    for r in range(20):
                        for c in range(20):
                            if board[(r, c)] is not None and self._game_board.is_connected_start((r, c)):
                                if self.is_valid_placement(board, c, r, card):
                                    legal_actions.append(f'place-{r}-{c}-{i}')
                                if self.is_valid_placement(board, c, r, card, flipped=True):
                                    legal_actions.append(f'rotate-{r}-{c}-{i}')

            elif type(card) is ActionCard:
                if card.name == Names.MAP:
                    # Could check if any are unknown
                    for j in range(3):
                        legal_actions.append(f'map-{j}-{i}')
                elif card.name == Names.MEND:
                    for j in range(8):
                        legal_actions.append(f'mend-{j}-{i}')
                elif card.name == Names.SABOTAGE:
                    for j in range(8):
                        legal_actions.append(f'sabotage-{j}-{i}')
                elif card.name == Names.DYNAMITE:
                    for r in range(20):
                        for c in range(20):
                            # Unless we want to restrict dynamite to actual use.
                            card_type = type(board[(r, c)])
                            if card_type is not SpecialCard:
                                legal_actions.append(f'dynamite-{r}-{c}-{i}')
                else:
                    raise ValueError(f"Unknown action card {card.name}")

        return legal_actions

    def _change_player_turn(self):
        self._player_turn = (self._player_turn + 1) % len(self._players)

    def _report_card(self, player_id, is_gold, index):
        # Dict of player_id and  tuple (goal_index, bool)
        self._reported_cards[(player_id, index)] = is_gold


    def transition_result(self, game_state, action):
        game_board = self._game_board  # Use the existing GameBoard object
        new_gs = {
            'game-board': game_board,
            'player-turn': self._player_turn,
            'mining-state': self._mining_states,
            'player-cards': self._players_cards[self._player_turn],
            'reported-cards': self._reported_cards,
            'played-cards': self._played_cards
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
        elif action.startswith('discard'):
            _, index = action.split('-')
            card_index = int(index)
            card = self._players_cards[player_turn][card_index]
            new_gs['player-cards'].remove(card)
        elif action.startswith('mend'):
            _, p, z = action.split('-')
            card_index = int(z)
            if card_index < 0 or card_index >= len(self._players_cards[player_turn]):
                raise IndexError(f"Card index {card_index} is out of range for player {player_turn}")
            card = self._players_cards[player_turn][card_index]
            new_gs['player-cards'].remove(card)
            self.add_played_card(player_turn, card)
            self._mining_states[int(p)] = True
        elif action.startswith('sabotage'):
            _, p, z = action.split('-')
            card_index = int(z)
            if card_index < 0 or card_index >= len(self._players_cards[player_turn]):
                raise IndexError(f"Card index {card_index} is out of range for player {player_turn}")
            card = self._players_cards[player_turn][card_index]
            new_gs['player-cards'].remove(card)
            self.add_played_card(player_turn, card)
            self._mining_states[int(p)] = False
        elif action.startswith('dynamite'):
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
        elif action.startswith('map'):
            _, index, y, z = action.split('-')
            card_index = int(z)
            if card_index < 0 or card_index >= len(self._players_cards[player_turn]):
                raise IndexError(f"Card index {card_index} is out of range for player {player_turn}")
            card = self._players_cards[player_turn][card_index]
            self.add_played_card(player_turn, card)
            new_gs['player-cards'].remove(card)
            card = self._game_board.peak_goal_card(int(index))
            if y == 0:
                # Reveal Truth
                self._report_card(player_turn, card, int(index))
            elif y == 1:
                # Reveal Lie
                self._report_card(player_turn, not card, int(index))

        new_card = self._deck.draw()
        new_gs['player-cards'].append(new_card)
        new_gs['player-turn'] = (player_turn + 1) % len(self._players)

        return new_gs

    def state_transition(self, agent_actuators):
        game_state = self.get_game_state()
        # print(f"Player Turn: {self._player_turn}")

        legal_actions = self.get_legal_actions()
        print(f"Legal Actions: {legal_actions}")

        rotate = agent_actuators['rotate-card']
        handling_type, x, y, z = agent_actuators['play-card']
        # print(rotate)
        action = None

        if handling_type == 'place':
            if rotate:
                action = 'rotate-{0}-{1}-{2}'.format(x, y, z)
            else:
                action = 'place-{0}-{1}-{2}'.format(x, y, z)
        elif handling_type == 'discard':
            action = 'discard-{0}'.format(z)
        elif handling_type == 'mend':
            action = 'mend-{0}-{1}'.format(x, z)
        elif handling_type == 'sabotage':
            action = 'sabotage-{0}-{1}'.format(x, z)
        elif handling_type == 'map':
            action = 'map-{0}-{1}-{2}'.format(x, y, z)
        elif handling_type == 'dynamite':
            action = 'dynamite-{0}-{1}-{2}'.format(x, y, z)

        if action is not None:
            new_state = self.transition_result(game_state, action)
            self._players_cards[self._player_turn] = new_state['player-cards']
            self._player_turn = new_state['player-turn']
