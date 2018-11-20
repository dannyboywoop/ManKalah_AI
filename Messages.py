# constants for displaying state as 'pretty' board
row_padding = " " * 4
box_template = "[{:2}]"
row_template = row_padding + (box_template * 7)
score_template = box_template + (" " * 28) + box_template


def as_row(stones):
    """Returns stones as pretty row

    Arguments:
    stones -- list of 7 integers representing one players stones
    """
    return row_template.format(*stones)


def csv_as_list(csv):
    """Returns a comma seperated value as a list

    Arguments:
    csv -- comma separated value eg '1,2,3,4,5'
    """
    return [int(i) for i in args[1].split(',')]


class StartMessage(object):
    def __init__(self, *args):
        if len(args) != 1:
            raise MessageParseException(
                "Unable to parse `Change` message.\n Args: {}".format(args))
        self.position = args[0]

    def __str__(self):
        return "START(position={})".format(self.position)


class ChangeMessage(object):
    def __init__(self, *args):
        if len(args) != 3:
            raise MessageParseException(
                "Unable to parse `Change` message.\n Args: {}".format(args))
        self.moveswap = args[0]
        self.state = csv_as_list(args[1])
        self.turn = args[2]

    def pretty_board(self):
        """Returns `state` as a 'pretty' board"""
        south_score, north_score = self.state[7], self.state[15]
        south_stones = self.state[0:7]
        north_stones = self.state[8:15]

        # format data into 'pretty' rows
        north_row = as_row(north_stones)
        south_row = as_row(south_stones)
        score_row = score_template.format(south_score, north_score)

        return "{}\n{}\n{}".format(south_row, score_row, north_row)

    def __str__(self):
        return self.pretty_board()


class EndMessage(object):
    def __str__(self):
        return "END"


class MessageParseException(Exception):
    pass
