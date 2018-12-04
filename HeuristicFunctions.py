from GameState import GameState
from HeuristicComp import HeuristicCompTree


def num_stones_our_side(game_state: GameState, player: int) -> int:
    def get_board_index(hole_index):
        return game_state.hole_index(hole_index, player)

    seed_total = 0
    for hole_index in range(1, 8):
        board_index = get_board_index(hole_index)
        seed_count = game_state.board[board_index]
        seed_total += seed_count
    return seed_total


def num_stones_their_side(game_state: GameState, player: int) -> int:
    opponent = game_state._other_player(player)
    return num_stones_our_side(game_state, opponent)


def our_empty_holes(game_state: GameState, player: int) -> int:
    def get_board_index(hole_index):
        return game_state.hole_index(hole_index, player)

    empty_holes_count = 0
    for hole_index in range(1, 8):
        board_index = get_board_index(hole_index)
        seed_count = game_state.board[board_index]
        if seed_count is 0:
            empty_holes_count += 1

    return empty_holes_count


def their_empty_holes(game_state: GameState, player: int) -> int:
    opponent = game_state._other_player(player)
    return our_empty_holes(game_state, opponent)


def our_vulnerable_holes(game_state: GameState, player: int) -> int:
    non_empty_holes = []
    for hole_index in range(1, 7):
        board_index = game_state.hole_index(hole_index, player)
        seed_count = game_state.board[board_index]
        if seed_count:
            non_empty_holes.append(hole_index)

    opponent = game_state._other_player(player)
    num_vulnerable_holes = 0
    for hole_index in non_empty_holes:
        board_index = game_state.hole_index(hole_index, opponent)
        seed_count = game_state.board[board_index]
        if seed_count is 0:
            num_vulnerable_holes += 1

    return num_vulnerable_holes


def their_vulnerable_holes(game_state: GameState, player: int) -> int:
    opponent = game_state._other_player(player)
    return our_vulnerable_holes(game_state, opponent)


heuristic_functions = [
    num_stones_our_side,
    num_stones_their_side,
    our_empty_holes,
    their_empty_holes,
    our_vulnerable_holes,
    their_vulnerable_holes
]

weights = [
    1,
    1,
    1,
    1,
    1,
    1
]


def heuristic_combinder(functions: list, weights: list):
    def output_function(game_state: GameState, player: int) -> int:
        value = 0
        for index, function in enumerate(functions):
            weight = weights[index]
            value += (weight * function(game_state, player))
        return value
    return output_function


def heuristic_function(weights: list):
    return heuristic_combinder(heuristic_functions, weights)
