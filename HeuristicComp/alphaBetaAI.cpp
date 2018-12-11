#include "alphaBetaAI.h"
#include "heuristicComp.h"
#include <iostream>
#include <utility>
#include <algorithm>

// move constructors
move::move() :index(0), value(0) {}
move::move(int index, float value) :index(index), value(value) {}

// alphaBetaAi constructors
alphaBetaAI::alphaBetaAI(int maxDepth) :maxDepth(maxDepth), sharedNodesChecked(0) {}

// calulates and returns the best available move
int alphaBetaAI::chooseMove(heuristicComp& tree) {
	// reset sharedNodesChecked counter
	sharedNodesChecked = 0;

	// find best move
	move bestMove = evalualate(*tree.root, maxDepth, -inf, inf);

	// return best move
	return bestMove.index;
}

move alphaBetaAI::evalualate(
	sharedNode& currentsharedNode, int depthToSearch, float alpha, float beta) {
	// increment number of sharedNodes checked
	sharedNodesChecked++;

	move bestMove;

	// if bottom of searchable tree, return sharedNode value
	if (depthToSearch == 0 || currentsharedNode.isTerminal()) {
		bestMove.value = currentsharedNode.getValue();
		return bestMove;
	}

	// get children of current sharedNode
	const std::map<int, std::unique_ptr<sharedNode>>& children = currentsharedNode.getChildren();

	// if the current sharedNode is a max sharedNode
	if (currentsharedNode.isMaxNode()) {
		float value = -inf;

		// for each possible move
		for (const std::pair<const int, std::unique_ptr<sharedNode>>& child : children) {
			// check the expected value fo the move
			float checkValue = evalualate(
				*child.second, depthToSearch - 1, alpha, beta).value;

			// if expected value is better than current best
			// set that move (and value) as new best
			if (checkValue > value) {
				value = checkValue;
				bestMove.index = child.first;
				bestMove.value = value;
			}

			// update alpha if appropriate
			alpha = std::max(alpha, value);

			// prune current sharedNode if possible
			if (alpha >= beta) break;
		}
	}
	// if the curren sharedNode is a min sharedNode
	else {
		float value = inf;

		// for each possible move
		for (const std::pair<const int, std::unique_ptr<sharedNode>>& child : children) {
			// check the expected value fo the move
			float checkValue = evalualate(
				*child.second, depthToSearch - 1, alpha, beta).value;

			// if expected value is better than current best
			// set that move (and value) as new best
			if (checkValue < value) {
				value = checkValue;
				bestMove.index = child.first;
				bestMove.value = value;
			}

			// update beta if appropriate
			beta = std::min(beta, value);

			// prune current sharedNode if possible
			if (alpha >= beta) break;
		}
	}
	
	return bestMove;
}