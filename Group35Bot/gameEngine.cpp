// includes
#include "gameEngine.h"
#include <string>

// convert a string into a message object
std::unique_ptr<message> gameEngine::parseMessage(std::string mess) {
	// if message is a start message
	if (mess[0] == 'S')
		return std::unique_ptr<message>(
			new startMessage(mess));

	// if message is a change message
	if (mess[0] == 'C')
		return std::unique_ptr<message>(
			new changeMessage(mess));

	// if message is an end message
	if (mess[0] == 'E')
		return std::unique_ptr<message>(
			new endMessage(mess));

	// else message not recognised
	throw std::string("Error: message not recognised");
}

// calculates and sends the best available move
void gameEngine::sendBestMove() {

	// get the best move from gameTree
	int bestMove = tree.getBestMove();

	// convert the move index to a move message
	std::string moveMessage;
	if (bestMove == -1) {
		moveMessage = "SWAP";
		// update tree root
		tree.makeMove(-1);
	}
	else {
		moveMessage = "MOVE;" + std::to_string(bestMove);
	}

	// send move message 
	std::cout << moveMessage << std::endl;
}

// play the game
void gameEngine::run() {
	std::string messageString;
	std::unique_ptr<message> messageRead;
	bool continueGame{ true };
	while (continueGame) {
		// Get a message from the game
		std::getline(std::cin, messageString);

		// parse message string into message object
		messageRead = parseMessage(messageString);

		// perform message action
		continueGame = messageRead->performMessageAction(tree);

		// make move if appropriate
		if (tree.isOurTurn()) {
			sendBestMove();
		}

	}
}

// gameEngine constructor
gameEngine::gameEngine(int maxTreeDepth, weightList weights) : tree(maxTreeDepth, weights) {}
