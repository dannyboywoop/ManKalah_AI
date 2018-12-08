#include "gameEngine.h"

// entrance point to the program
int main(int argc, char *argv[]) {
	uint16_t port = 12346; // default port
	int maxTreeSearchDepth = 7;

	// check if exactly one command line argument was entered;
	if (argc == 2) {
		// attempt to parse the command line argument as a port number
		int portNum = std::stoi(argv[1]);
		port = static_cast<uint16_t>(portNum);
	}

	// create a game engine that searches to the maximum depth specified
	// listening to the port number specified
	gameEngine engine(maxTreeSearchDepth, port);
	engine.run();	

	return 0;
}