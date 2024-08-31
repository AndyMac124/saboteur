import random

from saboteur_game_environment import SaboteurGameEnvironment as se

class GoldDiggerAgent:
    def __init__(self):
        self.suspected_saboteur = {}

    def agent_program(self, percepts, actuators):
        actions = []

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
        reported = gs['reported-cards']  # Dict of player_id and tuple (goal_index, bool)
        cards_player = gs['player-cards']  # Dict of player_id and list of cards played
        deck_is_empty = gs['deck-status']  # Bool (isEmpty)

        legal_moves = se.get_legal_actions_gs(gs)

        if len(cards) == 0 or len(legal_moves) == 0:
            move = ('pass', 0, 0, 0)
            actions.append(move)
            return actions

        # Dictionary of players and suspected saboteur
        self.suspected_saboteur = {}
        for i in range(8):
            self.suspected_saboteur[i] = False

        move = random.choice(legal_moves)
        actions.append(move)

        return actions