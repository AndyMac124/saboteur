import random

def gold_digger_agent_program(percepts, actuators):
    actions = []

    game_state = {
        'game-board': percepts['game-board-sensor'],
        'player-turn': percepts['turn-taking-indicator'],
        'mining-state': percepts['cards-in-hand-sensor'],
        'player-cards': percepts['can-mine-sensor']
    }

    x = random.choice(range(20))
    y = random.choice(range(20))

    r = "place-{0}-{1}-0".format(x, y)

    actions.append(r)

    return actions
