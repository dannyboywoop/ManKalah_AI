#include "gameTree.h"
#include <iostream>
#include <utility>

node::node(gameState state, int player, gameTree& tree): state(state), 
	ourPlayer(player), children(), tree(tree), childrenCalculated(false) {
	tree.nodesInMemory++;
}

node::~node() {
	tree.nodesInMemory--;
}

float node::getValue() const {
	return state.getValue(ourPlayer);
}

bool node::isTerminal() const {
	return state.isGameOver();
}

const std::map<int, std::unique_ptr<node>>& node::getChildren() {
	if (!childrenCalculated) {
		std::set<int> availableMoves = state.movesAvailable();
		for (int move : availableMoves) {
			children[move] = std::unique_ptr<node>(new node(
				state.moveResult(move), ourPlayer, tree));
		}
		childrenCalculated = true;
	}
	return children;
}

bool node::isMaxNode() const {
	return state.getCurrentPlayer() == ourPlayer;
}

gameTree::gameTree(int maxDepth) :nodesInMemory(0), ai(maxDepth) {}

void gameTree::generateInitialTree(int ourPlayer) {
	// don't generate tree if a root already exists
	if (root) return;

	// create root node
	gameState initialState;
	root = std::unique_ptr<node>(new node(initialState, ourPlayer, *this));
	std::cout << initialState << std::endl;

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

void gameTree::makeMove(int index) {
	root->getChildren();
	root = std::move(root->children[index]);
	std::cout << root->state << std::endl;
}

bool gameTree::isOurTurn() const {
	return (root->isMaxNode() && !root->isTerminal());
}

int gameTree::getBestMove() {
	int bestMove = ai.chooseMove(*this);
	std::cout << nodesInMemory << " node(s) in memory" << std::endl;
	return bestMove;
}
