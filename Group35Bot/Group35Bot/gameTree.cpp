#include "gameTree.h"
#include <iostream>
#include <utility>

// node constructor
node::node(gameState state, int player, gameTree& tree): state(state), 
	ourPlayer(player), children(), tree(tree), childrenCalculated(false) {
	tree.nodesInMemory++;
}

// node destructor
node::~node() {
	tree.nodesInMemory--;
}

// returns the value of the node (heuristic or true value)
float node::getValue() const {
	if (isTerminal()) return state.getValue(ourPlayer);
	else return tree.heuristicFunction(state, ourPlayer);
}

// returns whether or not the node should have any children
bool node::isTerminal() const {
	return state.isGameOver();
}

// returns reference to node's children (calculating them first if necassary)
const std::map<int, std::unique_ptr<node>>& node::getChildren() {
	// check if the children have already been calculated
	if (!childrenCalculated) {
		// if not calculate them based on available moves
		std::set<int> availableMoves = state.movesAvailable();
		for (int move : availableMoves) {
			children[move] = std::unique_ptr<node>(new node(
				state.moveResult(move), ourPlayer, tree));
		}
		childrenCalculated = true;
	}
	// return reference to children
	return children;
}

// returns whether the node should be treated as a max node by the minimax
// tree search
bool node::isMaxNode() const {
	return state.getCurrentPlayer() == ourPlayer;
}

// gameTree constructor
gameTree::gameTree(int maxDepth, weightList weights) 
	:nodesInMemory(0), ai(maxDepth), heuristicFunction(weights) {}

// generates the first two levels of the game tree, accounting for extra
// "SWAP" options on second level
void gameTree::generateInitialTree(int ourPlayer) {
	// don't generate tree if a root already exists
	if (root) return;

	// create root node
	gameState initialState;
	root = std::unique_ptr<node>(new node(initialState, ourPlayer, *this));
	//std::cout << initialState << std::endl;

	// for all initial moves
	for (const std::pair<const int, std::unique_ptr<node>>& child :
		root->getChildren()) {

		// calculate subsequent children
		child.second->getChildren();

		// add swap move
		gameState clonedState = child.second->state;
		int ourNewPlayer = (child.second->ourPlayer + 1) % 2;
		child.second->children[-1] = std::unique_ptr<node>(new node(
			clonedState, ourNewPlayer, *this));
	}
}

// move the root of the tree to one of its children
// destroying all unecassary nodes
void gameTree::makeMove(int index) {
	// get children
	root->getChildren();

	// change root to relevant child
	root = std::move(root->children[index]);

	// print new game state
	//std::cout << root->state << std::endl;
}

// returns whether the root node contains a state where it is our turn
bool gameTree::isOurTurn() const {
	return (root->isMaxNode() && !root->isTerminal());
}

// calculate and return the index of the best move available to us
int gameTree::getBestMove() {
	int bestMove = ai.chooseMove(*this);
	//std::cout << nodesInMemory << " node(s) in memory" << std::endl;
	return bestMove;
}
