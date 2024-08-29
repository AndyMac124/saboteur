import random

from une_ai.models import GameEnvironment
from game_board import GameBoard

class SaboteurGameEnvironment(GameEnvironment):

    def __init__(self, players):
        super().__init__("Saboteur Game Environment")
        self._game_board = GameBoard()
        self._players = players
        self._player_turn = random.choice(players)
        self._mining_states = {player: True for player in players}

    def add_player(self, player):
        self._players.append(player)
        self._mining_states[player] = True

    def get_game_board(self):
        return self._game_board.get_board()

    def get_percepts(self):
        game_state = self.get_game_state()
        return {
            'game-board': game_state['game-board'].get_map(),
            'player-turn': game_state['player-turn']
        }

    def turn(game_state):
        return game_state['player-turn']

    def get_game_state(self):
        game_state = {
            'game-board': self._game_board.copy(),
            'player-turn': self._player_turn,
            'mining-state': self._mining_states
        }
        return game_state

    # TODO determine winner based on game state/board
    def get_winner(game_state):
        pass

    # TODO determine payoff for a player based on game state
    def payoff(game_state, player_name):
        return 0

    # TODO determine if game state is terminal
    def is_terminal(game_state):
        return False

    # TODO all legal placements and special cards
    def get_legal_actions(game_state):
        return []

    def _change_player_turn(self):
        self._player_turn = self._players[(self._players.index(self._player_turn) + 1) % len(self._players)]

    # TODO next gamestate based on an action
    def transition_result(game_state, action):
        return game_state

    def state_transition(self, agent_actuators):
        game_state = self.get_game_state()
        action = agent_actuators[self._player_turn]
        game_state = self.transition_result(game_state, action)
        self._change_player_turn()
        return game_state