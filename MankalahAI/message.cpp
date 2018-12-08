#include "message.h"
#include <iostream>
    
message::message(std::string text) : rawMessage(text) {}

// start message methods
startMessage::startMessage(std::string text) : message(text) {}
void startMessage::printFormatted() const {
    // rawMessage == "START;[team]"
    std::cout<<"Match started: We are "<<rawMessage.substr(6)<<std::endl;
}
void startMessage::performMessageAction(gameTree& tree) const {
    // team name starts at position 6
    std::string playerName = rawMessage.substr(6);
    int playerNum;

    // get player number
    if (playerName == "North") playerNum = 0;
    else if (playerName == "South") playerNum = 1;
    else throw std::string("Invalid player name!");

    // initialize game tree
    tree.generateInitialTree(playerNum);
}

// change message methods
changeMessage::changeMessage(std::string text) : message(text) {}
void changeMessage::printFormatted() const {
    std::cout<<rawMessage<<std::endl;
}
void changeMessage::performMessageAction(gameTree& tree) const {
    // rawMessage == 
    // CHANGE;[SWAP or index];n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n;[YOU or OPP]

    // find end of [SWAP or index]
    size_t moveEnd = rawMessage.find(';', 7); // next semi colon after "CHANGE;"

    // get move as string
    std::string moveStr = 
        rawMessage.substr(7, moveEnd - 7);
    
    // convert move string to integer
    int move;
    if (moveStr == "SWAP") move = -1;
    else move = std::stoi(moveStr);

    // update tree based on move made
    tree.makeMove(move);
}

// end message methods
endMessage::endMessage(std::string text) : message(text) {}
void endMessage::printFormatted() const {
    std::cout << "Game Over!" << std::endl;
}
void endMessage::performMessageAction(gameTree& tree) const {
    // do nothing, the game's over!
}