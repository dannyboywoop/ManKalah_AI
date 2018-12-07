#include "message.h"
#include <iostream>
    
message::message(std::string text) : rawMessage(text) {}

// start message methods
startMessage::startMessage(std::string text) : message(text) {}
void startMessage::printFormatted() const {
    std::cout<<rawMessage<<std::endl;
}
void startMessage::performMessageAction(gameTree&) const {

}

// change message methods
changeMessage::changeMessage(std::string text) : message(text) {}
void changeMessage::printFormatted() const {
    std::cout<<rawMessage<<std::endl;
}
void changeMessage::performMessageAction(gameTree&) const {

}

// end message methods
endMessage::endMessage(std::string text) : message(text) {}
void endMessage::printFormatted() const {
    std::cout<<rawMessage<<std::endl;
}
void endMessage::performMessageAction(gameTree&) const {

}