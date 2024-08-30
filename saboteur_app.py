import random

from saboteur_game import SaboteurGame
from saboteur_game_environment import SaboteurGameEnvironment
from saboteur_agent import SaboteurAgent
from saboteur_agent_programs import saboteur_agent_program
from gold_digger_agent_programs import gold_digger_agent_program

if __name__ == '__main__':

    possible_players = []
    for i in range(6):
        possible_players.append('gold_digger_agent_program')
    for i in range(3):
        possible_players.append('saboteur_agent_program')
    random.shuffle(possible_players)

    players = {}
    for i in range(8):
        if possible_players[i] == 'gold_digger_agent_program':
            name = 'gold_digger_agent_program_{0}'.format(i)
            player = SaboteurAgent(name, gold_digger_agent_program)
        else:
            name = 'saboteur_agent_program_{0}'.format(i)
            player = SaboteurAgent(name, saboteur_agent_program)
        players[i] = [name, player]

    game_environment = SaboteurGameEnvironment(players)

    for key, value in players.items():
        game_environment.add_player_idx(key, value)
        print(key, value)

    game = SaboteurGame(game_environment, players)
