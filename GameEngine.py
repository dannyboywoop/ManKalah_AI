"""Contains the GameEngine class"""
import socket
import sys

from Messages import StartMessage, ChangeMessage, EndMessage, Move
from GameTree import GameTree
import TestHeuristics


MESSAGE_TYPES = {
    "START": StartMessage,
    "CHANGE": ChangeMessage,
    "END": EndMessage
    }


def as_string(data):
    """Converts incoming bytes into string"""
    return data.decode("UTF-8")


class UnknownMessageException(Exception):
    """Exception to throw when unknown message received"""
    pass


class MultipleMessageException(Exception):
    """Exception to throw multiple messages received when
    only one was expected"""
    pass


def parse_message(message):
    """parses message strings into message objects"""
    # can only handle one message at a time
    if '\n' in message:
        raise MultipleMessageException("Trying to parse multiple messages")
    message = message.split(";")
    message_type = message[0]
    args = message[1:]

    message = MESSAGE_TYPES[message_type]

    # if message doesn't conform to protocol, throw exception
    if not message:
        raise UnknownMessageException(
            "Unrecognized message {}".format(message_type))

    # return new instance of message with remaining message arguments
    return message(*args)


class GameEngine:
    """Communicates with the ManKalah server,
    making moves dictated by our AI"""
    def __init__(self, host="localhost"):
        self.host = host
        self.conn = None
        self.data = None

        # defaults
        self.port = 12346
        heuristic = None

        # check for port specified as command line argument
        if len(sys.argv) >= 2:
            if sys.argv[1].isdigit():
                self.port = int(sys.argv[1])

        # check for heuristic specified as a command line argument
        if len(sys.argv) == 3:
            function_module, function_name = sys.argv[2].split(".")
            heuristic = vars(globals()[function_module])[function_name]

        self.game_tree = GameTree(heuristic)

    def run(self):
        """Setups socket and receives incoming messages until socket
        connection is terminated."""
        self._setup_socket()
        while True:
            self._receive_data()
            for message in self._data_as_messages():
                print("Recv: {}".format(message))

                message = parse_message(message)
                print(message)

                message.update_game_tree(self.game_tree)

                if self.game_tree.is_our_turn:
                    self._send_best_move()

    def _send_best_move(self):
        """Finds the current best move to make and sends its to the server"""
        # get the best move from the GameTree
        best_move = self.game_tree.best_move

        # convert the move index to a move message
        move = Move(best_move)
        if move.is_swap:
            self.game_tree.make_move(-1)

        # send move message
        self.conn.sendall(move.message())

    def _setup_socket(self):
        """Setup socket and wait for connection"""
        with socket.socket() as soc:
            soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            soc.bind((self.host, self.port))
            soc.listen()
            self.conn, _ = soc.accept()
            print("New connection accepted.")

    def _receive_data(self):
        """Wait for and receive incoming data"""
        self.data = self.conn.recv(1024).strip()
        self._abort_if_empty_data()

    def _abort_if_empty_data(self):
        """Exits whole program if empty data is received.
        Empty data is a termination message."""
        if not self.data:
            print("Empty message received. Terminating program.")
            sys.exit(0)

    def _data_as_messages(self):
        """Splits incoming data into separate message.
        This handles the situation where we receive mutliple
        messages at once."""
        return as_string(self.data).split("\n")


if __name__ == "__main__":
    GameEngine().run()
