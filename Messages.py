"""Contains the StartMessage, ChangeMessage, EndMessage, Move classes"""
import sys

# constants for displaying state as 'pretty' board
ROW_PADDING = " " * 4
BOX_TEMPLATE = "[{:2}]"
ROW_TEMPLATE = ROW_PADDING + (BOX_TEMPLATE * 7)
SCORE_TEMPLATE = BOX_TEMPLATE + (" " * 28) + BOX_TEMPLATE


def as_row(seeds):
    """Returns seeds as pretty row

    Arguments:
    seeds -- list of 7 integers representing one players seeds
    """
    return ROW_TEMPLATE.format(*seeds)


def csv_as_int_list(csv):
    """Returns a comma seperated value as a list

    Arguments:
    csv -- comma separated value eg '1,2,3,4,5'
    """
    return [int(i) for i in csv.split(',') if i.isdigit()]


def as_bytes(string):
    """Converts incoming string into bytes"""
    return string.encode("UTF-8")


class StartMessage:
    """Parses the initial message from the server specifying our player"""
    players = {
        "North": 0,
        "South": 1
    }

    def __init__(self, *args):
        if len(args) != 1:
            raise MessageParseException(
                "Unable to parse `Change` message.\n Args: {}".format(args))
        self.position = args[0]

    def update_game_tree(self, game_tree):
        """Calculates the initial game_tree for our current player"""
        our_player = StartMessage.players[self.position]
        game_tree.calculate_initial_tree(our_player)

    def __str__(self):
        return "START(position={})".format(self.position)


class ChangeMessage:
    """Parses server messages detailing a change to the game state"""
    def __init__(self, *args):
        if len(args) != 3:
            raise MessageParseException(
                "Unable to parse `Change` message.\n Args: {}".format(args))
        self.moveswap = self._parse_index_or_swap(args[0])
        self.state = csv_as_int_list(args[1])
        self.turn = args[2]

    def _parse_index_or_swap(self, arg):
        """takes a MOVESWAP string and converts it an integer representation

        Arguments:
        arg -- a MOVESWAP string
        """
        if arg == "SWAP":
            return -1
        else:
            return int(arg)

    def update_game_tree(self, game_tree):
        """change the root of the game tree based on the move that has
        just been received"""
        game_tree.make_move(self.moveswap)

    def pretty_board(self):
        """Returns `state` as a 'pretty' board"""
        north_score, south_score = self.state[7], self.state[15]
        north_seeds = self.state[6::-1]  # first 7 seeds in reverse order
        south_seeds = self.state[8:15]

        # format data into 'pretty' rows
        north_row = as_row(north_seeds)
        south_row = as_row(south_seeds)
        score_row = SCORE_TEMPLATE.format(north_score, south_score)

        return "{}\n{}\n{}".format(north_row, score_row, south_row)

    def __str__(self):
        return self.pretty_board()


class EndMessage:
    """Parses end of game message"""
    def update_game_tree(self, game_tree=None):
        """Prints termination message before exiting the program"""
        print("End message recieved. Terminating.")
        sys.exit(0)

    def __str__(self):
        return "END"


class Move:
    """Basic move data type"""
    def __init__(self, hole_index):
        self.hole_index = hole_index
        self.is_swap = hole_index == -1

    def message(self):
        """Defines the conversion from the integer representation of
        move to a MOVE message"""
        if self.is_swap:
            return as_bytes("SWAP\n")
        return as_bytes("MOVE;{}\n".format(self.hole_index))


class MessageParseException(Exception):
    """Exception thrown upon failing to parse a message"""
    pass
