import random

from saboteur_game_environment import SaboteurGameEnvironment as se

def saboteur_agent_program(percepts, actuators):
    actions = []

    gs = {
        'game-board': percepts['game-board-sensor'],
        'player-turn': percepts['turn-taking-indicator'],
        'mining-state': percepts['can-mine-sensor'],
        'player-cards': percepts['cards-in-hand-sensor'],
        'reported-cards': percepts['reported-cards-sensor'],
        'cards-played': percepts['cards-played-sensor']
    }

    board = gs['game-board']
    legal_moves = se.get_legal_actions

    # Dictionary of cards played by each player
    # Dictionary of players and suspected saboteur
    # List of all possible cards, remove what is on the board
    # Dictionary of goal cards we have ruled out
    # Location of gold card
    # List of all legal moves for current gamestate


    # If played Dynamite, and cut path probably Saboteur
    # We will discard Dynamite, or use it in a way that doesn't help the Saboteur, e.g. cut a path to a dead end.

    # Maybe we use a ratio of (PathCards) to (DeadEnds + Dynamite) to determine if played could be Saboteur

    # Prioritise PathCards with more access points for versatility

    # If player suspected of being Saboteur, we will play Sabotage on them

    # If player suspected of being GoldDigger, and player is not mining, play mend on them







    move = random.choice(legal_moves)

    actions.append(move)

    return actions
