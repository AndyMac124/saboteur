"""
saboteur_game_environment.py

Reference: This class was based off the ConnectFourEnvironment class from the COSC350 Assignment 2 by Johnathon Vitale.
"""

import random
from typing import Dict, List, Optional
from playing_cards import Card, Names
from legal_moves import is_connected_to_start
from une_ai.models import GameEnvironment
from game_board import GameBoard
from deck import Deck


# Game Environment for Saboteur Game
class SaboteurGameEnvironment(GameEnvironment):

    def __init__(self):
        super().__init__("Saboteur Game Environment")
        self._game_board = GameBoard()
        self._players = []
        first = random.randint(0, 7)
        self._player_turn = first
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

    # Adds a player, their four cards and their type to the game
    def add_player_with_cards(self, player, player_id, types):
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

    # Using the legal_moves file instead of this
    def get_legal_actions(game_state):
        return []

    # Used by the GUI to display the type of previous player
    def get_last_player_type(self):
        return str(self.previous_player)

    # Used by the GUI to display the previous move
    def get_previous_move(self):
        return str(self.previous_move)

    def turn(gamestate):
        player_id = gamestate['player-turn']
        return player_id

    # Adds a played card to the list of played cards at position of player_id
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

    # Using a rule based strategy in agent programs
    def payoff(self, player_name):
        return 0

    def is_terminal(self):
        board = self._game_board.get_board()
        goal_locations = [(14,8), (14,10), (14,12)]

        # If the gold card is flipped, check if it is connected to the start
        for goal in goal_locations:
            if board[goal].name is Names.GOLD:
                access = Card.static_access_points(Names.GOLD)
                if is_connected_to_start(board, goal, access, self.get_game_board().get_flipped_cards()):
                    self._winner = "Gold Diggers"
                    return True

        # If the deck is empty, check if all players have no cards left
        if self._deck.is_empty():
            for i in range(8):
                pc = self._players_cards
                if pc[i]:
                    return False
            self._winner = "Saboteurs"
            return True

        return False

    # Used when a player uses the map card, adds to dict of reported cards
    def _report_card(self, player_id, truth, index):
        # Dict of player_id and  tuple (goal_index, bool)
        if truth:
            self._reported_cards[player_id] = (int(index), True)
        else:
            self._reported_cards[player_id] = (int(index), False)

    # Used for placing a card on the board in standard orientation
    def _place_card(self, player_turn, new_gs, row, col, c):
        card = self._players_cards[player_turn][c]
        self._game_board.add_path_card(row, col, card)
        self.add_played_card(player_turn, card)
        new_gs['player-cards'].remove(card)
        self.previous_move = f"Place Card at ({row},{col})"
        self.previous_player = self.previous_player = self.player_type_list[player_turn]

    # Used for placing a card on the board in rotated orientation
    def _place_rotated_card(self, player_turn, new_gs, row, col, c):
        card = self._players_cards[player_turn][c]
        self._game_board.add_flipped_path_card(row, col, card)
        self.add_played_card(player_turn, card)
        new_gs['player-cards'].remove(card)
        self.previous_move = f"Place Flipped Card at ({row},{col})"
        self.previous_player = self.previous_player = self.player_type_list[player_turn]

    # Used for discarding a card
    def _discard_card(self, player_turn, new_gs, card_index):
        card = self._players_cards[player_turn][card_index]
        new_gs['player-cards'].remove(card)
        self.previous_move = f"Discard index {card_index}"
        self.previous_player = self.previous_player = self.player_type_list[player_turn]

    # Used for mending a player and changing their mining state to True
    def _mend_player(self, player_turn, new_gs, p, card_index):
        card = self._players_cards[player_turn][card_index]
        new_gs['player-cards'].remove(card)
        self.add_played_card(player_turn, card)
        self._mining_states[p] = True
        self.previous_move = f"Mend player: {p}"
        self.previous_player = self.previous_player = self.player_type_list[player_turn]

    # Used for sabotaging a player and changing their mining state to False
    def _sabotage_player(self, player_turn, new_gs, p, card_index):
        card = self._players_cards[player_turn][card_index]
        new_gs['player-cards'].remove(card)
        self.add_played_card(player_turn, card)
        self._mining_states[p] = False
        self.previous_move = f"Sabotage Player: {p}"
        self.previous_player = self.previous_player = self.player_type_list[player_turn]

    # Used for playing a dynamite card and removing a path card from the board
    def _play_dynamite(self, player_turn, new_gs, row, col, card_index):
        card = self._players_cards[player_turn][card_index]
        self._game_board.remove_path_card(row, col)
        self.add_played_card(player_turn, card)
        new_gs['player-cards'].remove(card)
        self.previous_move = f"Drop Dynamite at ({row},{col})"
        self.previous_player = self.previous_player = self.player_type_list[player_turn]

    # Used for playing a map card to peak at a goal card
    def _play_map(self, player_turn, new_gs, truth, g_idx, card_index):
        card = self._players_cards[player_turn][card_index]
        self.add_played_card(player_turn, card)
        new_gs['player-cards'].remove(card)
        is_gold = self._game_board.peak_goal_card(g_idx)
        self._known_cards[player_turn][g_idx] = is_gold
        if truth == 0:
            # Reveal Truth
            self._report_card(player_turn, is_gold, g_idx)
        elif truth == 1:
            # Reveal Lie
            self._report_card(player_turn, not is_gold, g_idx)
        new_gs['reported-cards'] = self._reported_cards
        self.previous_move = f"Map for goal index:{g_idx}"
        self.previous_player = self.player_type_list[player_turn]

    # Generates a new game state based on an action
    def transition_result(self, game_state, action):
        game_board = self._game_board
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

        _, row_str, col_str, c = action.split('-')
        row = int(row_str)
        col = int(col_str)
        card_index = int(c)
        assert card_index < len(self._players_cards[player_turn]), f"Card index {card_index} is out of range for player {player_turn}"
        assert card_index >= 0, f"Card index {card_index} is out of range for player {player_turn}"

        if action.startswith('place'):
            self._place_card(player_turn, new_gs, row, col, card_index)
        elif action.startswith('pass'):
            self.previous_move = f"Pass (No cards left)"
            self.previous_player = self.previous_player = self.player_type_list[player_turn]
        elif action.startswith('rotate'):
            self._place_rotated_card(player_turn, new_gs, row, col, card_index)
        elif action.startswith('discard'):
            self._discard_card(player_turn, new_gs, card_index)
        elif action.startswith('mend'):
            self._mend_player(player_turn, new_gs, col, card_index)
        elif action.startswith('sabotage'):
            self._sabotage_player(player_turn, new_gs, col, card_index)
        elif action.startswith('dynamite'):
            self._play_dynamite(player_turn, new_gs, row, col, card_index)
        elif action.startswith('map'):
            self._play_map(player_turn, new_gs, row, col, card_index)

        # If deck is not empty, draw a card
        if not new_gs['deck-status']:
            new_card = self._deck.draw()
            new_gs['player-cards'].append(new_card)

        new_gs['player-turn'] = (player_turn + 1) % len(self._players)

        return new_gs

    # Generates the state transition for the agent
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
