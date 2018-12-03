"""contains a few basic heuristic functions"""
import random

from HeuristicComp import HeuristicCompTree
from GameStats import GameStatsArray

def bad_heuristic(game_state, player):
    """arbitrary heuristic, no useful informational content"""
    return random.randint(1,98)
    # return game_state.board[game_state.hole_index(2, player)]


def test_heuristic1(game_state, player):
    # weight1 = [1, 1, -1, 1]
    """returns the difference in score between the two players"""
    opponent_score = game_state.scores()[game_state._other_player(player)]

    player_advantage = game_state.scores()[player] - opponent_score
    close_to_win_player = game_state.scores()[player] / 50
    close_to_win_opponent = opponent_score / 50

    """ Number of holes that will end in my scoring well - 1
    Hence preparing the game to make more go-again moves """
    go_again_holes_num = 0
    for i in range(1, 7):
        if game_state.board[game_state.hole_index(i, player)] - 7 - i == 0:
            go_again_holes_num += 1

    """Number of stones on player's side"""
    total_stones_player = 0
    for i in range(1, 7):
        total_stones_player += game_state.board[game_state.hole_index(i, player)]



    return weight1[0] * player_advantage \
           + weight1[1] * close_to_win_player \
           + weight1[2] * close_to_win_opponent \
           + weight1[3] * go_again_holes_num


def test_heuristic2(game_state, player):
    # weight2 = [1, 1, -1, 1]
    """returns the difference in score between the two players"""
    opponent_score = game_state.scores()[game_state._other_player(player)]

    player_advantage = game_state.scores()[player] - opponent_score
    close_to_win_player = game_state.scores()[player] / 50
    close_to_win_opponent = opponent_score / 50

    """ Number of holes that will end in my scoring well - 1
    Hence preparing the game to make more go-again moves """
    go_again_holes_num = 0
    for i in range(1, 7):
        if game_state.board[game_state.hole_index(i, player)] - 7 - i == 0:
            go_again_holes_num += 1

    """Number of stones on player's side"""
    total_stones_player = 0
    for i in range(1, 7):
        total_stones_player += game_state.board[game_state.hole_index(i, player)]

    return weight2[0] * player_advantage \
           + weight2[1] * close_to_win_player \
           + weight2[2] * close_to_win_opponent \
           + weight2[3] * go_again_holes_num


def avg_wins(game_stats_arr):
    total_matches = len(game_stats_arr)
    wins_north = len([el for el in game_stats_arr if el.result[0] > el.result[1]]) / total_matches * 100
    wins_south = len([el for el in game_stats_arr if el.result[0] < el.result[1]]) / total_matches * 100
    return wins_north, wins_south


def avg_second_player_wins_swap(game_stats_arr):
    total_swaps = len([el for el in game_stats_arr if el.swap])
    second_player_wins_swap = len([el for el in game_stats_arr if el.swap and (el.result[0] > el.result[1])])
    second_player_wins_swap_perc = 0
    if total_swaps != 0:
        second_player_wins_swap_perc = second_player_wins_swap / total_swaps * 100
    avg_swaps_perc = total_swaps / len(game_stats_arr) * 100
    return second_player_wins_swap_perc, avg_swaps_perc


def get_avg_nodes_searched(game_stats_arr):
    return sum(el.avg_nodes_searched for el in game_stats_arr) / len(game_stats_arr) * 100


# TODO: heuristic functions should accept weight as parameters
if __name__ == "__main__":
    weight1 = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
    weight2 = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
    for j in range(100):
        game_stats_array = GameStatsArray()
        for i in range(1):
            tree = HeuristicCompTree(test_heuristic1, test_heuristic2, 4)
            tree.run_game()
            game_stats_array.append(tree.game_stats)

        """Get average of wins"""
        wins_north, wins_south = game_stats_array.avg_wins()
        print(game_stats_array)
        if wins_south > wins_north:
            weight1 = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
        else:
            weight2 = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]

    print("FINAL WEIGHTS")
    print("Weight NORTH: " + "{} ".format(weight1))
    print("Weight SOUTH: " + "{} ".format(weight2))
