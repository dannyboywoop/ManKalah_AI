import sys

# constants for displaying state as 'pretty' board
row_padding = " " * 4
box_template = "[{:2}]"
row_template = row_padding + (box_template * 7)
score_template = box_template + (" " * 28) + box_template


def as_row(seeds):
    """Returns seeds as pretty row

    Arguments:
    seeds -- list of 7 integers representing one players seeds
    """
    return row_template.format(*seeds)


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
        our_player = StartMessage.players[self.position]
        game_tree.calculate_initial_tree(our_player)

    def __str__(self):
        return "START(position={})".format(self.position)


class ChangeMessage:
    def __init__(self, *args):
        if len(args) != 3:
            raise MessageParseException(
                "Unable to parse `Change` message.\n Args: {}".format(args))
        self.moveswap = args[0]
        self.state = csv_as_int_list(args[1])
        self.turn = args[2]

    def update_game_tree(self, game_tree):
        move_index = self.moveswap
        game_tree.make_move(move_index)

    def pretty_board(self):
        """Returns `state` as a 'pretty' board"""
        north_score, south_score = self.state[7], self.state[15]
        north_seeds = self.state[0:7]
        south_seeds = self.state[8:15]

        # format data into 'pretty' rows
        north_row = as_row(north_seeds)
        south_row = as_row(south_seeds)
        score_row = score_template.format(north_score, south_score)

        return "{}\n{}\n{}".format(north_row, score_row, south_row)

    def __str__(self):
        return self.pretty_board()


class EndMessage:
    def update_game_tree(self, game_tree):
        pass

    def __str__(self):
        return "END"


class Move:
    def __init__(self, hole_index):
        self.hole_index = hole_index

    def message(self):
        return as_bytes("MOVE;{}\n".format(self.hole_index))


class MessageParseException(Exception):
    pass
