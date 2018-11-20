class Node:
    def __init__(self, game_state, is_max_node, tree=None):
        self.game_state = game_state
        self.is_max_node = is_max_node
        self.children = {}
        self.tree = tree

    # TODO: we cannot show tree with all the game state
    def __str__(self, level=0, move=""):
        output = "  " * level + move + str(self.game_state) + "\n"
        for key, child in self.children.items():
            output += child.__str__(level+1, str(key)+": ")
        return output

    def is_terminal(self):
        return len(self.children) == 0

    def calculate_children(self, depth=1):
        # TODO: replace with actual calculation from game state
        if not self.children:
            self.children = {
                1: Node(10, True, self.tree),
                2: Node(11, True, self.tree)
            }

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


class GameTree:
    def __init__(self, root):
        root.tree = self
        self.root = root

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

    def __str__(self):
        return self.root.__str__()


if __name__ == "__main__":
    tree = GameTree(Node(1, True))

    print(tree)

    tree.calculate_children()
    print(tree)

    tree.calculate_children(2)
    print(tree)

    tree.calculate_children(3)
    print(tree)

    tree.root.children[1].make_root()
    print(tree)
