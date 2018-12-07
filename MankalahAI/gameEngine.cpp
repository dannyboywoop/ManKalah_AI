#include "gameEngine.h"
#include "message.h"
#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>
#include <string>
#include <vector>

void gameEngine::createSocket(){
	listening = socket(AF_INET, SOCK_STREAM, 0);
	if (listening == -1) {
		throw std::string("Error: Failed to create socket!");
	}
}

void gameEngine::bindSocket(int port /*=12346*/){
	sockaddr_in hint;
	hint.sin_family = AF_INET;
	hint.sin_port = htons(port);
	inet_pton(AF_INET, "0.0.0.0", &hint.sin_addr);

	if (bind(listening, (sockaddr*)&hint, sizeof(hint)) == -1) {
		throw std::string("Error: Failed to bind to IP/port!");
	}
}

void gameEngine::markSocketForListening(int maxClients /*= 1*/){
	if (listen(listening, maxClients) == -1) {
		throw std::string("Error: Listen failed!");
	}
}

void gameEngine::acceptCall(){

	clientSocket = accept(listening,
		(sockaddr*)&client, &clientSize);

	if (clientSocket == -1) {
		throw std::string("Error: Failed to connect to client!");
	}

	std::cout << "Connected!" << std::endl;

	// close listening socket
	close(listening);
}

int gameEngine::receiveData(char (&buff)[1024]){
	// clear the buffer
	memset(buff, 0, 1024);

	// wait for a message
	int bytesRecv = int(recv(clientSocket, buff, 1024, 0));
	if (bytesRecv == -1) {
		throw std::string("Error: Connection issue!");
	}
	return bytesRecv;
	// display message
	//std::cout << "Received: " << std::string(buff, 0, bytesRecv) << std::endl;
}

std::vector<message> parseDataToMessages(){

}

void gameEngine::run(){
	char buf[1024];
	std::vector<message> messages;
	while (true) {
		// recieve data
		int messageLength = receiveData(buf);
		if (messageLength == 0) {
			std::cout << "The client disconnected!" << std::endl;
			break;
		}

		// parse into seperate messages
		messages = parseDataToMessages(buf, messageLength);

		// act on all messages recieved
		for (const message& m: messages){
			std::cout<<m.rawMessage<<std::endl;
			m.printFormatted();
			m.performMessageAction(tree);
		}

		// make move if appropriate
		if (tree.isOurTurn()){
			sendBestMove();
		}
	}
}

void gameEngine::sendBestMove(){
	// resend message
	//send(clientSocket, buff, bytesRecv + 1, 0);
}

gameEngine::gameEngine(): gameEngine(7){}

gameEngine::gameEngine(int maxTreeDepth): tree(maxTreeDepth) {
	// create a socket
	createSocket();

	// bind the socket to an IP / port
	bindSocket();

	// Mark the socket for listening in
	markSocketForListening();

	// Accept a call
	acceptCall();
}

gameEngine::~gameEngine(){
	// close socket
	close(clientSocket);
}

