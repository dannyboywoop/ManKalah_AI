#ifndef GAME_ENGINE_H
#define GAME_ENGINE_H

#include "message.h"
#include "gameTree.h"
#include <vector>
#include <memory>


class gameEngine {
private:
	gameTree tree;

	void sendBestMove();

	std::unique_ptr<message> parseMessage(std::string);

public:
	gameEngine(int maxTreeDepth, weightList weights);

	void run();
};


#endif
