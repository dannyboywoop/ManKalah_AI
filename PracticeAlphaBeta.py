# Alpha-Beta Pruner -- Daniel Holmes -- 2018
import math

# basic AI implemented MiniMax search with ALpha-Beta pruning
class AlphaBetaAI:    
    # initializer
    def __init__(self, maxDepth):
        # maxDepth is the maximum depth of the tree to search
        # before using a heuristic
        self.maxDepth = maxDepth
        return
    
    # attempts to find the best available move, given a game state
    def chooseMove(self, state):
        # simple count of nodes checked before move decided
        self.nodesChecked = 0
        
        # used to initialize alpha and beta
        inf = float('inf') 
        
        # perform search for best move
        evaluation = self.evaluate(state,self.maxDepth,-inf,inf) 
        
        # print number of nodes checked before move was decided
        print("{} nodes checked".format(self.nodesChecked))
        
        # returns the best move, the resulting state and 
        # the expected value as a tuple
        return evaluation
        
    # evaluates the optimal move and expected value
    # of a game state, searching to a maximum depth of depthToSearch
    def evaluate(self, node, depthToSearch, alpha, beta):
        # increment number of nodes checked
        self.nodesChecked+=1
        
        # initialize return values
        bestMove, nextState = None, None
        
        # if maximum depth reached or at terminal node
        # return the value of the state
        if (depthToSearch==0 or node.isTerminal()):
            return bestMove, nextState, node.getValue()
        
        # get a dictionary of the possible moves and resultant states
        # from the given state
        children = node.getChildren()
        
        # if the current state is a max node
        if node.isMaxNode():
            value = -float('inf')
            
            # for each possible move
            for move, child in children.items():
                # check the expected value of the move
                _,_,checkValue = self.evaluate(child,depthToSearch-1,alpha,beta)
                
                # if expected value is better than current best
                # set that move (and value) as new best
                if checkValue > value:
                    value = checkValue
                    bestMove, nextState = move, child
                    
                # update alpha if appropriate
                alpha = max(alpha, value)
                
                # prune current node if possible
                if (alpha >= beta):
                    break
                
            # return the bestMove, the state that results from that move
            # and the expected value associated with this move as a tuple
            return bestMove, nextState, value
        
        # else if the current state is a min node
        else:
            value = float('inf')
            
            # for each possible move
            for move, child in children.items():
                # check the expected value of the move
                _,_,checkValue = self.evaluate(child,depthToSearch-1,alpha,beta)
                
                # if expected value is better than current best
                # set that move (and value) as new best
                if checkValue < value:
                    value = checkValue
                    bestMove, nextState = move, child
                    
                # update beta if appropriate
                beta = min(beta, value)
                
                # prune current node if possible
                if (alpha >= beta):
                    break
                
            # return the bestMove, the state that results from that move
            # and the expected value associated with this move as a tuple
            return bestMove, nextState, value
            
# implemented a basic tree for the purpose of testing
class BasicTree:
    def __init__(self, val, MAX, children = {}, ):
        self.val = val # value of the node
        self.MAX = MAX # True if the node is a max node, false otherwise
        self.children = children # dictionary of child nodes (with corresponding moves)

    # string representation of the tree
    def __str__(self, level=0, move=""):
        outputStr = "  "*level+move+str(self.val)+"\n"
        for key, child in self.children.items():
            outputStr += child.__str__(level+1,str(key)+": ")
        return outputStr
        
    # returns true if node has no children
    def isTerminal(self):
        return (len(self.children) == 0)
        
    # returns a dictionary of child nodes (with corresponding moves)
    def getChildren(self):
        return self.children
    
    # returns the value of the node if it is a terminal node
    # or its heuristic value otherwise
    def getValue(self):
        if self.isTerminal():
            return self.val
        return self.heuristicValue()
    
    # arbitrary heuristic function
    def heuristicValue(self):
        return math.sqrt(self.val)
    
    # returns whether the current node is a max node
    def isMaxNode(self):
        return self.MAX
    
    # counts number of nodes in the tree
    def nodeCount(self):
        self.numberOfNodes = 1
        for node in self.children.values():
            self.numberOfNodes+=node.nodeCount()
        return self.numberOfNodes
            
 
# below is a basic example of how the alpha-beta pruner AI works
if __name__=='__main__': 
    
    # this is the tree that we performed alpha-beta pruning on in the lectures
    exampleTree = BasicTree(0,True,{
        1:BasicTree(1,False,{
            1:BasicTree(2,True,{
                1:BasicTree(1,False,{1:BasicTree(10,True),2:BasicTree(11,True)}),
                2:BasicTree(2,False,{1:BasicTree(9,True),2:BasicTree(12,True)})
            }),
            2:BasicTree(2,True,{
                1:BasicTree(3,False,{1:BasicTree(14,True),2:BasicTree(15,True)}),
                2:BasicTree(4,False,{1:BasicTree(13,True),2:BasicTree(14,True)})
            })
        }),
        2:BasicTree(1,False,{
            1:BasicTree(2,True,{
                1:BasicTree(5,False,{1:BasicTree(5,True),2:BasicTree(2,True)}),
                2:BasicTree(6,False,{1:BasicTree(4,True),2:BasicTree(1,True)})
            }),
            2:BasicTree(2,True,{
                1:BasicTree(7,False,{1:BasicTree(3,True),2:BasicTree(22,True)}),
                2:BasicTree(8,False,{1:BasicTree(20,True),2:BasicTree(21,True)})
            })
        })
    }) 
    
    # print the example tree
    print(exampleTree)
    
    # print total number of nodes in the example tree
    print("The example tree has {} nodes\n".format(exampleTree.nodeCount()))
    
    # create an alphaBeta pruning AI with a max search depth of 4
    optimalAI = AlphaBetaAI(4)
    
    # calculate the next move
    move, nextState, expectedValue = optimalAI.chooseMove(exampleTree)
    
    # print the results
    print("{} is the best move!".format(move))
    print("{} is the expected payoff".format(expectedValue))
    print("The resultant state would be:")
    print(nextState)
