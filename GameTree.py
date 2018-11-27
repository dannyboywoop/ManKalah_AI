from gameState import GameState
from PracticeAlphaBeta import AlphaBetaAI
import copy


class Node:
    def __init__(self, game_state, our_player, tree=None):
        self.game_state = game_state
        self.our_player = our_player
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
        return self.game_state.game_over

    def get_children(self):
        if not self.children:
            available_moves = self.game_state.moves_available()
            for move in available_moves:
                new_state = self.game_state.move_result(move)
                self.children[move] = Node(
                    new_state, self.our_player, self.tree)
        return self.children

    def make_root(self):
        self.tree.root = self

    @property
    def payoff(self):
        if self.is_terminal():
            return self.game_state.payoff
        return self.game_state.heuristic_value

    @property
    def is_max_node(self):
        return self.game_state.current_player == self.our_player

    @property
    def node_count(self):
        self.numberOfNodes = 1
        for node in self.children.values():
            self.numberOfNodes += node.node_count
        return self.numberOfNodes


class GameTree:
    def __init__(self):
        self.root = None
        self.ai = AlphaBetaAI(4)

    def calculate_initial_tree(self, our_player):
        if self.root is not None:
            return

        # create root node
        init_state = GameState()
        root = Node(init_state, our_player, self)
        self.root = root

        # for all initial moves
        for child in self.root.get_children().values():
            # calculate subsequent moves
            child.get_children()

            # add swap move
            cloned_state = copy.deepcopy(child.game_state)
            our_new_player = (child.our_player + 1) % 2
            child.children[-1] = Node(cloned_state, our_new_player, self)

    def make_move(self, index):
        self.root.children[int(index)].make_root()

    @property
    def is_our_turn(self):
        return self.root.is_max_node

    @property
    def best_move(self):
        move, next_state, expected_value = self.ai.choose_move(self)
        return move

    def __str__(self):
        return self.root.__str__()


if __name__ == "__main__":
    game_tree = GameTree()
    game_tree.calculate_initial_tree(0)

    print(game_tree)
