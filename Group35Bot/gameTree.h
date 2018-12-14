// header guard
#ifndef GAME_TREE_H
#define GAME_TREE_H

// includes
#include "gameState.h"
#include "alphaBetaAI.h"
#include "heuristic.h"
#include <map>
#include <memory>

// class for storing a game tree and making decisions
class gameTree {
	friend class node;
public:
	std::unique_ptr<node> root; // pointer to the root node

	// constructor, takes the maximum search depth and the weights
	// to use for the heuristic function
	gameTree(int maxDepth, weightList weights);

	// generates the first two levels of the gameTree (implements Pie Rule)	
	void generateInitialTree(int ourPlayer);

	// move the root of the tree, discarding unnecessary nodes
	void makeMove(int index);

	// returns true if it is our turn at the root node
	bool isOurTurn() const;

	// returns the best move available to us
	int getBestMove();
private:
	int nodesInMemory; // the number of nodes currently store in memory
	alphaBetaAI ai; // the AI used to choose the best possible move
	heuristic heuristicFunction; // the heuristic function used
};

// stores a single gameState with pointers to child states
class node {
	friend class gameTree;
public:
	// constructor
	node(gameState, int, gameTree&);
	// destructor
	~node();

	// return the value of the state stored in the node
	float getValue() const;

	// return whether the node stores a gameOver state
	bool isTerminal() const;

	// calculate (or return if previously calculated) the nodes children
	const std::map<int, std::unique_ptr<node>>& getChildren();

	// returns true if the node is a max node (our player's turn)
	bool isMaxNode() const;
private:
	gameState state; // stores the state of the game
	int ourPlayer; // the number of our player
	std::map<int, std::unique_ptr<node>> children; // child nodes
	gameTree& tree; // tree containing the node
	bool childrenCalculated; // true if the children have been calculated
};

// end header guard
#endif
