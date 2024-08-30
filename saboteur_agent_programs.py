

def saboteur_agent_program(percepts, actuators):
    actions = []

    game_state = {
        'game-board': percepts['game-board-sensor'],
        'player-turn': percepts['turn-taking-indicator'],
        'mining-state': percepts['cards-in-hand-sensor'],
        'player-cards': percepts['can-mine-sensor']
    }

    return None
