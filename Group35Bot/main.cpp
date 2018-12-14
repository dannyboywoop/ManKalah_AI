#include "gameEngine.h"
#include "heuristic.h"
#include <string>

// entrance point to the program
int main(int argc, char *argv[]) {
	int maxTreeSearchDepth = 10;
	weightList weights = { 
		0.94411071f,
		1.0f,
		0.93632376f,
		0.70470548f,
		0.11684469f,
		0.01519149f,
		0.04276269f,
		0.16460274f,
		0.39338962f,
		0.08789862f 
	};

	// check if exactly one command line argument was entered
	if (argc == 2) {
		// attempt to parse the command line argument as an int
		maxTreeSearchDepth = std::stoi(argv[1]);
	}

	// check if exactly 10 command line arguments were entered
	if (argc == 11) {
		// attempt to parse the command line arguments as weights
		for (int i = 0; i < 10; i++) {
			weights[i] = std::stof(argv[i + 1]);
		}
	}

	// check if exactly 11 command line arguments were enterered
	if (argc == 12) {
		// attempt to parse the command line argument as an int
		maxTreeSearchDepth = std::stoi(argv[1]);
		// attempt to parse the command line arguments as weights
		for (int i = 0; i < 10; i++) {
			weights[i] = std::stof(argv[i + 2]);
		}
	}
	// create a game engine that searches to the maximum depth specified
	gameEngine engine(maxTreeSearchDepth, weights);
	engine.run();

	return 0;
}