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

    r = "dynamite-{0}-{1}-{2}".format(14, 13, 0)
    g = "rotate-false"

    actions.append(r)
    actions.append(g)

    return actions
