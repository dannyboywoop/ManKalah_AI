#include "TCPGameEngine.h"
#include "heuristic.h"

// entrance point to the program
int main(int argc, char *argv[]) {
	uint16_t port = 12346; // default port
	int maxTreeSearchDepth = 9;
	weightList weights = {1,1,0,0,0,0,0,0,0,0};

	// check if exactly one command line argument was entered
	if (argc == 2) {
		// attempt to parse the command line argument as a port number
		int portNum = std::stoi(argv[1]);
		port = static_cast<uint16_t>(portNum);
	}

	// check if exactly 10 command line arguments were entered
	if (argc == 11) {
		// attempt to parse the command line arguments as weights
		for(int i=0;i<10;i++){
			weights[i] = std::stof(argv[i+1]);
		}
	}

	// check if exactly 11 command line arguments were enterered
	if (argc == 12) {
		// attempt to parse the command line argument as a port number
		int portNum = std::stoi(argv[1]);
		port = static_cast<uint16_t>(portNum);
		// attempt to parse the command line arguments as weights
		for(int i=0;i<10;i++){
			weights[i] = std::stof(argv[i+2]);
		}
	}

	// create a game engine that searches to the maximum depth specified
	// listening to the port number specified
	TCPGameEngine engine(maxTreeSearchDepth, port, weights);
	engine.run();	

	return 0;
}