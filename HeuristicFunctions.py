from GameState import GameState


def player_empty_holes(game_state: GameState, player: int) -> int:
    def get_board_index(hole_index):
        return game_state.hole_index(hole_index, player)

    empty_holes_count = 0
    for hole_index in range(1, 8):
        board_index = get_board_index(hole_index)
        seed_count = game_state.board[board_index]
        if seed_count is 0:
            empty_holes_count += 1

    return empty_holes_count


def opponent_empty_holes(game_state: GameState, player: int) -> int:
    opponent = game_state._other_player(player)
    return player_empty_holes(game_state, opponent)


def heuristic_combinder(functions: list, weights: list):
    if len(functions) != len(weights):
        raise Exception()
    
    def foo(game_state: GameState, player: int) -> int:
        output = 0
        for index, function in enumerate(functions):
            weight = weights[index]
            output += (weight * function(game_state, player))
        return output
    
    return foo

def test_heuristic(game_state, player):
    """returns the difference in score between the two players"""
    opponent_score = game_state.scores()[game_state._other_player(player)]
    return game_state.scores()[player] - opponent_score

heuristic = heuristic_combinder(
    [player_empty_holes, opponent_empty_holes, test_heuristic],
    [1, 1, 1]
)

from HeuristicComp import HeuristicCompTree



if __name__ == "__main__":
    HeuristicCompTree(heuristic, test_heuristic).run_game()

