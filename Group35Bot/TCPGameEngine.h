// header guard
#ifndef TCP_GAME_ENGINE_H
#define TCP_GAME_ENGINE_H

#include "message.h"
#include "gameTree.h"
#include <netdb.h>
#include <vector>
#include <memory>

class TCPGameEngine{
private:
	int listening;
	sockaddr_in client;
	socklen_t clientSize = sizeof(client);
	int clientSocket;
    gameTree tree;

	void createSocket();

	void bindSocket(uint16_t);

	void markSocketForListening(int maxClients = 1);

	void acceptCall();

	int receiveData(char (&buff)[1024]);
	
	void sendBestMove();

    std::vector<std::unique_ptr<message>> parseDataToMessages(
		const char (&buff)[1024], int size);
	
	std::unique_ptr<message> parseMessage(std::string);

public:
	TCPGameEngine(int maxTreeDepth, uint16_t port, weightList weights);
    ~TCPGameEngine();
    
	void run();
};

#endif