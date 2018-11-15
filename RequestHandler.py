import socketserver

# TODO: add board formatting
# TODO: add response sending


def as_bytes(string):
    return string.encode("UTF-8")


def as_string(data):
    return data.decode("UTF-8")


class MessageParseException(BaseException):
    pass


class UnknownMessageException(BaseException):
    pass


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
        return "CHANGE (moveswap={}, state={}, turn={})".format(self.moveswap, self.state, self.turn)


class EndMessage(object):
    def __str__(self):
        return "END"


class InputParser(object):
    message_types = {
        "START": StartMessage,
        "CHANGE": ChangeMessage,
        "END": EndMessage
    }

    def __init__(self, message):
        message = message.split(";")
        self.message_type = message[0]
        self.args = message[1:]

    def get_message(self):
        message = InputParser.message_types[self.message_type]

        if not message:
            raise UnknownMessageException("Unrecognized message {}".format(self.message_type))

        return message(*self.args)


class RequestHandler(socketserver.BaseRequestHandler):
    def get_user_input(self):
        return as_bytes(input() + "\n")

    def parse_message(self):
        data = as_string(self.data)
        return InputParser(data).get_message()

    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                break
            print("Recv: {}".format(self.data))

            message = self.parse_message()
            print(message)

            self.request.sendall(self.get_user_input())


class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    HOST, PORT = "localhost", 12346
    server = ReuseAddrTCPServer((HOST, PORT), RequestHandler)
    server.serve_forever()
