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
class SearchNode(object):
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
        super(PathTracingSearchNode,self).__init__()
    
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
        super(EvaluatedNode,self).__init__()
        ###self._evaluation = evalFunction(self)
    
    def evaluate(self,evalFunction):
        """
        Evaluates, or reevaluates the underlying node based on the given func
        """
        self._evaluation = evalFunction(self)
    
    def getEvaluation(self):
        """
        Preconditions: only use after a call to this.evaluate(f)
        """
        return self._evaluation
    
    ##these operators assume initialization of evaluation
    #Note: DO NOT RELY ON == and != operator for the evaluation of this node:
    #              those operators compare underlying world-state
    def __lt__(self,other):
        return self._evaluation < other._evaluation
    def __le__(self,other):
        return self._evaluation <= other._evaluation
    def __gt__(self,other):
        return self._evaluation > other._evaluation
    def __ge__(self,other):
        return self._evaluation >= other._evaluation
    def __cmp__(self,other):
        return self._evaluation-other._evaluation

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
        super(BestFirstSearchNode,self).__init__()
        #note: diamond inheritence
    def notifyClosing(self):
        return
    def notifyExpansion(self):
        return
class _PrioritySet(PriorityQueue):
    """Minor Class
    Represents a priority queue combined with a set to provide O(logn) retrieval
    time as well as O(1) access time for checking contents
    """
    __slots__ = ("_hiddenSet",)
    def __init__(self,comparator):
        super(_PrioritySet,self).__init__(comparator)
        self._hiddenSet = set()#TODO: change to a map for O(logn) pushing
    def push(self,hashable):
        """
        Replaces equivalent nodes.  If they compare differently, the new one 
        will be heapified back in place
        """
        if hashable in self._hiddenSet:
            ##replace the old hashable with the new one
            for ind in range(0,len(self.heapArray)):
                if self.heapArray[ind] == hashable:
                    self.heapArray[ind] = hashable
                    self._siftUp(ind)
                    break
            for ind in range(0,len(self.heapArray)):
                if self.heapArray[ind] == hashable:
                    self._sinkDown(ind)
                    break
        else:
            super(_PrioritySet,self).push(hashable)
            self._hiddenSet.add(hashable)
    def pop(self):
        val = super(_PrioritySet,self).pop()
        self._hiddenSet.remove(val)
        return val
    def __contains__(self,item):
        return (item in self._hiddenSet)
    def find(self,hashable):
        """
        Function: SearchNode -> SearchNode
        Note that this compares world state, not other state
        """
        for ind in range(0,len(self.heapArray)):
            if self.heapArray[ind] == hashable:
                return self.heapArray[ind]

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
            ##TRACING############
            #print "Closing:"
            #print curNode
            #raw_input()
            curNode.notifyClosing()
            ###################
            closed.add(curNode)
            if curNode.isGoal():
                return curNode.getPath()
            #nodes are implemented to track their path/parent on creation
            successors = curNode.successorStates()
            for suc in successors:
                suc.evaluate(evaluationFunction)
                if (not suc in closed):
                    if (not suc in frontier):
                        ##TRACING############
                        #print "Expanding To:"
                        #print suc
                        #raw_input()
                        suc.notifyExpansion()
                        ###################
                        frontier.push(suc)
                    else:
                        #if our new one is better, swap them
                        old = frontier.find(suc)
                        if (comparator(suc,old)):
                            ##TRACING############
                            #print "Expanding To:"
                            #print suc
                            #raw_input()
                            suc.notifyExpansion()
                            ###################
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
                suc.notifyExpansion()
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
        super(AStarSearchNode,self).__init__()

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
    
    print ("TESTING: _PriorityQueue")
    pq = _PrioritySet(hasBetterUtilityThan)
    
    pq.push(1)
    pq.push(8)
    pq.push(1)
    pq.push(2)
    pq.push(8)
    pq.push(2)
    pq.push(6)
    pq.push(8)
    pq.push(5)
    pq.push(7)
    
    print (pq.heapArray == [8,6,7,1,5,2])
    print (not pq.isEmpty())
    print (pq.pop() == 8)
    print (pq.pop() == 7)
    print (pq.heapArray == [6,5,2,1])
    print (not pq.isEmpty())
    pq.push(9)
    pq.push(4)
    print (pq.heapArray == [9,6,4,1,5,2])
    print (pq.pop() == 9)
    print (pq.pop() == 6)
    print (pq.pop() == 5)
    print (pq.pop() == 4)
    print (pq.pop() == 2)
    print (pq.pop() == 1)
    print (pq.isEmpty())
    
    class Test(object):
        __slots__ = ("x","y","extra","c")
        def __init__(self,x,y,c=0):
            self.extra = (6,8889,y,3443,x,"fda")
            self.x = x
            self.y = y
            self.c = c
        def __hash__(self):
            return hash((self.x,self.y))
        def __eq__(self,other):
            return (self.x,self.y) == (other.x,other.y)
        def __ne__(self,other):
            return not self.__eq__(other)
        def __lt__(self,other):
            return self.c < other.c
        def __gt__(self,other):
            return self.c > other.c
        def __le__(self,other):
            return self.c <= other.c
        def __ge__(self,other):
            return self.c >= other.c
        def __cmp__(self,other):
            return self.c - other.c
        def __str__(self):
            return "("+str(self.x)+":"+str(self.y)+":"+str(self.c)+")"
            
    print ("")
    print ("next 4 numbers should be the same:")
    obj1 = Test(1,2,4444)
    print obj1.__hash__()
    obj1.extra = (99,89)
    print obj1.__hash__()
    pq.push(obj1)
    obj1b = pq.pop()
    print (obj1 is obj1b)
    print obj1b.__hash__()
    pq.push(obj1)
    obj2 = Test(1,2,99999)#should hash and equate to same
    print (len(pq.heapArray) == len(pq._hiddenSet) and len(pq.heapArray) == 1)
    print (obj2.__hash__())
    print (obj1 == obj2)
    pq.push(obj1)
    pq.push(obj2)
    print (len(pq.heapArray) == len(pq._hiddenSet) and len(pq.heapArray) == 1)
    obj2b = pq.pop()
    print (obj2 is obj2b)
    print (obj1 < obj2)
    pq.push(obj2b)
    obj3 = Test(8,4,5555)
    pq.push(obj3)
    obj4 = Test(8,4,10101010)
    pq.push(obj4)
    obj4b = pq.pop()
    obj2c = pq.pop()
    print (pq.heapArray == list())
    print (obj2b is obj2c)
    print (obj4b is obj4)
    print (obj4 == obj3)
    
    pq.push(obj1)#1,2,4444
    pq.push(obj1)
    pq.push(obj1)
    pq.push(Test(4,4,4))
    pq.push(Test(4,4,6666))
    
    def pr(queue):
        print ("---")
        for obj in queue.heapArray:
            print obj
    pr(pq)
    pq.push(Test(4,4,3))
    pr(pq)
    pq.push(obj4)#8,4,10101010
    pq.push(Test(4,4,4))
    pr(pq)
    pq.push(obj3)#8,4,5555
    pq.push(obj1)
    pr(pq)
    pq.push(Test(1,99,1))
    pq.push(Test(1,4,3))
    pr(pq)
    pq.push(Test(0,0,0))
    pq.push(Test(0,2,4446))
    pq.push(Test(1,99,3))
    pq.push(Test(4,4,0))
    pq.push(Test(8,4,0))
    pr(pq)
    print ("XXXXXXXXXXX")
    while (not pq.isEmpty()):
        print (pq.pop())
    
    print "--------------"
    
    newQ = _PrioritySet(hasBetterUtilityThan)
    newQ.push(Test(0,0,4))
    newQ.push(Test(1,1,4))
    
    print ("This concludes tests for Search.py")
