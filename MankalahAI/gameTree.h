#ifndef GAME_TREE_H
#define GAME_TREE_H

#include "gameState.h"
#include "alphaBetaAI.h"
#include <map>
#include <memory>

class gameTree {
	friend class node;
public:
	gameTree(int maxDepth);
	std::unique_ptr<node> root;
	void generateInitialTree(int ourPlayer);
	void makeMove(int index);
	bool isOurTurn() const;
	int getBestMove();
private:
	int nodesInMemory;
	alphaBetaAI ai;
};

class node {
	friend class gameTree;
public:
	node(gameState, int, gameTree&);
	~node();
	float getValue() const;
	bool isTerminal() const;
	const std::map<int, std::unique_ptr<node>>& getChildren();
	bool isMaxNode() const;
private:
	gameState state;
	int ourPlayer;
	std::map<int, std::unique_ptr<node>> children;
	gameTree& tree;
	bool childrenCalculated;
};

#endif
