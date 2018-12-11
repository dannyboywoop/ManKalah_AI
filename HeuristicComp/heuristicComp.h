#ifndef HEURISTIC_COMP_H
#define HEURISTIC_COMP_H

#include "gameState.h"
#include "alphaBetaAI.h"
#include "heuristic.h"
#include <map>
#include <memory>

class sharedNode {
	friend class heuristicComp;
public:
	sharedNode(gameState, heuristicComp&);
	~sharedNode();
	float getValue() const;
	bool isTerminal() const;
	const std::map<int, std::unique_ptr<sharedNode>>& getChildren();
	bool isMaxNode() const;
private:
	gameState state;
	std::map<int, std::unique_ptr<sharedNode>> children;
	heuristicComp& tree;
	bool childrenCalculated;
	int rootPlayer() const;
};

class heuristicComp {
	friend class sharedNode;
public:
	heuristicComp(int maxDepth, float north[10], float south[10]);
	int runGame();
	std::unique_ptr<sharedNode> root;
private:
	void generateInitialTree();
	void makeMove(int index);
	int getBestMove();
	int nodesInMemory;
	alphaBetaAI ai;
	heuristic heuristics[2];
};



#endif