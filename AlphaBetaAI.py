"""Contains the AlphaBetaAI class"""
INF = float('inf')


class AlphaBetaAI:
    """A simple AI that performs a Mini-Max search with Alpha-Beta pruning
    to determine the best move from a given node in a GameTree"""
    def __init__(self, max_depth):
        # maxDepth is the maximum depth of the tree to search
        # before using a heuristic
        self.max_depth = max_depth
        self.nodes_checked = 0

    def choose_move(self, game_tree):
        """Given a game tree, finds the best move from the root node."""
        self.nodes_checked = 0

        evaluation = self.evaluate(game_tree.root, self.max_depth)

        # print("Searching for best move: {} node(s) checked"
        #       .format(self.nodes_checked))

        return evaluation

    def evaluate(self, node, depth_to_search, alpha=-INF, beta=INF):
        """Evaluates the best move from a given node, by determining the values
        of the nodes in the subtree for which the node is the root"""
        self.nodes_checked += 1

        best_move, next_node = None, None

        if depth_to_search == 0 or node.is_terminal():
            # TODO: Remove later
            # if node.is_terminal():
            #     print("Terminal node: move({}) value({})".format(best_move, node.get_value()))
            return best_move, next_node, node.get_value()

        # get a dictionary of the possible moves and resultant states
        # from the given state
        children = node.get_children()

        # if the current state is a max node
        if node.is_max_node:
            value = -INF

            # for each possible move
            for move, child in children.items():
                # check the expected value of the move
                _, _, check_value = self.evaluate(
                    child, depth_to_search-1, alpha, beta)

                # if expected value is better than current best
                # set that move (and value) as new best
                if check_value > value:
                    value = check_value
                    best_move, next_node = move, child

                # update alpha if appropriate
                alpha = max(alpha, value)

                # prune current node if possible
                if alpha >= beta:
                    break

        # else if the current state is a min node
        else:
            value = INF

            # for each possible move
            for move, child in children.items():
                # check the expected value of the move
                _, _, check_value = self.evaluate(
                    child, depth_to_search-1, alpha, beta)

                # if expected value is better than current best
                # set that move (and value) as new best
                if check_value < value:
                    value = check_value
                    best_move, next_node = move, child

                # update beta if appropriate
                beta = min(beta, value)

                # prune current node if possible
                if alpha >= beta:
                    break
        #             TODO: remove print
        # print("Still some other nodes: move({}) value({})".format(best_move, value))
        return best_move, next_node.game_state, value
