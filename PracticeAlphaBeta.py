import math

inf = float('inf')


class AlphaBetaAI:
    def __init__(self, maxDepth):
        # maxDepth is the maximum depth of the tree to search
        # before using a heuristic
        self.max_depth = maxDepth

    def choose_move(self, game_tree):
        self.nodes_checked = 0

        evaluation = self.evaluate(game_tree.root, self.max_depth)

        print("{} nodes checked".format(self.nodes_checked))

        return evaluation

    def evaluate(self, node, depth_to_search, alpha=-inf, beta=inf):
        self.nodes_checked += 1

        bestMove, next_node = None, None

        if (depth_to_search == 0 or node.is_terminal()):
            return bestMove, next_node, node.getValue()

        # get a dictionary of the possible moves and resultant states
        # from the given state
        children = node.children

        # if the current state is a max node
        if node.is_max_node:
            value = -float('inf')

            # for each possible move
            for move, child in children.items():
                # check the expected value of the move
                _, _, checkValue = self.evaluate(
                    child, depth_to_search-1, alpha, beta)

                # if expected value is better than current best
                # set that move (and value) as new best
                if checkValue > value:
                    value = checkValue
                    bestMove, next_node = move, child

                # update alpha if appropriate
                alpha = max(alpha, value)

                # prune current node if possible
                if (alpha >= beta):
                    break

        # else if the current state is a min node
        else:
            value = float('inf')

            # for each possible move
            for move, child in children.items():
                # check the expected value of the move
                _, _, checkValue = self.evaluate(
                    child, depth_to_search-1, alpha, beta)

                # if expected value is better than current best
                # set that move (and value) as new best
                if checkValue < value:
                    value = checkValue
                    bestMove, next_node = move, child

                # update beta if appropriate
                beta = min(beta, value)

                # prune current node if possible
                if (alpha >= beta):
                    break
        return bestMove, next_node.game_state, value


# below is a basic example of how the alpha-beta pruner AI works
if __name__ == '__main__':

    from GameTree import GameTree, Node
    from gameState import GameState

    init_state = GameState()
    root = Node(init_state, True)
    game_tree = GameTree(root)
    game_tree.calculate_children(5)

    print("Game tree built.")

    ai = AlphaBetaAI(4)

    move, next_state, expected_value = ai.choose_move(game_tree)

    # print the results
    print("{} is the best move!".format(move))
    print("{} is the expected payoff".format(expected_value))
    print("The resultant state would be:")
    print(next_state)
