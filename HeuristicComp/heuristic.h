#ifndef HEURISTIC_H
#define HEURISTIC_H

#include "gameState.h"
#include <array>

typedef std::array<float,10> weightList;

class heuristic{
private:
    float numPoints(const gameState&, int);
    float numGoAgainTurns(const std::array<short int, holes>&);
    float numStonesOnSide(const std::array<short int, holes>&);
    float emptyHoles(const std::array<short int, holes>&);
    float vulnerableHoles(const std::array<short int, holes>&, const std::array<short int, holes>&);

    weightList weights;
public:
    float operator()(const gameState&, int);
    heuristic(weightList);
    heuristic(float list[10]);
};

#endif