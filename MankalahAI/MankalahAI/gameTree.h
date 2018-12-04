#ifndef GAME_TREE_H
#define GAME_TREE_H

#include "gameState.h"
#include <map>

class node {
public:
	node();
	~node();
	float getValue();
	bool isTerminal();
	std::map<int, node>& getChildren();
	void makeRoot();
	bool isMaxNode();
};


class gameTree {
public:
	gameTree();
	node root;
	void generateInitialTree(int ourPlayer);
	void makeMove(int index);
	bool isOurTurn();
	int getBestMove();
};


#endif
