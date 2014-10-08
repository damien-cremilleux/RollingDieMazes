"""
Die.py

Provides the Die class, which allows holding and manipulating of the state of
a die object.

Authors:
    Joseph Fuchs        <jjf2614@rit.edu>
    Damien Cremilleux   <dxc9849@rit.edu>

Dates editted:
    Oct. 4th, 2014 (initial revision)
    Oct. 6th, 2014 (added equality and hash functions)
"""

from Directions import *

class Die:
    """
    A class that keeps track of the state of a die object, as well as performing
    manipulations on the orientation rotations of dice.
    
    """
    
    #Static constants:
    #do not change during runtime
    ##these mark the initial state of a die
    _UP_DOWN     = (1,6)#(top-facing, bottom-facing)
    _NORTH_SOUTH = (2,5)#(north-facing,south-facing)
    _EAST_WEST   = (3,4)#(east-facing,west-facing)
    
    
    """treat these as private varibles
    tuple[int]  _upDown     = (top num  , bot num)
    tuple[int]  _northSouth = (north num, south num)
    tuple[int]  _eastWest   = (east num , west num)
    """
    __slots__ = ("_upDown","_northSouth","_eastWest")
    
    def __init__(self):
        """
        Function: null -> null
        
        Description: Initializes a die; used in construction of a Die object
        Initializes a Die object to the default, initial orientation:
        UP    = 1
        DOWN  = 6
        EAST  = 3
        WEST  = 4
        NORTH = 2
        SOUTH = 5
        """
        self._upDown = Die._UP_DOWN
        self._northSouth = Die._NORTH_SOUTH
        self._eastWest = Die._EAST_WEST
    
    def __eq__(self,other):
        x = self._upDown == other._upDown
        y = self._northSouth == other._northSouth
        z = self._eastWest == other._eastWest
        return (x and y and z)
    def __ne__(self,other):
        return not self.__eq__(other)
    def __hash__(self):
        """
        Assumes die state does not change.  Only use this where die objects
        are never altered
        """
        return hash((self._upDown,self._northSouth,self._eastWest))
    def __str__(self):
        return "TopFace: "+str(self.getTop())+"   NorthFace: "+\
                str(self.getNorth())+"   EastFace: "+str(self.getEast())+"\n"+\
                "BotFace: "+str(self.getBottom())+"   SouthFace: "+\
                str(self.getSouth())+"   WestFace: "+str(self.getWest())
        
    ############################################################################
    
    #treat private
    @staticmethod
    def _flippedTuple(tup):
        """
        Function: Tuple -> Tuple
        
        Description: return the reverse of a given tuple
        
        Returns: the reverse of the given tuple.
        """
        result = tuple()#empty tuple
        for elem in tup:
            result = (elem,) + result
        return result
    
    #treat private
    def _rollNorthward(self):
        """
        Function: null -> null
        
        Description: changes the orientation of the cube as if it were rolled 
        in the northward direction.  (rotated 90deg around East-West axis).
        Top will now face Northward
        
        DOES NOT CHANGE THE DIE POSITION, JUST ORIENTATION
        
        Mutates: the die will change as described
        """
        ##Step 1: swap (top,bot) with (north,south)
        tmp = self._upDown
        self._upDown = self._northSouth
        self._northSouth = tmp
        ##Step 2: make sure the previous north is rolled underneath instead of up
        self._upDown = Die._flippedTuple(self._upDown)
    
    #treat private
    def _rollSouthward(self):
        """
        Function: null -> null
        
        Description: changes the orientation of the cube as if it were rolled 
        in the southward direction.  (rotated -90deg around East-West axis).
        Top will now face Southward
        
        DOES NOT CHANGE THE DIE POSITION, JUST ORIENTATION
        
        Mutates: the die will change as described
        """
        ##do _rollNorthward's steps backwards
        self._upDown = Die._flippedTuple(self._upDown)
        tmp = self._upDown
        self._upDown = self._northSouth
        self._northSouth = tmp
    
    #treat private
    def _rollEastward(self):
        """
        Function: null -> null
        
        Description: changes the orientation of the cube as if it were rolled 
        in the eastward direction.  (rotated 90deg around North-South axis).
        Top will now face Eastward.
        
        DOES NOT CHANGE THE DIE POSITION, JUST ORIENTATION
        
        Mutates: the die will change as described
        """
        ##Step 1: swap (top,bot) with (east,west)
        tmp = self._upDown
        self._upDown = self._eastWest
        self._eastWest = tmp
        ##Step 2: make sure the previous east is rolled underneath instead of up
        self._upDown = Die._flippedTuple(self._upDown)
    
    #treat private
    def _rollWestward(self):
        """
        Function: null -> null
        
        Description: changes the orientation of the cube as if it were rolled 
        in the eastward direction.  (rotated 90deg around North-South axis).
        Top will now face Eastward.
        
        DOES NOT CHANGE THE DIE POSITION, JUST ORIENTATION
        
        Mutates: the die will change as described
        """
        ##do _rollEastward's steps backwards
        self._upDown = Die._flippedTuple(self._upDown)
        tmp = self._upDown
        self._upDown = self._eastWest
        self._eastWest = tmp
        
    
    ############################################################################
    
    #treat public
    def rotate(self,direction):
        """
        Function: Direction -> null
        
        See: Directions.py
        
        Description: Will rotate the cube towards the given direction such that
        the top side will now face that direction (NORTH, SOUTH, EAST, or WEST)
        
        Mutates: the die will change as described
        """
        if   (direction == Directions.NORTH):
            self._rollNorthward()
        elif (direction == Directions.SOUTH):
            self._rollSouthward()
        elif (direction == Directions.EAST):
            self._rollEastward()
        elif (direction == Directions.WEST):
            self._rollWestward()
        else:
            print ("Internal Error: invalid die rotation direction")
    
    #treat public
    def getTop(self):
        """
        Function: null -> int
        
        Description: returns the number that is currently on the top of this 
        die
        
        Returns: the number on the top of this die
        """
        return self._upDown[0]
        
    #treat public
    def getWhatTopWouldBe(self,direction):
        """
        Function: Direction -> int
        
        See: Directions.py
        
        Description: return what the number on top of this dice will be if it 
        were to be rotated in the given direction.
        
        Returns: what the number on top would be if rotated in input direction
        
        Mutates: the pre-state and post-state of this die will be the same by
        calling this function, but the intermediate state will be manipulated 
        for computation.  This function effectively does not change state.
        """
        self.rotate(direction)
        val = self.getTop()
        self.rotate(Directions.otherWay(direction))
        return val
    
    #treat public
    def getNorth(self):
        return self._northSouth[0]
        
    #treat public
    def getEast(self):
        return self._eastWest[0]
    
    #treat public
    def getBottom(self):
        return self._upDown[1]
    
    #treat public
    def getSouth(self):
        return self._northSouth[1]
    
    #treat public
    def getWest(self):
        return self._eastWest[1]
    


