"""
Search.py

Contains generic search algorithms for solving puzzles.

Contains a heirarchy of generic search node classes that each hold extended 
features useful for various search algorithms that use them.

Authors:
    Joseph Fuchs        <jjf2614@rit.edu>
    Damien Cremilleux   <dxc9849@rit.edu>

Dates editted:
    Oct. 4th, 2014 (partially completed)
    Oct. 5th, 2014 (partially completed)
    Oct. 6th, 2014 (initial revision)
"""

from PriorityQueue import *

################################################################################
class SearchNode:
    """Interface
    An interface that is used by the search functions.  A search node can have
    some changing members, but THE WORLD STATE MUST ALWAYS REMAIN CONSTANT so 
    that a SearchNode may be used in hashsets and hashmaps.
    
    all world state must be immutable
    """
    
    def successorStates(self):
        """
        Function: null -> collection<SearchNodes>
        
        SUBCLASSES MUST IMPLEMENT THIS
        
        Description: Creates a list of successor states that can be expanded
        upon by our search
        
        Returns: a list of successor states of this search node
        """
        raise Exception("successorStates not implemented for "\
                        +self.__class__.__str__())
    
    def isGoal(self):
        """
        Function: null -> bool
        
        SUBCLASSES MUST IMPLEMENT THIS
        
        Description: determines if this search node represents goal state
        
        Returns: True iff the state is a goal
        """
        raise Exception("isGoal not implemented for "+self.__class__.__str__())
    
    """IMPORTANT
    All implementing subclasses should implement the following such that any
    two SearchNodes are equal if they have the same state.  Note that 
    implementing subclasses SHOULD NOT every change world state once the node is
    created, but can change other state data.  For example, If this is being 
    used for a board game search, the world state (the state of the board) 
    should never be altered after the node is created, but we can alter other
    state that the search algorithm might want to use.
    """
    def __eq__(self,other):
        """
        True if and only if self.worldState == other.worldState
        """
        raise Exception("__eq__ not implemented for "+self.__class__.__str__())
    def __ne__(self):
        """
        True if and only if self.worldState != other.worldState
        """
        raise Exception("__ne__ not implemented for "+self.__class__.__str__())
    def __hash__(self):
        """
        A number such that two SearchNodes with same worldState produce the same 
        number.
        """
        raise Exception("__hash__ not implemented for "\
                        +self.__class__.__str__())

################################################################################  
class PathTracingSearchNode(SearchNode):
    """Interface
    An interface for a search node that can fetch a backtracked path from the 
    start node.
    
    Used in Best First Search
    """
    
    def __init__(self):
        super(SearchNode,self).__init__()
    
    def getPath(self):
        """
        Function: null -> <Arbitrary data type that represents path>
        
        SUBCLASSES MUST IMPLEMENT THIS
        
        Description: constructs or fetches an object that represents the steps
        taken from the start node to reach this node.
        
        Returns: the path from start state to this state
        """
        raise Exception("getPath not implemented for "+self.__class__.__str__())
    
    def evaluatePath(self):
        """
        Function: null -> int
        
        SUBCLASSES MUST IMPLEMENT THIS
        
        Description: finds the evaluation (cost or utility) that taking the
        path from initial state to this state accumulated.
        
        Returns: the cost or utility value of reaching this state through the
        used path.
        """
        raise Exception("evaluatePath not implemented for "+\
                        self.__class__.__str__())

################################################################################
class EvaluatedNode(SearchNode):
    """Abstract Class
    Records the evaluation of a node given an evaluation function
    """
    
    __slots__ = ("_evaluation",)
    
    ###def __init__(self,evalFunction):
    def __init__(self):##WE MUST EVALUATE LATER
        super(SearchNode,self).__init__()
        ###self._evaluation = evalFunction(self)
    
    def evaluate(self,evalFunction):
        """
        Evaluates, or reevaluates the underlying node based on the given func
        """
        self._evaluation = evalFunction(self)
    
    def getEvaluation(self):
        return self._evaluation
    
    ##these operators assume initialization of evaluation
    #Note: DO NOT RELY ON == and != operator for the evaluation of this node
    def __lt__(self,other):
        return self._evaluation < other._evaluation
    def __le__(self,other):
        return self._evaluation <= other._evaluation
    def __gt__(self,other):
        return self._evaluation > other._evaluation
    def __ge__(self,other):
        return self._evaluation >= other._evaluation
    def __cmp__(self,other):
        return ##TODO

################################################################################
#####BEST FIRST SEARCH##########################################################

##x and y are tuples: (eval, SearchNode)
def hasLowerCostThan(x,y):
    """x and y are EvaluatedNodes"""
    return x<y
def hasBetterUtilityThan(x,y):
    """x and y are EvaluatedNodes"""
    return x>y

class BestFirstSearchNode(EvaluatedNode,PathTracingSearchNode):
    """Abstract Class
    User must implement needed methods
    """
    def __init__(self):
        super(EvalutedNode,self).__init__()
        super(PathTracingSearchNode,self).__init__()
        #note: possible double call to SearchNode.__init__()

