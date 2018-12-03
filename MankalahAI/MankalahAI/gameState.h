#ifndef GAME_STATE_H
#define GAME_STATE_H

#include<array>
#include<set>

const int holes = 7;
const int seeds = 7;
const int boardSize = 2 * holes + 2;
const int totalSeeds = 2 * holes * seeds;
const std::array<int, boardSize> defaultBoard =
	{ 7,7,7,7,7,7,7,0,7,7,7,7,7,7,7,0 };

class gameState {
private:
	const int scoreHoles[2] = { holes, boardSize - 1 };
	std::array<int, boardSize> board;
	int currentPlayer;
	bool gameOver;
	bool firstTurn;

	int otherPlayer() const;
	int otherPlayer(int player) const;
	int holeIndex(int hole) const;
	int holeIndex(int hole, int player) const;
	void giveRemainingSeedsToPlayer(int player);

public:
	int getValue(int player) const;
	std::set<int> movesAvailable() const;
	std::set<int> movesAvailable(int player) const;
	std::array<int, 2> scores() const;
	gameState moveResult(int pos) const;

	// default constructor
	gameState();
};

#endif