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

}

// end message methods
endMessage::endMessage(std::string text) : message(text) {}
void endMessage::printFormatted() const {
    std::cout<<rawMessage<<std::endl;
}
void endMessage::performMessageAction(gameTree& tree) const {

}