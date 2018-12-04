#ifndef GAME_STATE_H
#define GAME_STATE_H

#include <iostream>
#include <array>
#include <set>

const int holes = 7;
const int seeds = 7;
const int boardSize = 2 * holes + 2;
const int totalSeeds = 2 * holes * seeds;
const std::array<int, boardSize> defaultBoard =
	{ 7,7,7,7,7,7,7,0,7,7,7,7,7,7,7,0 };

typedef std::array<int, boardSize> gameBoard;
std::ostream& operator<<(std::ostream& os, const gameBoard& board);

class gameState {
friend std::ostream& operator<<(std::ostream& os, const gameState& state);
private:
	const int scoreHoles[2] = { holes, boardSize - 1 };
	gameBoard board;
	int currentPlayer;
	bool gameOver;
	bool firstTurn;

	int otherPlayer() const;
	int otherPlayer(int player) const;
	int holeIndex(int hole) const;
	int holeIndex(int hole, int player) const;
	void giveRemainingSeedsToPlayer(int player);

public:
	float getValue(int player) const;
	std::set<int> movesAvailable() const;
	std::set<int> movesAvailable(int player) const;
	std::array<int, 2> scores() const;
	gameState moveResult(int pos) const;
	bool isGameOver() const;
	int getCurrentPlayer() const;

	// default constructor
	gameState();
};

#endif