#ifndef MESSAGE_H
#define MESSAGE_H

#include "gameTree.h"
#include <string>

class message{
public:
    std::string rawMessage;
    void printFormatted() const;
    void performMessageAction(gameTree& tree) const;
};



#endif