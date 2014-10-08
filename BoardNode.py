"""
BoardNode.py

Implements SearchNode in Search.py

Authors:
    Joseph Fuchs        <jjf2614@rit.edu>
    Damien Cremilleux   <dxc9849@rit.edu>

Dates editted:
    Oct. 5th, 2014 (partially completed)
    Oct. 6th, 2014 (initial revision)
"""

from Search import AStarSearchNode

from Directions import *

class BoardNode(AStarSearchNode):
    """
    Provides search state for the board puzzle
    
    Caution: make sure this object and it's components are treated as constants;
                do not change them, except for this.path and this.board
    """
    
    """Treat these as public and use them in the heuristic functions
    Board       board       = the board object that corresponds to this state
    (int,int)   location    = the (row, column) tuple of the die location
    Die         die         = the die object that corresponds to die state.
    tuple(Direction) path   = the moves taken from initial state to get here
    """
    __slots__ = ("board","location","die","path")
    
    def __init__(self,board,location,die,path=tuple()):
        """
        Function: Board -> null
        
        Description: All Board Nodes will share the same board object, but 
        different locations and dice.
        """
        super(BoardNode,self).__init__()
        self.board = board
        self.location = location
        self.die = die
        self.path = path
        #############
        #DEBUGGING: Prints movement as nodes are created
        #print self
        #raw_input()
        #############
    
    def __str__(self):
        result = "NODE:\n"
        result += "Location: "+str(self.location)+"\n"
        result += "Die:      "+str(self.die.getTop())+"\n"
        result += "  ud:"+str(self.die._upDown)+"\n"
        result += "  ns:"+str(self.die._northSouth)+"\n"
        result += "  ew:"+str(self.die._eastWest)+"\n"
        result += "Hash:     "+str(hash(self))+"\n"
        result += "Dir: "
        for dir in self.path:
            result += "-"+Directions.directionToString(dir)
        result += "\n"
        return result
    
    def successorStates(self):
        """
        Function: null -> collection<BoardNode>
        
        Description: retrieves a list of successor BoardNodes for this board
        node
        
        Returns: the list as described
        """
        result = list()
        for direction in self.board.getValidMoves(self.location,self.die):
            newState = self.board.nextState(direction,self.location,self.die)
            newPath = self.path + (direction,)
            newNode = BoardNode(self.board,newState[0],newState[1],newPath)
            result.append(newNode)
        return result
    
    def isGoal(self):
        """
        Function: null -> boolean
        
        Description: determines if the given search node represents a goal 
        state
        
        Returns: True if this node is a goal state
        """
        return self.board.isGoal(self.location,self.die)
    
    def getPath(self):
        """
        Function: null -> sequence<Direction>
        
        Description: retrieves the path from the start position that brought us
        to this current location and orientation
        
        Returns: the path that brought us to this current location
        """
        return self.path
    
    def evaluatePath(self):
        """
        Function: null -> int
        
        Description: Finds the number of movements (cost) it took to get to this
        world state.
        
        Returns: the number of movements (cost) to get to this world state
        """
        return len(self.path)
    
    #allow use with == operator and use in sets or hashmaps
    def __eq__(self,other):
        diceEqual = (self.die == other.die)
        locationsEqual = (self.location == other.location)
        return (diceEqual and locationsEqual)
    def __ne__(self,other):
        return not self.__eq__(other)
    def __hash__(self):
        dieHash = self.die.__hash__()
        return hash((dieHash, self.location))


################################################################################
##Friendly evaluation functions for BoardNode objects

def heuristicTest(BoardNode):
    """If used in A*, the search will be Uniform-Cost search"""
    return 0#returning 0 will only look at the path cost and ignore heuristics
    
    ############################################################################
    ##Enter our 3 heuristic functions below.
    ##
    ##They take one argument, a BoardNode object, and return an estimated cost
    ##value.
    ############################################################################


    #TODO:

################################################################################

#this is used by Main.py as the list of heuristics for it to use
SequenceOfHeuristics = (heuristicTest,)

################################################################################
if __name__ == "__main__":
    print ("Unit test for BoardNode.py mechanics:  Should return no falses")
    
    print ("TODO: DEVELOP SOME UNIT TESTS FOR THE BoardNode class")
    
    print ("This concludes tests for BoardNode.py")
