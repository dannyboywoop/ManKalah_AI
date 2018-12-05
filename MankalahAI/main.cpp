#include "gameTree.h"
#include <iostream>
#include <list>
#include <chrono>

int main() {
	// Record start time
	auto start = std::chrono::high_resolution_clock::now();
	
	// go through the game
	gameTree tree(8);
	std::list<int> bestMoves;
	tree.generateInitialTree(1);
	while(!tree.root->isTerminal()) {
		int bestMove = tree.getBestMove();
		bestMoves.push_back(bestMove);
		tree.makeMove(bestMove);
	}

	// Record end time
	auto finish = std::chrono::high_resolution_clock::now();

	// measure time elapsed
	std::chrono::duration<double> elapsed = (finish - start)/bestMoves.size();
	std::cout << "Time for execution: " << elapsed.count() << "s" << std::endl;

	// output moves
	for (int move : bestMoves) {
		std::cout << move << ", ";
	}
	std::cout << std::endl;

	return 0;
}