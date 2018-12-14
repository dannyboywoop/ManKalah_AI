// header guard
#ifndef GAME_STATE_H
#define GAME_STATE_H

// includes
#include <iostream>
#include <array>
#include <set>

// board constants
const int holes = 7; // number of holes on each side (excluding score hole)
const short int seeds = 7; // number of seeds in each hole
const int boardSize = 2 * holes + 2; // total number of holes (inc. score hole)
const short int totalSeeds = 2 * holes * seeds; // total number of seeds
const std::array<short int, boardSize> defaultBoard =
	{ 7,7,7,7,7,7,7,0,7,7,7,7,7,7,7,0 }; // starting configuration of board

typedef std::array<short int, boardSize> gameBoard; // gameBoard type

// insertion operator overload for printing gameBoard objects
std::ostream& operator<<(std::ostream& os, const gameBoard& board);

// gameState class stores state of Kalah game. Provides methods for determining
// subsequent moves available and the states those moves lead to.
class gameState {
// insertion operator overload for printing game states
friend std::ostream& operator<<(std::ostream& os, const gameState& state);
private:
	const int scoreHoles[2] = { holes, boardSize - 1 }; // indices of score holes
	gameBoard board; // stores state of game board
	int currentPlayer; // stores the number of the player whos turn it is
	bool gameOver; // true if the state represents a game over state
	bool firstTurn; // true if the state represents an initialized board

	// gives all seeds remaining on the board to the specified player
	void giveRemainingSeedsToPlayer(int player);

public:
	// return the value of the current state
	float getValue(int player) const;

	// return a set of moves available to the current player
	std::set<int> movesAvailable() const;

	// return a set of available to the given player
	std::set<int> movesAvailable(int player) const;

	// return the current player scores
	std::array<short int, 2> scores() const;

	// return the state that would result from the given move
	gameState moveResult(int pos) const;

	// return whether the state is a game over state
	bool isGameOver() const;

	// returns the number of the current player
	int getCurrentPlayer() const;

	// return the number of the player who's turn it isn't
	int otherPlayer() const;

	// returns the number of the player opposite to the one entered
	int otherPlayer(int player) const;

	// converts a hole number to a board index for the current player
	int holeIndex(int hole) const;

	// converts a hole number to a board index for the given player
	int holeIndex(int hole, int player) const;
	
	// returns the current state of the gameBoard
	const gameBoard& getGameBoard() const;

	// default constructor
	gameState();
};

// end header guard
#endif