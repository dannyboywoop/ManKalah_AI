class StartMessage(object):
    def __init__(self, *args):
        if len(args) != 1:
            raise MessageParseException("Unable to parse `Start` message")
        self.position = args[0]

    def __str__(self):
        return "START(position={})".format(self.position)


class ChangeMessage(object):
    def __init__(self, *args):
        if len(args) != 3:
            raise MessageParseException("Unable to parse `Change` message")
        self.moveswap = args[0]
        self.state = args[1]
        self.turn = args[2]

    def __str__(self):
        return "CHANGE (moveswap={}, state={}, turn={})".format(
            self.moveswap, self.state, self.turn)


class EndMessage(object):
    def __str__(self):
        return "END"