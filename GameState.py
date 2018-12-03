"""Contains the GameState class"""
import copy


# constants for 7,7 Kalah
HOLES = 7
SEEDS = 7


class GameState:
    """
    Stores the state of a kalah game, with
    methods to determine subsequent states
    """

    def __init__(self, heuristic=None):
        """Sets up game board and selects South as the first player"""
        self.board = ([SEEDS] * HOLES + [0]) * 2
        self.current_player = 1
        self.game_over = False
        self.first_turn = True
        self.score_holes = [HOLES, 2 * HOLES + 1]  # indices of score holes
        self.heuristic = heuristic

    def _other_player(self, player=None):
        """given the name of one player, returns the name of the other"""
        if player is None:
            player = self.current_player
        return (player + 1) % 2

    def _opponents_score_hole(self):
        """return index of opponents score hole"""
        return self.score_holes[self._other_player()]

    def _players_score_hole(self):
        """return index of current players score hole"""
        return self.score_holes[self.current_player]

    def hole_index(self, hole, player=None):
        """converts a player's hole number [1-7] into a board index"""
        if player is None:
            player = self.current_player

        # check in range
        if hole < 1 or hole > HOLES:
            raise Exception("Index out of range")

        return player * (HOLES + 1) + hole - 1

    def _give_remaining_seeds_to_player(self, player=None):
        """gives all remaining seeds on the board to one player

        Arguments:
        player -- the number of the player that should receive the seeds"""
        if player is None:
            player = self.current_player

        # get current scores
        final_scores = list(self.scores())

        # calculate number of remaining seeds
        seeds_remaining = 2 * SEEDS * HOLES - final_scores[0] - final_scores[1]

        # calculate scores after remaining seeds have been distributed
        final_scores[player] += seeds_remaining

        # set final board state
        self.board = [0] * 7 + [final_scores[0]] + [0] * 7 + [final_scores[1]]

    def get_value(self, player):
        """returns the value (heuristic or absolute) of the state to
        a given player"""
        if not self.game_over and self.heuristic:
            return self.heuristic(self, player)
        opponent_score = self.scores()[self._other_player(player)]
        return self.scores()[player] - opponent_score

    def moves_available(self, player=None):
        """returns a list of available moves"""
        if player is None:
            player = self.current_player

        moves = []

        # for each of the current player's holes, check if it contains seeds
        for i in range(1, HOLES + 1):
            if self.board[self.hole_index(i, player)] > 0:
                # if so, hole is a valid move
                moves += [i]

        # return list of valid moves
        return moves

    def scores(self):
        """returns a tuple of player scores: (North's score, South's score)"""
        return self.board[self.score_holes[0]], self.board[self.score_holes[1]]

    def move_result(self, pos):
        """returns the resultant gameState after a given move

        Arguments:
        pos -- number [1-7] of the hole to select when making a move
        """

        # get board index of selected hole
        selected_pos = self.hole_index(pos)

        # get number of seeds in selected hole, check there's atleast 1
        num_of_seeds = self.board[selected_pos]
        if num_of_seeds < 1:
            raise Exception("Not a legal move!")

        # create a new state as a deep copy of the current one
        new_state = copy.deepcopy(self)

        # take seeds from selected hole
        new_state.board[selected_pos] = 0

        # place seeds in subsequent holes (ignoring opponents score hole)
        while num_of_seeds > 0:
            # move around the board
            selected_pos += 1

            # if end is reached go back to the start
            if selected_pos == len(new_state.board):
                selected_pos = 0

            # if not opponents score hole, deposit a seed
            if selected_pos != new_state._opponents_score_hole():
                new_state.board[selected_pos] += 1
                num_of_seeds -= 1

        # check if landed on own hole
        performed_capture = False
        if (new_state.hole_index(1) <= selected_pos <=
                new_state.hole_index(HOLES)):
            # if so check if it has only 1 seed and the opposite hole is empty
            opposite_pos = 2 * HOLES - selected_pos
            seeds_in_current_pos = new_state.board[selected_pos]
            seeds_in_opposite_pos = new_state.board[opposite_pos]
            if seeds_in_current_pos == 1 and seeds_in_opposite_pos > 0:
                performed_capture = True
                new_state.board[selected_pos] = 0
                new_state.board[opposite_pos] = 0
                new_state.board[new_state._players_score_hole()] += (
                    1 + seeds_in_opposite_pos
                )

        # check for game over
        for player in range(0, 2):
            # if one of the player's sides is empty
            if not new_state.moves_available(player):
                # give the remaining seeds to the other player
                new_state._give_remaining_seeds_to_player(
                    new_state._other_player(player))

                # game over
                new_state.game_over = True

        # change current player if turn is over
        if (selected_pos != new_state._players_score_hole() or
                self.first_turn or performed_capture):
            new_state.first_turn = False
            new_state.current_player = self._other_player()

        # return resultant state
        return new_state
