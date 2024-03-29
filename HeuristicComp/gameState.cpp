#include "gameState.h"
#include <string>
#include <iomanip>

// pretty board formatter
std::ostream& operator<<(std::ostream& os, const gameBoard& board) {
	// print top border
	os << "--------------------------------------" << std::endl;

	// print north row
	os << "|   ";
	for (int i = holes - 1; i >= 0; i--) {
		os << std::setw(3) << board[i] << ' ';
	}
	os << "     |" << std::endl;

	// print score row
	os << '|' << std::setw(3) << board[holes] << "                            "
		<< std::setw(3) << board.back() << "  |" << std::endl;

	// print south row
	os << "|   ";
	for (int i = holes + 1; i < boardSize - 1; i++) {
		os << std::setw(3) << board[i] << ' ';
	}
	os << "     |" << std::endl;


	// print bottom border
	os << "--------------------------------------";	

	return os;
}

// insertion operator overload for gameState
std::ostream& operator<<(std::ostream& os, const gameState& state) {
	os << state.board;
	return os;
}

// default constructor
gameState::gameState() :board(defaultBoard), currentPlayer(1), 
	gameOver(false), firstTurn(true) {}

// returns the player whos turn it isn't
int gameState::otherPlayer() const {
	return otherPlayer(currentPlayer);
}

// returns the number of the player opposite to the player entered
int gameState::otherPlayer(int player) const {
	return (player + 1) % 2;
}

// convert a hole number to a board index for the current player
int gameState::holeIndex(int hole) const {
	return holeIndex(hole, currentPlayer);
}

// convert a hole number to a board index for the given player
int gameState::holeIndex(int hole, int player) const {
	if (hole < 1 || hole > holes) {
		throw std::string("Invalid hole number!");
	}
	return player * (holes + 1) + hole - 1;
}


// pass all seeds left on the board to the specified player
void gameState::giveRemainingSeedsToPlayer(int player) {
	std::array<short int,2> finalScores = scores();
	
	// count seeds left on board
	short int seedsRemaining = short(totalSeeds - finalScores[0] - finalScores[1]);
	
	// clear the board of all seeds
	for (short int& hole : board) {
		hole = 0;
	}
	
	// set the scores for each player, givin all remaining seeds to the
	// specified player
	board[scoreHoles[player]] = short(finalScores[player] + seedsRemaining);
	board[scoreHoles[otherPlayer(player)]] = finalScores[otherPlayer(player)];
}

// returns the value of the state
float gameState::getValue(int player) const {
	return float(board[scoreHoles[player]] 
		- board[scoreHoles[otherPlayer(player)]]);
}

// returns a set of possible moves for the current player
std::set<int> gameState::movesAvailable() const {
	return movesAvailable(currentPlayer);
}

// returns a set of possible moves for the player specified
std::set<int> gameState::movesAvailable(int player) const {
	std::set<int> moves;
	for (int i = 1; i <= holes; i++) {
		if (board[holeIndex(i, player)] > 0) moves.insert(i);
	}

	return moves;
}

// return an array of scores [north's score, south's score]
std::array<short int, 2> gameState::scores() const {
	return { board[scoreHoles[0]], board[scoreHoles[1]] };
}

// returns the state that would result from a given move
gameState gameState::moveResult(int pos) const {
	// get board index of selected hole
	int selectedPos = holeIndex(pos);

	// get number of seeds in selected hole, check there's atleast 1
	int numOfSeeds = board[selectedPos];
	if (numOfSeeds < 1) throw std::string("Illegal move attempted!");

	// create a new state as a deep copy of the current one
	gameState newState = *this;

	// take seeds from selected hole
	newState.board[selectedPos] = 0;

	// place seeds in subsequent holes (ignoring opponent's score hole)
	while (numOfSeeds > 0){
		// move around the board (looping to start if necassary)
		selectedPos++;
		selectedPos %= boardSize;

		// if not opponents score hole, deposit a seed
		if (selectedPos != scoreHoles[otherPlayer()]) {
			newState.board[selectedPos]++;
			numOfSeeds--;
		}
	}

	// check if landed on own hole
	bool performedCapture = false;
	if (holeIndex(1) <= selectedPos && holeIndex(holes) >= selectedPos) {
		// if so check if it has only 1 seed and the opposite hole is empty
		int oppositePos = 2 * holes - selectedPos;
		short int seedsInCurrentPos = newState.board[selectedPos];
		short int seedsInOppositePos = newState.board[oppositePos];
		if (seedsInCurrentPos == 1 && seedsInOppositePos > 0) {
			// if so perform capture
			performedCapture = true;
			newState.board[selectedPos] = 0;
			newState.board[oppositePos] = 0;
			newState.board[scoreHoles[currentPlayer]] = short(
				newState.board[scoreHoles[currentPlayer]] 
				+ 1 + seedsInOppositePos);
		}
	}

	// check for game over
	for (int player = 0; player <= 1; player++) {
		// if one of the player's side is empty
		if (newState.movesAvailable(player).empty()) {
			// give the remaining seeds to the other player
			newState.giveRemainingSeedsToPlayer(otherPlayer(player));

			// game over
			newState.gameOver = true;
		}
	}

	// change current player if turn is over
	if (selectedPos != scoreHoles[currentPlayer] 
		|| firstTurn || performedCapture) {

		newState.firstTurn = false;
		newState.currentPlayer = otherPlayer();
	}

	// return resultant state
	return newState;
}

// check if the state represents a game over state
bool gameState::isGameOver() const {
	return gameOver;
}

// returns the number of the player who's turn it is
int gameState::getCurrentPlayer() const {
	return currentPlayer;
}

// returns a copy of the gameBoard
const gameBoard& gameState::getGameBoard() const {
	return board;
}
