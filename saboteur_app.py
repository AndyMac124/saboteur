"""
saboteur_app.py
"""

import random

from saboteur_game import SaboteurGame
from saboteur_game_environment import SaboteurGameEnvironment
from saboteur_agent import SaboteurAgent
from saboteur_agent_programs import saboteur_agent_program
from gold_digger_agent_programs import gold_digger_agent_program

if __name__ == '__main__':

    # Creating and shuffling the 9 possible players
    possible_players = []
    for i in range(6):
        possible_players.append('gold_digger_agent_program')
    for i in range(3):
        possible_players.append('saboteur_agent_program')
    random.shuffle(possible_players)

    game_environment = SaboteurGameEnvironment()

    # Dictionary to store the actual players in this game
    players = {}

    # Assigning the first 8 players from the shuffled list
    for i in range(8):
        if possible_players[i] == 'gold_digger_agent_program':
            player = SaboteurAgent(i, gold_digger_agent_program)
        else:
            player = SaboteurAgent(i, saboteur_agent_program)
        players[i] = player
        # Adding player, players index, and player type
        game_environment.add_player_cards(player, i, possible_players[i])

    game = SaboteurGame(game_environment, players)
