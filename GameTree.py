from gameState import GameState
from PracticeAlphaBeta import AlphaBetaAI


class Node:
    def __init__(self, game_state, is_max_node, tree=None):
        self.game_state = game_state
        self.is_max_node = is_max_node
        self.children = {}
        self.tree = tree

    def __str__(self, level=0, move=""):
        left_padding = " " * 2 * level
        output = left_padding + move + "\n" + str(self.game_state) + "\n"
        for key, child in self.children.items():
            output += child.__str__(level+1, str(key)+": ")
        return output

    # TODO: implement and move to `GameState`
    def getValue(self):
        return 100

    def is_terminal(self):
        return len(self.children) == 0

    def calculate_children(self, depth=1):
        if not self.children:
            available_moves = self.game_state.moves_available()
            for move in available_moves:
                new_state = self.game_state.move_result(move)
                is_max_node = new_state.current_player == "North"  # TODO: relate this to our player
                self.children[move] = Node(new_state, is_max_node, self.tree)

    def make_root(self):
        self.tree.root = self

    @property
    def payoff(self):
        if self.is_terminal():
            return self.game_state.payoff
        return self.game_state.heuristic_value

    @property
    def node_count(self):
        self.numberOfNodes = 1
        for node in self.children.values():
            self.numberOfNodes += node.node_count
        return self.numberOfNodes

players = {
    "North": 0,
    "South": 1
}


class GameTree:
    def __init__(self, root):
        root.tree = self
        self.root = root
        self.our_player = None
        self.current_turn = 1
        self.ai = AlphaBetaAI(4)

    def calculate_children(self, depth=1):
        current_queue = [self.root]
        next_queue = []

        for current_depth in range(depth):
            while current_queue:
                current_node = current_queue.pop()
                current_node.calculate_children()

                is_not_final_loop = current_depth != (depth - 1)
                if is_not_final_loop:
                    next_queue += list(current_node.children.values())

            current_queue = next_queue
            next_queue = []

    def make_move(self, index):
        # TODO: tidy up code & fix `current_player` indices
        self.root.children[int(index)].make_root()
        self.calculate_children(4)
        self.current_turn = players[self.root.game_state.current_player]

    @property
    def is_our_turn(self):
        return self.our_player == self.current_turn

    @property
    def best_move(self):
        move, next_state, expected_value = self.ai.choose_move(self)
        return move

    def __str__(self):
        return self.root.__str__()
