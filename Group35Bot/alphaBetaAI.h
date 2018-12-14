// header guard
#ifndef ALPHA_BETA_AI_H
#define ALPHA_BETA_AI_H

// includes
#include <limits>

// inf represents maximum value a float can take
const float inf = std::numeric_limits<float>::max();

class gameTree;
class node;

// basic struct for storing a move
struct move {
	int index; // index associated with move
	float value; // value of node the move takes you to
	move();
	move(int,float);
};

// class for performing MiniMax search with alpha-beta pruning
class alphaBetaAI {
public:
	// constructor, takes argument representing maximum depth of search
	alphaBetaAI(int);
	// select and return the best move available given a gameTree
	int chooseMove(gameTree&);
private:
	int maxDepth; // maximum depth to search before using heuristic value
	int nodesChecked; // counts number of nodes checked in a given search
	// evaluates a given node
	move evalualate(node&, int, float, float);
};

// end header guard
#endif
