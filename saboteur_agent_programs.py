

def saboteur_agent_program(percepts, actuators):
    actions = []
    player_turn = percepts['turn-taking-indicator']

    game_state = {
        'game-board': percepts['game-board-sensor'],
        'power-up-Y': percepts['powerups-sensor']['Y'],
        'power-up-R': percepts['powerups-sensor']['R'],
        'player-turn': percepts['turn-taking-indicator']
    }

    # If first move, release in middle columns
    if move == 0:
        start_moves = ["release-2", "release-3", "release-4"]
        actions.append(random.choice(start_moves))
        move = move + 1
        return actions

    if not ConnectFourEnvironment.is_terminal(game_state):
        tic = time.time()
        root_node = MCTSGraphNode(game_state, None, None)
        best_move = mcts(root_node, player_turn)
        toc = time.time()
        print("[MTCS (player {0})] Elapsed (sec): {1:.6f}".format(player_turn, toc - tic))
        if best_move is not None:
            actions.append(best_move)

    return actions