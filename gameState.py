# basic gameState class
# stores the state of the game with methods to determine subsequent states
import copy

class gameState:
    players = {
        "North" : 0,
        "South" : 1        
    }
    
    # sets up game board and selects South as the first player
    def __init__(self, holes=7, seeds=7):
        self.seeds = seeds
        self.holes = holes
        self.board = [seeds]*holes + [0] + [seeds]*holes + [0]
        self.currentPlayer = "South"
        self.gameOver = False
        self.firstTurn = True
        self.scoreSlots = [self.holes, 2 * self.holes + 1]
        return
    
    # return index of opponents score slot
    def opponentsScoreSlot(self):
        opponentsPlayerNumber = (self.players[self.currentPlayer] + 1) % 2
        return self.scoreSlots[opponentsPlayerNumber]
      
    # return index of current players score slot
    def playersScoreSlot(self):
        return self.scoreSlots[self.players[self.currentPlayer]]
    
    # converts a player's slot number [1-7] into a board index
    def slotIndex(self, slot, player = None):
        if (player == None):
            player = self.currentPlayer
        if (slot<1 or slot>self.holes):
            raise Exception("Index out of range")
        return self.players[player]*(self.holes+1) + slot - 1

    # given the name of one player, returns the name of the other
    def otherPlayer(self, player = None):
        if (player == None):
            player = self.currentPlayer
        if player == "North":
            return "South"
        if player == "South":
            return "North"

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
    
    # returns a tuple of player scores: (North's score, South's score)
    def Scores(self):
        return self.board[self.scoreSlots[0]],self.board[self.scoreSlots[1]]
    
    # returns the resultant gameState after a given move
    def moveResult(self, pos):
        # get board index of selected slot
        selectedPos = self.slotIndex(pos)
        
        # get number of seeds in selected slot there's atleast 1
        numOfSeeds = self.board[selectedPos]
        if (numOfSeeds < 1):
            raise Exception("Not a legal move!")
        
        # create a new state as a deep copy of the current one
        newState = copy.deepcopy(self)
        
        # take seeds from selected hole
        newState.board[selectedPos] = 0
        
        # place seeds in subsequent slots (ignoring opponents score slot)
        while (numOfSeeds>0):
            selectedPos+=1
            
            # loop around board if end is reached
            if (selectedPos == len(newState.board)):
                selectedPos=0
            
            # if not opponents score slot, deposit a seed
            if selectedPos != newState.opponentsScoreSlot():
                newState.board[selectedPos]+=1
                numOfSeeds-=1
        
        # check if landed on own hole
        if (newState.slotIndex(1)<=selectedPos<=newState.slotIndex(newState.holes)):
            # if so check if it has only 1 seed and the opposite hole is empty
            oppositePos = 2 * newState.holes - selectedPos
            seedsInCurrentPos = newState.board[selectedPos]
            seedsInOppositePos = newState.board[oppositePos]
            if (seedsInCurrentPos==1 and seedsInOppositePos>0):
                newState.board[selectedPos] = 0
                newState.board[oppositePos] = 0
                newState.board[newState.playersScoreSlot()] += 1 + seedsInOppositePos
                
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
        if (selectedPos != newState.playersScoreSlot() or self.firstTurn):
            newState.firstTurn = False
            newState.currentPlayer = self.otherPlayer()
                
        return newState
