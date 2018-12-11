#include "heuristicComp.h"
#include <iostream>
#include <utility>

// sharedNode constructor
sharedNode::sharedNode(gameState state, heuristicComp& tree): state(state), children(), tree(tree), childrenCalculated(false) {
	tree.nodesInMemory++;
}

// sharedNode destructor
sharedNode::~sharedNode() {
	tree.nodesInMemory--;
}

// returns the value of the sharedNode (heuristic or true value)
float sharedNode::getValue() const {
	if (isTerminal()) return state.getValue(rootPlayer());
	else return tree.heuristics[rootPlayer()](state, rootPlayer());
}

// returns whether or not the sharedNode should have any children
bool sharedNode::isTerminal() const {
	return state.isGameOver();
}

// returns reference to sharedNode's children (calculating them first if necassary)
const std::map<int, std::unique_ptr<sharedNode>>& sharedNode::getChildren() {
	// check if the children have already been calculated
	if (!childrenCalculated) {
		// if not calculate them based on available moves
		std::set<int> availableMoves = state.movesAvailable();
		for (int move : availableMoves) {
			children[move] = std::unique_ptr<sharedNode>(new sharedNode(
				state.moveResult(move), tree));
		}
		childrenCalculated = true;
	}
	// return reference to children
	return children;
}

// returns whether the sharedNode should be treated as a max sharedNode by the minimax
// tree search
bool sharedNode::isMaxNode() const {
	return state.getCurrentPlayer() == rootPlayer();
}

int sharedNode::rootPlayer() const {
	return tree.root->state.getCurrentPlayer();
}

// heuristicComp constructor
heuristicComp::heuristicComp(int maxDepth, float north[10], float south[10]) 
	:nodesInMemory(0), ai(maxDepth), heuristics({north, south}) {
		generateInitialTree();
	}

// generates the first two levels of the game tree, accounting for extra
// "SWAP" options on second level
void heuristicComp::generateInitialTree() {
	// don't generate tree if a root already exists
	if (root) return;

	// create root sharedNode
	gameState initialState;
	root = std::unique_ptr<sharedNode>(new sharedNode(initialState, *this));

	// for all initial moves
	for (const std::pair<const int, std::unique_ptr<sharedNode>>& child :
		root->getChildren()) {

		// calculate subsequent children
		child.second->getChildren();

		// add swap move
		gameState clonedState = child.second->state;
		int newPlayer = clonedState.otherPlayer();
		for(int i=0;i<=holes;i++){
			clonedState.board[i] = child.second->state.board[i+holes+1];
			clonedState.board[i+holes+1] = child.second->state.board[i];
		}
		clonedState.currentPlayer = newPlayer;
		child.second->children[-1] =
			std::unique_ptr<sharedNode>(new sharedNode(clonedState, *this));
	}
}

// move the root of the tree to one of its children
// destroying all unecassary sharedNodes
void heuristicComp::makeMove(int index) {
	// get children
	root->getChildren();

	// change root to relevant child
	root = std::move(root->children[index]);
}

// calculate and return the index of the best move available to us
int heuristicComp::getBestMove() {
	int bestMove = ai.chooseMove(*this);
	return bestMove;
}

int heuristicComp::runGame(){
	while (!root->isTerminal()){
		makeMove(getBestMove());
	}

	auto result = root->state.scores();

	return (result[1] > result[0]);
}