from GameState import GameState


def our_num_points(game_state: GameState, player: int) -> int:
    return game_state.scores()[player]


def their_num_points(game_state: GameState, player: int) -> int:
    opponent = game_state._other_player(player)
    return our_num_points(game_state, opponent)


def num_our_go_again_turns(game_state: GameState, player) ->int:
    def get_board_index(hole_index):
        return game_state.hole_index(hole_index, player)
    turns_available = 0
    for hole_index in range(1, 8):
        board_index = get_board_index(hole_index)
        if game_state.board[board_index] == (8 - hole_index):
            turns_available += 1
    return turns_available


def num_their_go_again_turns(game_state: GameState, player) ->int:
    oppenont = game_state._other_player(player)

    def get_board_index(hole_index):
        return game_state.hole_index(hole_index, oppenont)

    turns_avalible = 0
    for hole_index in range(1, 8):
        board_index = get_board_index(hole_index)
        if(game_state.board[board_index] == (8-hole_index)):
            turns_avalible += 1
    return turns_avalible


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
    num_vulnerable_holes = 0
    opponent = game_state._other_player(player)
    for hole_index in range(1, 8):
        our_index = game_state.hole_index(hole_index, player)
        their_index = game_state.hole_index(8 - hole_index, opponent)
        
        we_have_seeds = game_state.board[our_index]
        they_dont_have_seeds = not game_state.board[their_index]
        if we_have_seeds and they_dont_have_seeds:
            num_vulnerable_holes += 1

    return num_vulnerable_holes


def their_vulnerable_holes(game_state: GameState, player: int) -> int:
    opponent = game_state._other_player(player)
    return our_vulnerable_holes(game_state, opponent)


heuristic_functions = [

]


def heuristic_combinder(weights: list):
    def output_function(game_state: GameState, player: int) -> int:
        return (
            our_num_points(game_state, player) * weights[0]
            - their_num_points(game_state, player) * weights[1]
            + num_our_go_again_turns(game_state, player) * weights[2]
            - num_their_go_again_turns(game_state, player) * weights[3]
            + (((2 * num_stones_our_side(game_state, player)) - 1) * weights[4])
            + (((2 * num_stones_their_side(game_state, player)) - 1) * weights[5])
            + (((2 * our_empty_holes(game_state, player)) - 1) * weights[6])
            + (((2 * their_empty_holes(game_state, player)) - 1) * weights[7])
            - our_vulnerable_holes(game_state, player) * weights[8]
            + their_vulnerable_holes(game_state, player) * weights[9]
        )
    return output_function


def heuristic_function(weights: list):
    return heuristic_combinder(weights)
