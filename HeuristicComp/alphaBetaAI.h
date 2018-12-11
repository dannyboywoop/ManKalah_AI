// header guard
#ifndef ALPHA_BETA_AI_H
#define ALPHA_BETA_AI_H

#include <limits>

const float inf = std::numeric_limits<float>::max();

class heuristicComp;
class sharedNode;

struct move {
	int index;
	float value;
	move();
	move(int,float);
};

class alphaBetaAI {
public:
	alphaBetaAI(int);
	int chooseMove(heuristicComp&);
private:
	int maxDepth;
	int sharedNodesChecked;
	move evalualate(sharedNode&, int, float, float);
};


#endif
