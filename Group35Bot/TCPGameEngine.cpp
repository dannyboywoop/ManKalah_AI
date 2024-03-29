#include "TCPGameEngine.h"
#include "message.h"
#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <cstring>
#include <string>
#include <algorithm>

// create the listening socket
void TCPGameEngine::createSocket(){
	listening = socket(AF_INET, SOCK_STREAM, 0);
	if (listening == -1) {
		throw std::string("Error: Failed to create socket!");
	}
}

// bind the socket to a port/IP
void TCPGameEngine::bindSocket(uint16_t port){
	sockaddr_in hint;
	hint.sin_family = AF_INET;
	hint.sin_port = htons(port);
	inet_pton(AF_INET, "0.0.0.0", &hint.sin_addr);

	if (bind(listening, (sockaddr*)&hint, sizeof(hint)) == -1) {
		throw std::string("Error: Failed to bind to IP/port!");
	}
}

// mark socket for listening (you could have read the method name on this one)
void TCPGameEngine::markSocketForListening(int maxClients /*= 1*/){
	if (listen(listening, maxClients) == -1) {
		throw std::string("Error: Listen failed!");
	}
}

// accept connection from client (ManKalah.jar)
void TCPGameEngine::acceptCall(){

	clientSocket = accept(listening,
		(sockaddr*)&client, &clientSize);

	if (clientSocket == -1) {
		throw std::string("Error: Failed to connect to client!");
	}

	std::cout << "Connected!" << std::endl;

	// close listening socket
	close(listening);
}

// read socket info into buffer
int TCPGameEngine::receiveData(char (&buff)[1024]){
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

// convert a string into a message object
std::unique_ptr<message> TCPGameEngine::parseMessage(std::string mess){
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

// get all messages from buffer (parsed into message objects)
std::vector<std::unique_ptr<message>> TCPGameEngine::parseDataToMessages(
	const char (&buff)[1024], int size){
	
	// stores messages
	std::vector<std::unique_ptr<message>> messages;

	int previousEndLine = -1;
	for(int i=0; i<size; i++){
		// messages devided by new line characters
		if(buff[i]=='\n') {
			// add message to messages
			messages.push_back(
				// parse the message string to a message object
				parseMessage(
					std::string(buff,
					previousEndLine + 1,
					i - previousEndLine - 1)
				)
			);
			previousEndLine = i;
		}
	}

	return std::move(messages);	
}

// play the game
void TCPGameEngine::run(){
	char buf[1024];
	std::vector<std::unique_ptr<message>> messages;
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
		for (const auto& m: messages){
			m->printFormatted();
			m->performMessageAction(tree);
		}
		messages.clear();

		// make move if appropriate
		if (tree.isOurTurn()){
			sendBestMove();
		}
		
	}
}

// calculates and sends the best available move
void TCPGameEngine::sendBestMove(){
	
	// get the best move from gameTree
	int bestMove = tree.getBestMove();

	// convert the move index to a move message
	std::string moveMessage;
	if (bestMove == -1){
		moveMessage = "SWAP\n";
		tree.makeMove(-1);
		std::cout << "Performed Swap!" << std::endl;
	}else{
		moveMessage = "MOVE;" + std::to_string(bestMove) + '\n';
		std::cout << "Made move: " << bestMove << std::endl;
	}

	// send move message 
	send(clientSocket, moveMessage.c_str(), moveMessage.size(), 0);
}

// TCPGameEngine constructor
TCPGameEngine::TCPGameEngine(int maxTreeDepth, uint16_t port, weightList weights): tree(maxTreeDepth, weights) {
	// create a socket
	createSocket();

	// bind the socket to an IP / port
	bindSocket(port);

	// Mark the socket for listening in
	markSocketForListening();

	// Accept a call
	acceptCall();
}

TCPGameEngine::~TCPGameEngine(){
	// close socket
	close(clientSocket);
}

