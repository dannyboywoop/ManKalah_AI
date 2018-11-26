import socket
import sys

from Messages import StartMessage, ChangeMessage, EndMessage
from GameTree import GameTree, Node
from gameState import GameState


def as_string(data):
    """Converts incoming bytes into string"""
    return data.decode("UTF-8")


def as_bytes(string):
    """Converts incoming string into bytes"""
    return string.encode("UTF-8")


class UnknownMessageException(Exception):
    pass


class MultipleMessageException(Exception):
    pass


class InputParser:
    """Handles parsing message strings into message objects"""
    message_types = {
        "START": StartMessage,
        "CHANGE": ChangeMessage,
        "END": EndMessage
    }

    def __init__(self, message):
        # can only handle one message at a time
        if '\n' in message:
            raise MultipleMessageException("Trying to parse multiple messages")
        message = message.split(";")
        self.message_type = message[0]
        self.args = message[1:]

    def get_message(self):
        message = InputParser.message_types[self.message_type]

        # if message doesn't conform to protocol, throw exception
        if not message:
            raise UnknownMessageException(
                "Unrecognized message {}".format(self.message_type))

        # return new instance of message with remaining message arguments
        return message(*self.args)


class GameEngine:
    def __init__(self, game_tree, host="localhost", port=12346):
        self.host = host
        self.port = port
        self.game_tree = game_tree

    def run(self):
        """Setups socket and receives incoming messages until socket
        connection is terminated."""
        self._setup_socket()
        while True:
            self._receive_data()
            for message in self._data_as_messages():
                print("Recv: {}".format(message))

                message = InputParser(message).get_message()
                print(message)

                message.update_game_tree(self.game_tree)

                if self.game_tree.is_our_turn:
                    best_move = self.game_tree.best_move
                    apples = "MOVE;{}\n".format(best_move)  # TODO: make into own object
                    self.conn.sendall(as_bytes(apples))

    def _setup_socket(self):
        """Setup socket and wait for connection"""
        with socket.socket() as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            self.conn, _ = s.accept()
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
    init_state = GameState()
    root = Node(init_state, True)
    game_tree = GameTree(root)
    game_tree.calculate_children(4)

    GameEngine(game_tree).run()
