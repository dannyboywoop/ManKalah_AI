"""Contains variants on Node and GameTree classes for use in HeuristicComp"""
import copy
from GameState import GameState
from AlphaBetaAI import AlphaBetaAI


class SharedNode:
    """stores a GameState and a dictionary of possible subsequent states
    that can be reached"""
    def __init__(self, game_state, tree=None):
        self.game_state = game_state
        self.children = {}
        self.tree = tree
        self.tree.nodes_in_memory += 1

    def get_value(self):
        """returns the value of the GameState to root node player"""
        if self.is_terminal():
            return self.game_state.scores()[self.root_current_player]
        else:
            return self.tree.heuristics[self.root_current_player](
                self.game_state, self.root_current_player)

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
                self.children[move] = SharedNode(
                    new_state, self.tree)
        return self.children

    def make_root(self):
        """makes the node the new root of its GameTree"""
        self.tree.root = self

    def __del__(self):
        self.tree.nodes_in_memory -= 1

    @property
    def root_current_player(self):
        return self.tree.root.game_state.current_player

    @property
    def is_max_node(self):
        """returns true if the node stores a GameState
        is the same as the root node"""
        return (self.game_state.current_player == self.root_current_player)


class HeuristicCompTree:
    """class for storing a game tree shared by both players
    with methods making decisions for both players based on the tree"""
    def __init__(self, north_heuristic, south_heuristic):
        self.root = None
        self.nodes_in_memory = 0
        self.ai = AlphaBetaAI(5)
        self.heuristics = [north_heuristic, south_heuristic]
        self._calculate_initial_tree()

    def _calculate_initial_tree(self):
        """calculates the initial root node and descendant nodes of
        the tree up to a depth of 2.
        Adds choices to relevant nodes to implement the pie rule"""
        if self.root is not None:
            return

        # create root node
        init_state = GameState()
        root = SharedNode(init_state, self)
        self.root = root

        # for all initial moves
        for child in self.root.get_children().values():
            # calculate subsequent moves
            child.get_children()

            # add swap move
            swap_state = copy.deepcopy(child.game_state)
            swap_state.board = swap_state.board[8:] + swap_state.board[:8]
            swap_state.current_player = (swap_state.current_player + 1) % 2
            child.children[-1] = SharedNode(swap_state, self)

    def runGame(self):
        while not self.root.is_terminal():
            self.make_move(self.best_move)
        result = self.root.game_state.scores()
        print("Game Over!")
        print("Results: {} {}".format(result[0], result[1]))

    def make_move(self, index):
        """moves the root of the tree to the node determined by the move index;
        all nodes no longer in the tree are destroyed."""
        self.root.get_children()
        self.root.children[index].make_root()

    @property
    def best_move(self):
        """searches for and returns the best move available from
        the root node of the tree"""
        move, _, _ = self.ai.choose_move(self)
        print("{} SharedNode(s) in memory".format(self.nodes_in_memory))
        return move
