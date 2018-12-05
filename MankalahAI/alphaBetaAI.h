#ifndef ALPHA_BETA_AI_H
#define ALPHA_BETA_AI_H

#include <limits>

const float inf = std::numeric_limits<float>::max();

class gameTree;
class node;

struct move {
	int index;
	float value;
};

class alphaBetaAI {
public:
	alphaBetaAI(int);
	int chooseMove(gameTree&);
private:
	int maxDepth;
	int nodesChecked;
	move evalualate(node&, int, float, float);
};


#endif
