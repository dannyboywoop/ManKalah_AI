from GameState import GameState
from PracticeAlphaBeta import AlphaBetaAI
import copy


class Node:
    def __init__(self, game_state, our_player, tree=None):
        self.game_state = game_state
        self.our_player = our_player
        self.children = {}
        self.tree = tree
        self.tree.nodes_in_memory += 1

    def get_value(self):
        return self.game_state.get_value(self.our_player)

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

    def __del__(self):
        self.tree.nodes_in_memory -= 1

    @property
    def is_max_node(self):
        return self.game_state.current_player == self.our_player


class GameTree:
    def __init__(self):
        self.root = None
        self.nodes_in_memory = 0
        self.ai = AlphaBetaAI(5)

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
        self.root.get_children()
        self.root.children[index].make_root()

    @property
    def is_our_turn(self):
        return self.root.is_max_node

    @property
    def best_move(self):
        move, _, _ = self.ai.choose_move(self)
        print("{} node(s) in memory".format(self.nodes_in_memory))
        return move