################################################################################
if __name__ == "__main__":
    print ("Unit test for Die.py mechanics:  Should return no falses")
    
    n = Directions.NORTH
    s = Directions.SOUTH
    e = Directions.EAST
    w = Directions.WEST
    
    die = Die()
    
    ##test initializing
    print (die.getTop() == 1)
    print (die.getBottom() == 6)
    print (die.getEast() == 3)
    print (die.getWest() == 4)
    print (die.getNorth() == 2)
    print (die.getSouth() == 5)
    
    
    ##test rotating eastward 4 times
    print (die.getWhatTopWouldBe(e) == 4)
    die.rotate(e)
    print (die.getTop() == 4)
    print (die.getBottom() == 3)
    print (die.getEast() == 1)
    print (die.getWest() == 6)
    print (die.getNorth() == 2)
    print (die.getSouth() == 5)
    
    print (die.getWhatTopWouldBe(e) == 6)
    die.rotate(e)
    print (die.getTop() == 6)
    
    print (die.getWhatTopWouldBe(e) == 3)
    die.rotate(e)
    print (die.getTop() == 3)

    print (die.getWhatTopWouldBe(e) == 1)
    die.rotate(e)
    print (die.getTop() == 1)
    
    
    ##test rotating westward 4 times
    print (die.getWhatTopWouldBe(w) == 3)
    die.rotate(w)
    print (die.getTop() == 3)
    print (die.getBottom() == 4)
    print (die.getEast() == 6)
    print (die.getWest() == 1)
    print (die.getNorth() == 2)
    print (die.getSouth() == 5)
    
    print (die.getWhatTopWouldBe(w) == 6)
    die.rotate(w)
    print (die.getTop() == 6)
    
    print (die.getWhatTopWouldBe(w) == 4)
    die.rotate(w)
    print (die.getTop() == 4)

    print (die.getWhatTopWouldBe(w) == 1)
    die.rotate(w)
    print (die.getTop() == 1)


    ##test rotating northward 4 times
    print (die.getWhatTopWouldBe(n) == 5)
    die.rotate(n)
    print (die.getTop() == 5)
    print (die.getBottom() == 2)
    print (die.getEast() == 3)
    print (die.getWest() == 4)
    print (die.getNorth() == 1)
    print (die.getSouth() == 6)
    
    print (die.getWhatTopWouldBe(n) == 6)
    die.rotate(n)
    print (die.getTop() == 6)
    
    print (die.getWhatTopWouldBe(n) == 2)
    die.rotate(n)
    print (die.getTop() == 2)

    print (die.getWhatTopWouldBe(n) == 1)
    die.rotate(n)
    print (die.getTop() == 1)
    
    
    ##test rotating southward 4 times
    print (die.getWhatTopWouldBe(s) == 2)
    die.rotate(s)
    print (die.getTop() == 2)
    print (die.getBottom() == 5)
    print (die.getEast() == 3)
    print (die.getWest() == 4)
    print (die.getNorth() == 6)
    print (die.getSouth() == 1)
    
    print (die.getWhatTopWouldBe(s) == 6)
    die.rotate(s)
    print (die.getTop() == 6)
    
    print (die.getWhatTopWouldBe(s) == 5)
    die.rotate(s)
    print (die.getTop() == 5)

    print (die.getWhatTopWouldBe(s) == 1)
    die.rotate(s)
    print (die.getTop() == 1)
    

    print ("This concludes tests for Die.py")