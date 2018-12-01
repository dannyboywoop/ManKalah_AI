"""contains a few basic heuristic functions"""


from HeuristicComp import HeuristicCompTree


def bad_heuristic(game_state, player):
    """arbitrary heuristic, no useful informational content"""
    return game_state.board[game_state.hole_index(2, player)]


def test_heuristic(game_state, player):
    """returns the difference in score between the two players"""
    opponent_score = game_state.scores()[game_state._other_player(player)]
    return game_state.scores()[player] - opponent_score

if __name__ == "__main__":
    HeuristicCompTree(bad_heuristic, test_heuristic).runGame()
