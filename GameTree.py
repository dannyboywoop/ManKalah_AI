"""Contains the Node and GameTree classes"""
import copy
from GameState import GameState
from AlphaBetaAI import AlphaBetaAI


class Node:
    """stores a GameState and a dictionary of possible subsequent states
    that can be reached"""
    def __init__(self, game_state, our_player, tree=None):
        self.game_state = game_state
        self.our_player = our_player
        self.children = {}
        self.tree = tree
        self.tree.nodes_in_memory += 1

    def get_value(self):
        """returns the value of the GameState to our player"""
        return self.game_state.get_value(self.our_player)

    def is_terminal(self):
        """returns true if the node has no possible children
        i.e. it is a game-over node"""
        return self.game_state.game_over

    def get_children(self):
        """returns the dictionary of child nodes for the node,
        calculating them if necessary"""
        if not self.children:
            available_moves = self.game_state.moves_available()
            for move in available_moves:
                new_state = self.game_state.move_result(move)
                self.children[move] = Node(
                    new_state, self.our_player, self.tree)
        return self.children

    def make_root(self):
        """makes the node the new root of its GameTree"""
        self.tree.root = self

    def __del__(self):
        self.tree.nodes_in_memory -= 1

    @property
    def is_max_node(self):
        """returns true if the node stores a GameState in which it is our
        player's turn"""
        return self.game_state.current_player == self.our_player


class GameTree:
    """class for storing a game tree and making decisions based on the tree"""
    def __init__(self):
        self.root = None
        self.nodes_in_memory = 0
        self.ai = AlphaBetaAI(5)

    def calculate_initial_tree(self, our_player):
        """calculates the initial root node and descendant nodes of
        the tree up to a depth of 2.
        Adds choices to relevant nodes to implement the pie rule"""
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
        """moves the root of the tree to the node determined by the move index;
        all nodes no longer in the tree are destroyed."""
        self.root.get_children()
        self.root.children[index].make_root()

    @property
    def is_our_turn(self):
        """returns true if it is our player's turn in the state stored at the
        root fo the tree"""
        return self.root.is_max_node

    @property
    def best_move(self):
        """searches for and returns the best move available from
        the root node of the tree"""
        move, _, _ = self.ai.choose_move(self)
        print("{} node(s) in memory".format(self.nodes_in_memory))
        return move
