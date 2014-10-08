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
from RelaxedSearches import NoOrientationNode
from Directions import *
from Search import aStarSearch

class Counter(object):
    __slots__ = ("count")
    def __init__(self,init=0):
        self.count = init
    def countUp(self,amt=1):
        self.count = self.count + amt
    def getCount(self):
        return self.count

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
    __slots__ = ("board","location","die","path","closedCounter","frontierCounter")
    
    def __init__(self,board,location,die,closedCounter,frontierCounter,path):
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
        self.closedCounter = closedCounter
        self.frontierCounter = frontierCounter
    
    def __str__(self):
        result = "NODE:\n"
        result += "Location: "+str(self.location)+"\n"
        result += "Die:      "+str(self.die.getTop())+"\n"
        result += "  UD:"+str(self.die._upDown)+"\n"
        result += "  NS:"+str(self.die._northSouth)+"\n"
        result += "  EW:"+str(self.die._eastWest)+"\n"
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
            newNode = BoardNode(self.board,newState[0],newState[1],self.closedCounter,self.frontierCounter,newPath)
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
    
    def notifyClosing(self):
        self.closedCounter.countUp()
    def notifyExpansion(self):
        self.frontierCounter.countUp()
    
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
    
    ############################################################################
    ##Enter our 3 heuristic functions below.
    ##
    ##They take one argument, a BoardNode object, and return an estimated cost
    ##value.
    ############################################################################
def UniformCost(boardNode):
    """If used in A*, the search will be Uniform-Cost search"""
    return 0#returning 0 will only look at the path cost and ignore else

def ManhattanDistanceIgnoringOrientation(boardNode):
    r2 = boardNode.board._goalLocation[0]
    r1 = boardNode.location[0]
    c2 = boardNode.board._goalLocation[1]
    c1 = boardNode.location[1]
    return abs(r2-r1)+abs(c2-c1)

def ManhattanDistanceAccountingOrientation(boardNode):
    ##First find if the 1 on the die is facing away from goal, towards the 
    ##goal, or upwards.
    
    r2 = boardNode.board._goalLocation[0]
    r1 = boardNode.location[0]
    c2 = boardNode.board._goalLocation[1]
    c1 = boardNode.location[1]
    dr = abs(r2-r1)
    dc = abs(c2-c1)
    
    #if we our 1 is facing towards the goal: it will take dr+dc
    return
    

################################################################################

#this is used by Main.py as the list of heuristics for it to use
SequenceOfHeuristics = (UniformCost,ManhattanDistanceIgnoringOrientation,ShortestPathIgnoringOrientation)

################################################################################
if __name__ == "__main__":
    print ("Unit test for BoardNode.py mechanics:  Should return no falses")
    
    print ("TODO: DEVELOP SOME UNIT TESTS FOR THE BoardNode class")
    
    print ("This concludes tests for BoardNode.py")
