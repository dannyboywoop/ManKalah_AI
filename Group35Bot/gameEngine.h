// header guard
#ifndef GAME_ENGINE_H
#define GAME_ENGINE_H

// includes
#include "message.h"
#include "gameTree.h"
#include <vector>
#include <memory>

// communicates with ManKalah.jar through std in/out. Makes and sends decisions
class gameEngine {
private:
	gameTree tree; // stores game tree with the current game state as root

	// determines the best move to play and sends the relevant message
	void sendBestMove();

	// parses a message string into a message object
	std::unique_ptr<message> parseMessage(std::string);

public:
	// constructor, sets the maximum tree search depth and the weights to
	// us for the heuristic
	gameEngine(int maxTreeDepth, weightList weights);

	// runs our AI
	void run();
};

// end header guard
#endif
