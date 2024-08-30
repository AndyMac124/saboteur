import random

from typing import Dict, List, Optional
from playing_cards import Card
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
            'cards-in-hand-sensor': game_state['player-cards']
        }

    def get_player(self, player_id):
        if player_id in self._players:
            return self._players[player_id]
        else:
            raise KeyError(f"Player ID {player_id} not found in players dictionary")

    def turn(gamestate):
        player_id = gamestate['player-turn']
        return player_id

    def get_game_state(self):
        game_state = {
            'game-board': self._game_board.copy(),
            'player-turn': self._player_turn,
            'mining-state': self._mining_states,
            'player-cards': self._players_cards[self._player_turn]
        }
        return game_state

    # TODO determine winner based on game state/board
    def get_winner(self):
        pass

    # TODO determine payoff for a player based on game state
    def payoff(self, player_name):
        return 0

    # TODO determine if game state is terminal
    def is_terminal(self):
        return False

    # TODO all legal placements and special cards
    def get_legal_actions(self):
        return []

    def _change_player_turn(self):
        self._player_turn = (self._player_turn + 1) % len(self._players)

    # TODO next gamestate based on an action
    def transition_result(self, game_state, action):
        game_board = self._game_board  # Use the existing GameBoard object
        new_gs = {
            'game-board': game_board,
            'player-turn': self._player_turn,
            'mining-state': self._mining_states,
            'player-cards': self._players_cards[self._player_turn]
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
            new_gs['player-cards'].remove(card)
        elif action.startswith('discard'):
            _, index = action.split('-')
            card_index = int(index)
            card = self._players_cards[player_turn][card_index]
            new_gs['player-cards'].remove(card)
        elif action == 'play-mend-card':
            pass
        elif action == 'play-sabotage-card':
            pass
        elif action == 'play-dynamite-card':
            pass
        elif action == 'play-map-card':
            pass

        new_card = self._deck.draw()
        new_gs['player-cards'].append(new_card)
        new_gs['player-turn'] = (player_turn + 1) % len(self._players)

        return new_gs

    def state_transition(self, agent_actuators):
        game_state = self.get_game_state()
        print(f"Player Turn: {self._player_turn}")

        action = None

        if 'place-card' in agent_actuators:
            _, x, y, z = agent_actuators['place-card']
            action = 'place-{0}-{1}-{2}'.format(x, y, z)
        elif 'discard-card' in agent_actuators:
            _, index = agent_actuators['discard-card']
            action = 'discard-{0}'.format(index)
        elif 'play-mend-card' in agent_actuators and agent_actuators['play-mend-card']:
            action = 'play-mend-card'
        elif 'play-sabotage-card' in agent_actuators and agent_actuators['play-sabotage-card']:
            action = 'play-sabotage-card'
        elif 'play-dynamite-card' in agent_actuators and agent_actuators['play-dynamite-card']:
            action = 'play-dynamite-card'
        elif 'play-map-card' in agent_actuators and agent_actuators['play-map-card']:
            action = 'play-map-card'

        if action is not None:
            new_state = self.transition_result(game_state, action)
            self._players_cards[self._player_turn] = new_state['player-cards']
            self._player_turn = new_state['player-turn']
