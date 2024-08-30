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

    def get_game_board(self):
        return self._game_board.get_board()

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
        return game_state

    def state_transition(self, agent_actuators):
        game_state = self.get_game_state()
        print(f"Player Turn: {self._player_turn}")
        self._change_player_turn()
        return game_state
