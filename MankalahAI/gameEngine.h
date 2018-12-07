#ifndef GAME_ENGINE_H
#define GAME_ENGINE_H

#include "message.h"
#include "gameTree.h"
#include <netdb.h>
#include <vector>

class gameEngine{
private:
	int listening;
	sockaddr_in client;
	socklen_t clientSize = sizeof(client);
	int clientSocket;
    gameTree tree;

	void createSocket();

	void bindSocket(int port=12346);

	void markSocketForListening(int maxClients = 1);

	void acceptCall();

	int receiveData(char (&buff)[1024]);
	
	void sendBestMove();

    std::vector<message> parseDataToMessages(const char (&buf)[1024], int size);

public:
	gameEngine();
    gameEngine(int);
    ~gameEngine();
    
	void run();
};

#endif