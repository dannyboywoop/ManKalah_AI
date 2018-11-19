# game engine must meet this spec to work with the alpha beta pruner

class gameState:
    def __init__(self):
        #initializer goes here
        
    def isTerminal(self):
        # returns whether the state is an end-game state
        # i.e. all slots empty on one side of the board
        
    def getChildren(self):
        # returns a dictionary of possible subsequent move-state pairs
        # e.g. return {1:state1, 3:state3, 4:state4}
        # note keys are the possible moves that can be made from this state
        # values are the states that would occur after the corresponding move
        
        # if no children (no possible moves), return an empty dictionary
    
    def getValue(self):
        if self.isTerminal():
            # return actual value of result of game
        else:
            return self.heuristicValue()
    
    def heuristicValue(self):
        # return the heuristic value of the current state
    
    def isMaxNode(self):
        # return True if it is the AI's turn, 
        # False if it is the opponents turn