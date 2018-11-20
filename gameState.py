# basic gameState class
# stores the state of the game with methods to determine subsequent states
import copy

class gameState:
    players = {
        "North" : 0,
        "South" : 1        
    }
    
    # sets up game board and selects South as the first player
    def __init__(self, seeds, holes):
        self.seeds = seeds
        self.holes = holes
        self.board = [seeds]*holes + [0] + [seeds]*holes + [0]
        self.currentPlayer = "South"
        self.gameOver = False
        self.scoreSlots = [self.holes, 2 * self.holes + 1]
        return
    
    # return index of opponents score slot
    def opponentsScoreSlot(self):
        opponentsPlayerNumber = (self.players[self.currentPlayer] + 1) % 2
        return self.scoreSlots[opponentsPlayerNumber]
      
    # return index of current players score slot
    def playersScoreSlot(self):
        return self.scoreSlots[self.currentPlayer]
    
    # converts a player's slot number [1-7] into a board index
    def slotIndex(self, slot):
        if (slot<0 or slot>self.holes):
            raise Exception("Index out of range")
        return self.players[self.currentPlayer]*self.holes+1 + slot - 1

    # clone server state
    def cloneServerState(self, board, currentPlayer):
        if currentPlayer not in self.players.keys():
            raise Exception("Invalid player")
        if (len(board)!=2*(self.holes+1)):
            raise Exception("Invalid board size")
        
        self.board = board
        self.currentPlayer = currentPlayer
        
    # returns a list of available moves
    def movesAvailable(self):
        moves = []
        for i in range(1, self.holes+1):
            if (self.board[self.slotIndex(i)]!=0):
                moves += [i]
        return moves
    
    # returns a tuple of player scores: (player 1's score, player 2's score)
    def Scores(self):
        return self.board[self.scoreSlots[0]],self.board[self.scoreSlots[1]]
    
    # returns the resultant gameState after a given move
    def moveResult(self, pos):
        # get board index of selected slot
        selectedPos = self.slotIndex(pos)
        
        # get number of seeds in selected slot there's atleast 1
        numOfSeeds = self.board(selectedPos)
        if (numOfSeeds < 1):
            raise Exception("Not a legal move!")
        
        # create a new state as a deep copy of the current one
        newState = copy.deepcopy(self)
        
        # place seeds in subsequent slots (ignoring opponents score slot)
        while (numOfSeeds>0):
            selectedPos+=1
            
            # loop around board if end is reached
            if (selectedPos == len(newState.board)):
                selectedPos=0
            
            # if not opponents score slot, deposit a seed
            if selectedPos != newState.opponentsScoreSlot():
                newState.board[newState]+=1
                numOfSeeds-=1
                
        # NEED TO IMPLEMENT STEALING OF OPPOSING PLAYERS SEEDS        
                
        # check for game over (currentPlayers side is now empty)
        if (len(newState.movesAvailable()) == 0):
            # read opponents score
            opponentsFinalScore = newState.board[newState.opponentsScoreSlot()]
            
            # current player gets all remaining seeds
            currentPlayersFinalScore = newState.seeds*newState.holes*2 - opponentsFinalScore
            
            # set all board values to 0
            newState.board = [0]*(2*self.holes+2)
            
            # set final scores
            newState.board[newState.opponentsScoreSlot()] = opponentsFinalScore
            newState.board[newState.playersScoreSlot()] = currentPlayersFinalScore
            
            newState.gameOver = True
        
        # change current player if not landed on own slot
        if selectedPos != newState.playersScoreSlot():
            if self.currentPlayer == "North":
                newState.currentPlayer = "South"
            if self.currentPlayer == "South":
                newState.currentPlayer = "North"
    
    # returns the resultant gameState after a swap
    def swapResult(self):
        # create a new copy as a deep copy of the current one
        newState = copy.deepcopy(self)
        
        # swap the two halves of the board
        newState.board = (
            newState.board[:newState.holes+1] 
            + newState.board[newState.holes+1:]
        )
        
        return newState
        