from GameState import GameState


class GameStatsArray:
    def __init__(self):
        self.game_stats_array = []

    def append(self, game_stats):
        self.game_stats_array.append(game_stats)

    def avg_wins(self):
        total_matches = len(self.game_stats_array)
        wins_north = len([el for el in self.game_stats_array if el.result[0] > el.result[1]]) / total_matches * 100
        wins_south = len([el for el in self.game_stats_array if el.result[0] < el.result[1]]) / total_matches * 100
        return wins_north, wins_south

    def avg_swap_stats(self):
        total_swaps = len([el for el in self.game_stats_array if el.swap])
        second_player_wins_swap = len([el for el in self.game_stats_array if el.swap and (el.result[0] > el.result[1])])
        second_player_wins_swap_perc = 0
        if total_swaps != 0:
            second_player_wins_swap_perc = second_player_wins_swap / total_swaps * 100
        avg_swaps_perc = total_swaps / len(self.game_stats_array) * 100
        return second_player_wins_swap_perc, avg_swaps_perc

    def get_avg_nodes_searched(self):
        return sum(el.avg_nodes_searched for el in self.game_stats_array) / len(self.game_stats_array) * 100

    @property
    def total_matches(self):
        return len(self.game_stats_array)

    def __str__(self):
        """Get averages"""
        wins_north, wins_south = self.avg_wins()
        second_player_wins_swap_perc, avg_swaps_perc = self.avg_swap_stats()
        avg_nodes_searched = self.get_avg_nodes_searched()
        return "Total matches: {}".format(self.total_matches)\
            + "AVG WINS: NORTH: {:.2f} SOUTH: {:.2f}".format(wins_north, wins_south)\
            + "AVG North wins with swap on total swaps: {:.2f}".format(second_player_wins_swap_perc)\
            + "AVG swaps: {:.2f}".format(avg_swaps_perc)\
            + "AVG nodes searched: {}".format(avg_nodes_searched)


class GameStats:
    players = {
        0: "North",
        1: "South"
    }

    _previous_game_state: GameState

    # TODO: store the number as an array to do the average
    def __init__(self):
        self.first_move = None
        self.first_turn_player = None
        self.swap = False
        self.tot_go_again_moves = [0, 0]
        self.max_go_again_consecutive_moves = [1, 1]
        self.avg_go_again_consecutive_moves = [0, 0]
        self.tot_captures = [0, 0]
        self.avg_capture_score = [0, 0]
        self.tot_moves = 0
        self._sum_nodes_searched = 0
        self._player_in_previous_turn = None
        self._consecutive_move_count = 1
        self._previous_game_state = None
        self.result = None

    @property
    def swap_triggering_move(self):
        if self.swap:
            return self.first_move
        else:
            return None

    def perform_swap(self):
        # print("Performing swap")
        self.swap = True
        self._player_in_previous_turn = None

    def _is_capture_move(self, game_state):
        """
        Check whether this move is a capture move or not
        :type game_state: GameState
        """
        player_current = game_state.current_player
        if self._player_in_previous_turn == player_current:
            score_difference = game_state.board[game_state._players_score_hole()] \
                               - self._previous_game_state.board[self._previous_game_state._players_score_hole()]
        else:
            score_difference = game_state.board[game_state._players_score_hole()] \
                - self._previous_game_state.board[self._previous_game_state._opponents_score_hole()]
        # print("Score difference: {}".format(score_difference))
        # if it is not a go-again move and the difference in the score between two
        # states is greater than one seed, then it is capture move
        # print("Player: curr {} and prev {}".format(player_current, self._previous_game_state.current_player))
        if score_difference > 1:
            # print("Capture performed")
            self.tot_captures[player_current] += 1
            if self.avg_capture_score[player_current] != 0:
                self.avg_capture_score[player_current] = self.avg_capture_score[player_current] + score_difference / 2
            else:
                self.avg_capture_score[player_current] = score_difference

    def move(self, game_state, index, nodes_searched):
        """
        Get information from the current move of the player

        :type game_state: GameState
        """

        player = game_state.current_player
        self.tot_moves += 1

        self._sum_nodes_searched += nodes_searched

        # This is the first move
        if self._previous_game_state is None and self._player_in_previous_turn is None:
            self.first_move = index
            self.first_turn_player = self.players.get(player)
            self._previous_game_state = game_state

        # This might also be the case when a swap has been performed, and I do not want to keep track
        # of the previous move since the gameState does not keep track of the actual player
        if self._player_in_previous_turn is None:
            self._player_in_previous_turn = player
            # print("Exiting function")
            return

        self._is_capture_move(game_state)
        self._previous_game_state = game_state

        if self._player_in_previous_turn == player:
            self.tot_go_again_moves[player] += 1
            self._consecutive_move_count += 1
        else:
            if self.max_go_again_consecutive_moves[player] < self._consecutive_move_count:
                self.max_go_again_consecutive_moves[player] = self._consecutive_move_count
            self.avg_go_again_consecutive_moves[player] = \
                    (self.avg_go_again_consecutive_moves[player] + self._consecutive_move_count) / 2
            self._consecutive_move_count = 1
            self._player_in_previous_turn = player

    @property
    def avg_nodes_searched(self):
        return self._sum_nodes_searched / self.tot_moves

    def __str__(self):
        result = self.result
        if self.swap:
            self.tot_go_again_moves.reverse()
            self.max_go_again_consecutive_moves.reverse()
            self.avg_go_again_consecutive_moves.reverse()
            self.tot_captures.reverse()
            self.avg_capture_score.reverse()
            result = (self.result[1], self.result[0])
            self.result = result
        return "First move: {}\n".format(self.first_move) \
               + "First turn player: {}\n".format(self.first_turn_player) \
               + "Swap needed? {}\n".format(self.swap) \
               + "Swap triggering move: {}\n".format(self.swap_triggering_move) \
               + ("Total go-again moves:" + " {}" * 2 + "\n").format(*self.tot_go_again_moves) \
               + ("Max go-again consecutive moves:" + " {}" * 2 + "\n").format(*self.max_go_again_consecutive_moves) \
               + ("Avg go-again consecutive moves:" + " {}" * 2 + "\n").format(*self.avg_go_again_consecutive_moves) \
               + ("Total captures:" + " {}" * 2 + "\n").format(*self.tot_captures) \
               + ("Avg captured score:" + " {}" * 2 + "\n").format(*self.avg_capture_score) \
               + "Avg nodes searched: {}\n".format(self.avg_nodes_searched) \
               + "Total moves: {}\n".format(self.tot_moves) \
               + "Result: North {} South {}\n".format(*result)