class _PrioritySet(PriorityQueue):
    """Minor Class
    Represents a priority queue combined with a set to provide O(logn) retrieval
    time as well as O(1) access time for checking contents
    """
    __slots__ = ("_hiddenSet",)
    def __init__(self,comparator):
        super(PriorityQueue,self).__init__(comparator)
        self._hiddenSet = set()#TODO: change to a map for O(logn) pushing
    def push(self,hashable):
        """
        Replaces equivalent nodes.  If they compare differently, the new one 
        will be heapified back in place
        """
        if hashable in self._hiddenSet:
            ##replace the old hashable with the new one
            for ind in range(0,len(self._heapArray)):
                if self._heapArray[ind] == hashable:
                    self._heapArray[ind] = hashable
                    self._siftUp(ind)
                    break
            for ind in range(0,len(self._heapArray)):
                if self._heapArray[ind] == hashable:
                    self._sinkDown(ind)
                    break
        else:
            super(PriorityQueue,self).push(hashable)
            self._hiddenSet.add(hashable)
    def pop(self):
        val = super(PriorityQueue,self).pop()
        self._hiddenSet.remove(val)
    def __contains__(self,item):
        return (item in self._hiddenSet)
    def find(self,hashable):
        """
        Function: SearchNode -> SearchNode
        Note that this compares world state, not other state
        """
        for ind in range(0,len(self._heapArray)):
            if self._heapArray[ind] == hashable:
                return self._heapArray[ind]

def bestFirstSearch(evaluationFunction,startNode,\
                    graphSearch=True,costMode=True):
    """
    Function: (Function: BestFSN -> int) X BestFSN -> arbitrary path datatype
    
    Description: given a search node and a node evaluation function, this
    will TRY to find a path to the goal.
    
    Warning: This function does not inherently guarantee optimality nor 
    completeness
    
    Returns: a sequence representing the path found that arrived at the goal 
    node.  The structure of the path is undefinied, and implemented by whichever
    SearchNode subclass is being used.
    
    Mutates: The search nodes may change internally only if the 
    evaluationFunction does so.
    """
    
    ##set whether we are in cost mode or utility mode
    if (costMode):
        comparator = hasLowerCostThan
    else:#set comparator to utility mode; maximize values instead of minimize
        comparator = hasBetterUtilityThan
    
    if (graphSearch):
        frontier = _PrioritySet(comparator)#doesn't store 2 w/ same world state
        startNode.evaluate(evaluationFunction)
        frontier.push(startNode)
        closed = set()
        while (not frontier.isEmpty()):
            curNode = frontier.pop()
            closed.add(curNode)
            if curNode.isGoal():
                return curNode.getPath()
            #nodes are implemented to track their path/parent on creation
            successors = curNode.successorStates()
            for suc in successors:
                suc.evaluate(evaluationFunction)
                if (not suc in closed):
                    if (not suc in frontier):
                        frontier.push(suc)
                    else:
                        #if our new one is better, swap them
                        old = frontier.find(suc)
                        if (comparator(suc,old)):
                            frontier.push(suc)#replaces old and reheapifies
        return None#return an empty path
    else:#do tree search instead
        frontier = PriorityQueue(comparator)#stores nodes with same world state
        startNode.evaluate(evaluationFunction)
        frontier.push(startNode)
        while (not frontier.isEmpty()):
            curNode = frontier.pop()
            if curNode.isGoal():
                return curNode.getPath()
            successors = curNode.successorStates()
            for suc in successors:
                suc.evaluate(evaluationFunction)
                frontier.push(suc)
        return None
            

################################################################################
#####A STAR SEARCH##############################################################
class AStarSearchNode(BestFirstSearchNode):
    """
    Represents a search node in a generic A* search.  Specific types of search
    problems should implement this abstract class
    """

    def __init__(self):
        """
        Function: int -> null

        Description: Initializes search node to a given g value
        """
        super(BestFirstSearchNode,self).__init__()

def aStarSearch(heuristicFunction,aStarSearchNode):
    """
    Function: (Function: ASSN -> int) X ASSN -> arbitrary path datatype
    
    Description: given a search node and a heuristic evaluation function, this
    will find the optimal path to the goal
    
    Returns: a sequence (an array) of search nodes that lead to the goal, with
    the Start node at the start of the sequence (index 0)
    
    Preconditions: heuristicFunction must be conistent and admissible
    
    Mutates: The search nodes will change internally
    """
    def f(assn):
        """
        Lambda Function: ASSN -> int
        """
        return heuristicFunction(assn) + assn.evaluatePath()
    return bestFirstSearch(f,aStarSearchNode)






################################################################################
if __name__ == "__main__":
    print ("Unit test for Search.py mechanics:  Should return no falses")
    
    print ("TODO: DEVELOP SOME UNIT TESTS FOR THE Search")
    
    print ("This concludes tests for Search.py")
