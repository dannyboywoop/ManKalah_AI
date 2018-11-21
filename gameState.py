import copy


# constants for 7,7 Kalah
HOLES = 7
SEEDS = 7


class GameState:
    """
    Stores the state of a kalah game, with
    methods to determine subsequent states
    """
    players = {
        "North": 0,
        "South": 1
    }

    def __init__(self):
        """Sets up game board and selects South as the first player"""
        self.board = [SEEDS] * HOLES + [0] + [SEEDS] * HOLES + [0]
        self.current_player = "South"
        self.game_over = False
        self.first_turn = True
        self.score_holes = [HOLES, 2 * HOLES + 1]  # indices of score holes
        return

    def _opponents_score_hole(self):
        """return index of opponents score hole"""
        opponents_player_number = (self.players[self.current_player] + 1) % 2
        return self.score_holes[opponents_player_number]

    def _players_score_hole(self):
        """return index of current players score hole"""
        return self.score_holes[self.players[self.current_player]]

    def _hole_index(self, hole, player=None):
        """converts a player's hole number [1-7] into a board index"""
        if player is None:
            player = self.current_player

        # check in range
        if (hole < 1 or hole > HOLES):
            raise Exception("Index out of range")

        return self.players[player] * (HOLES + 1) + hole - 1

    def _other_player(self, player=None):
        """given the name of one player, returns the name of the other"""
        if player is None:
            player = self.current_player
        if player == "North":
            return "South"
        if player == "South":
            return "North"

    def clone_server_state(self, board, current_player):
        """clones server state

        Arguments:
        board -- list of ints representing the number of seeds in each hole
        current_player -- the name of the player who's turn it is
        """
        # check current_player name is a valid option
        if current_player not in self.players.keys():
            raise Exception("Invalid player")

        # check the server state has the corrent number of holes
        if (len(board) != 2 * (HOLES + 1)):
            raise Exception("Invalid board size")

        # copy server state
        self.board = board
        self.current_player = current_player

    def moves_available(self):
        """returns a list of available moves"""
        moves = []

        # for each of the current player's holes, check if it contains seeds
        for i in range(1, HOLES + 1):
            if (self.board[self._hole_index(i)] > 0):
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
        selected_pos = self._hole_index(pos)

        # get number of seeds in selected hole, check there's atleast 1
        num_of_seeds = self.board[selected_pos]
        if (num_of_seeds < 1):
            raise Exception("Not a legal move!")

        # create a new state as a deep copy of the current one
        new_state = copy.deepcopy(self)

        # take seeds from selected hole
        new_state.board[selected_pos] = 0

        # place seeds in subsequent holes (ignoring opponents score hole)
        while (num_of_seeds > 0):
            # move around the board
            selected_pos += 1

            # if end is reached go back to the start
            if (selected_pos == len(new_state.board)):
                selected_pos = 0

            # if not opponents score hole, deposit a seed
            if selected_pos != new_state._opponents_score_hole():
                new_state.board[selected_pos] += 1
                num_of_seeds -= 1

        # check if landed on own hole
        performed_capture = False
        if (new_state._hole_index(1)
                <= selected_pos
                <= new_state._hole_index(HOLES)):
            # if so check if it has only 1 seed and the opposite hole is empty
            opposite_pos = 2 * HOLES - selected_pos
            seeds_in_current_pos = new_state.board[selected_pos]
            seeds_in_opposite_pos = new_state.board[opposite_pos]
            if (seeds_in_current_pos == 1 and seeds_in_opposite_pos > 0):
                performed_capture = True
                new_state.board[selected_pos] = 0
                new_state.board[opposite_pos] = 0
                new_state.board[new_state._players_score_hole()] += (
                        1 + seeds_in_opposite_pos
                )

        # check for game over (currentPlayers side is now empty)
        if (len(new_state.moves_available()) == 0):
            # read opponents score
            opponents_final_score = new_state.board[
                    new_state._opponents_score_hole()]

            # current player gets all remaining seeds
            current_players_final_score = (SEEDS * HOLES * 2
                                           - opponents_final_score
                                           )

            # set all board values to 0
            new_state.board = [0] * (2 * HOLES + 2)

            # set final scores
            new_state.board[new_state._opponents_score_hole()]\
                = opponents_final_score
            new_state.board[new_state._players_score_hole()]\
                = current_players_final_score

            # game over
            new_state.game_over = True

        # change current player if turn is over
        if (selected_pos != new_state._players_score_hole()
                or self.first_turn
                or performed_capture):
            new_state.first_turn = False
            new_state.current_player = self._other_player()

        # return resultant state
        return new_state
