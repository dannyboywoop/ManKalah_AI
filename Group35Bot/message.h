// header guard
#ifndef MESSAGE_H
#define MESSAGE_H

#include "gameTree.h"
#include <string>

class message{
protected:
    std::string rawMessage;
public:
    message(std::string);
    virtual void printFormatted() const = 0;
    virtual bool performMessageAction(gameTree&) const = 0;
};

class startMessage: public message{
public:
    startMessage(std::string);
    void printFormatted() const;
    bool performMessageAction(gameTree&) const;
};

class changeMessage: public message{
public:
    changeMessage(std::string);
    void printFormatted() const;
    bool performMessageAction(gameTree&) const;
};

class endMessage: public message{
public:
    endMessage(std::string);
    void printFormatted() const;
    bool performMessageAction(gameTree&) const;
};


#endif