"""
Board.py

Creates a board data structure that models the Rolling Die Maze problem

Authors:
    Joseph Fuchs        <jjf2614@rit.edu>
    Damien Cremilleux   <dxc9849@rit.edu>

    Oct. 4th, 2014 (partially completed)
    Oct. 5th, 2014 (initial revision)
    Oct. 6th, 2014 (added equality and hash functions)
    Oct. 7th, 2014 (added tests)
"""

import re
from copy import deepcopy

from Directions import *
from Die import *

class NoStartError(Exception):
    def __init__(self,message):
        super(Exception,self).__init__(message)

class Board(object):
    """
    Represents a model of a board for a Rolling Die Maze puzzle.
    
    Tracks a dice position and handles mechancis regarding movement
    
    Currently, the die location is decoupled from the board, and shows up as a
    FREE space on the board.
    """
    
    ##TODO: consider implementing as Cell object
    ##Also TODO: consider moving this to a distinct Input/Output class
    #Static constants:
    #do not change during runtime
    OBSTACLE = '*'
    FREE     = '.'
    GOAL     = 'G'
    START    = 'S'
    
    """
    tuple[int]          dieLocation = the (row,column) position of the die
    Die                 die         = the die object in the current puzzle
    array[Cell][Cell]   grid        = the grid that holds cell info
    
    If a Cell object is not simply a character, then see Cell.py.
    Otherwise, Cell.py doesn't exist yet and we are using string literals
    """
    __slots__ = ("_dieLocation","_die","_grid","_goalLocation")
    
    def __init__(self,boardFile):
        """
        Function: string -> null
        
        See: README.txt for details on the format of a valid board string.
        TODO: actually do that ^
        
        Description: Makes a Board object from a formatted board file
        
        Preconditions:  The boardString must be a valid board file
        """
        self._grid = list()
        tmpGrid = list()        # Temporary grid, used for formatting
        f = open(boardFile,"r")
        for line in f:
            tmpGrid.append(line)

        row = 0
        col = -1
        for line in tmpGrid:
            self._grid.append(line.split())
            if Board.START in line.split():
                col = line.split().index(Board.START)
                self._dieLocation = (row,col)
            if Board.GOAL in line.split():
                col = line.split().index(Board.GOAL)
                self._goalLocation = (row,col)
            row = row + 1
        if col < 0:
            raise NoStartError("Board has no start location: "+filename)
        self._die = Die()

    def __str__(self):
        """
        Function: null -> string
        
        Description: Return a formatted string representing the board
        """
        resultString = ""
        rNum = 0
        for row in self._grid:
            cNum = 0
            for elem in row:
                if (rNum,cNum) == self._dieLocation:
                    resultString = resultString + "D" + " "
                else:
                    resultString = resultString + elem + " "
                cNum = cNum + 1
            resultString = resultString + "\n"
            rNum = rNum + 1
        ###die info
        resultString = resultString + str(self._die) + "\n"
        
        return resultString

        # rowStrings = re.split('\s+',boardString)#split and remove endline chars
        # rowLength = 0#length of rows
        # for rNum in range(0,len(rowStrings)):
        #     rowStr = rowStrings[rNum]
            
        #     #detects trailing rows at end of board
        #     if (len(rowStr) < rowLength):
        #         break
        #     else:
        #         rowLength = len(rowStr)
            
        #     #sticks row to the end of our row list
        #     newRow = rowStr.split("",rowStr)
        #     for cNum in range(0,len(newRow)):
        #         ##TODO: convert newRow[cNum] from a character to Cell object
        #         ##      equivalent.  (currently this is not necessary)
        #         if newRow[cNum] == Board.START:
        #             newRow[cNum] = Board.FREE
        #             self._dieLocation = (rNum,cNum)
        #             self._die = Die()
        #     self._grid.append(newRow)
        
    # TODO: check multiple constructors
    # def __init__(self,width,height,startRow,startCol,goalRow,goalCol):
    #     """
    #     Function: int X int -> null
        
    #     Description: Initializes a board to an empty board with the die 
    #     initialized at the given start coordinates and the goal at the other 
    #     given coordinates.  Note that (0,0) is the top left cell of the grid.
        
    #     width is the number of columns
    #     height is the number of rows
        
    #     The board will not have obstacles initialized yet if you call this
    #     constructor
        
    #     Preconditions:
    #         startRow and startCol must correspond to a FREE space on the board
    #     """
    #     #init grid
    #     self._grid = Board._newGrid(height,width)
    #     for i in range(0,height):
    #         for j in range(0,width):
    #             self._grid[i][j] = Board.FREE
                
    #     #init goal position
    #     self._grid[goalRow][goalCol] = Board.GOAL
        
    #     ##init die
    #     self._dieLocation = (startRow,startCol)
    #     self._die = Die()
        
        
    ############################################################################
        
    #treat private
    @staticmethod
    def _addTuples(a,b):
        """
        Function: tuple X tuple -> tuple
        
        Description:  Performs vector addition on the two given tuples
        
        Returns: The vector sum of the two input tuples. (a1+b1,a2+b2)
        
        Preconditions: 
            -The inputs must have the same number of elements
            -The types must support the '+' operator
        """
        return (a[0]+b[0],a[1]+b[1])
                
    #treat private
    @staticmethod
    def _newGrid(numRows,numCols):
        """
        Function: int X int -> array[Cell][Cell]
        
        Description: creates a new empty grid of None values
        
        Returns: a new empty 2D grid of None values.
        """
        grid = list()
        tmpList = list()
        for nr in range(0,numRows):
            for nc in range(0,numCols):
                tmpList.append(None)
            grid.append(tmpList)
            tmpList=list()
        return grid
        
    ###########################################################################
    
    #treat public
    def getWidth(self):
        return len(self._grid[0])#number of columns
    
    #treat public
    def getHeight(self):
        return len(self._grid)#number of rows
    
    #treat public
    def isValidMoveInner(self, direction):
        """
        Function: Direction -> boolean
        
        See: Directions.py
        
        Description: determines if the given move (NORTH, SOUTH, EAST, or WEST)
        is a legal move for moving the die in the puzzle.
        
        Returns: True if the die movement on the board is legal
        """
        newPos = Board._addTuples(self._dieLocation,\
                                  Directions.toGridVector(direction))
        ##check Out Of Bounds
        if (newPos[0] >= self.getHeight() or newPos[0] < 0):
            return False
        elif (newPos[1] >= self.getWidth() or newPos[1] < 0):
            return False
        ##check for obstacle
        if (Board.OBSTACLE == self._grid[newPos[0]][newPos[1]]):
            return False
        ##check if 6 would be facing upwards
        if (self._die.getWhatTopWouldBe(direction) == 6):
            return False
        ##If we got this far, we passed our invalidation tests
        return True
    
    #treat public
    def isValidMove(self, direction, dieLoc, die):
        """
        Function: Direction X (int r,int c) X Die -> boolean
        
        See: Directions.py
        
        Description: determines if the given move on an arbitrary die at a given
        arbitrary location is a legal move for the puzzle.
        POST STATE OF ALL DATA EQUALS PRE STATE.
        
        Returns: True if the die movement on the board is legal
        """
        actualLoc = self._dieLocation
        actualDie = self._die
        self._dieLocation = dieLoc
        self._die = die
        result = self.isValidMoveInner(direction)
        self._dieLocation = actualLoc
        self._die = actualDie
        return result
        
    #treat public
    def getValidMovesInner(self):
        """
        Function: null -> array[Direction]
        
        See: Directions.py
        
        Description: produces a list of all valid movements that the die can 
        currently make given the current board state.
        
        Returns: a list of all valid moves (NORTH, SOUTH, EAST, WEST)
        """
        moves = list()
        for dir in [Directions.NORTH,Directions.EAST,\
                    Directions.SOUTH,Directions.WEST]:
            if (self.isValidMoveInner(dir)):
                moves.append(dir)
        return moves
    
    #treat public
    def getValidMoves(self,dieLoc,die):
        """
        Function: null -> array[Direction]
        
        See: Directions.py
        
        Description: produces a list of all valid movements that a given 
        arbitrary die can make at a given arbitrary location.
        
        POST STATE OF ALL DATA EQUALS PRE STATE.
        
        Returns: a list of all valid moves (NORTH, SOUTH, EAST, WEST)
        """
        actualLoc = self._dieLocation
        actualDie = self._die
        self._dieLocation = dieLoc
        self._die = die
        result = self.getValidMovesInner()
        self._dieLocation = actualLoc
        self._die = actualDie
        return result
        
    #treat public
    def moveDie(self,direction):
        """
        Function: Direction -> null
        
        See: Directions.py
        
        Description: moves the die, wherever it is on the board in the given
        direction by 1 grid unit, and also handles it's rotation.
        
        Preconditions: the direction of movement must be valid.  Precede this
        function call with board.isValidMove(dir) or otherwise know that it is
        valid.
        
        Mutates: the board changes as described.
        """
        self._dieLocation = Board._addTuples(self._dieLocation,\
                                  Directions.toGridVector(direction))
        self._die.rotate(direction)
    
    #treat public
    def nextState(self,direction,location,die):
        """
        Function: Direction -> ((int,int), Die)
        
        See: Directions.py
        
        Description: moves the die, wherever it is on the board in the given
        direction by 1 grid unit, and also handles it's rotation.
        
        DOES NOT CHANGE INPUT STATE, BUT RETURNS A NEW STATE; COPIES DIE OBJ
        
        Preconditions: the direction of movement must be valid.  Precede this
        function call with board.isValidMove(dir) or otherwise know that it is
        valid.
        
        Returns: a tuple, ((new loc row,new loc col), new Die)
        """
        newLocation = Board._addTuples(location,\
                                  Directions.toGridVector(direction))
        # TODO: check change with location instead of _dieLocation
        newDie = deepcopy(die)
        newDie.rotate(direction)
        return (newLocation,newDie)
    
    #treat public
    def isGoalInner(self):
        """
        Function: null -> boolean
        
        Description: finds if the board is in it's goal state
        
        Returns: True if the die is in goal state:
                    Die has 1 on top and is on the G location
        """
        tileValue = self._grid[self._dieLocation[0]][self._dieLocation[1]]
        if (tileValue == Board.GOAL):
            return self._die.getTop() == 1
        else:
            return False
        
    #treat public
    def isGoal(self,location,die):
        """
        Function: null -> boolean
        
        Description: finds if an arbitrary die and die-location would result in
        a victory for this board layout.
        
        Returns: True if the location and die would result in a goal state.
        """
        tileValue = self._grid[location[0]][location[1]]
        if (tileValue == Board.GOAL):
            return die.getTop() == 1
        else:
            return False


################################################################################
if __name__ == "__main__":
    print ("Unit test for Board.py mechanics:  Should return no falses")
  
    # Constructor test
    b1 = Board("puzzles/puzzle1.txt")
    print b1

    # Private functions test
    add = Board._addTuples((2,4),(3,9))
    print add == (5,13)

    g = Board._newGrid(2,2)
    print g == [[None, None],[None,None]]

    # Public functions test
    print b1.getWidth() == 5
    print b1.getHeight() == 2

    d = Die()
    dieLoc = (0,0)
    print b1.isValidMove(Directions.NORTH, dieLoc, d) == False
    print b1.isValidMove(Directions.SOUTH, dieLoc, d) == True
    print b1.isValidMove(Directions.EAST, dieLoc, d) == True
    print b1.isValidMove(Directions.WEST, dieLoc, d) == False

    dieLoc = (1,4)
    print b1.isValidMove(Directions.NORTH, dieLoc, d) == True
    print b1.isValidMove(Directions.SOUTH, dieLoc, d) == False
    print b1.isValidMove(Directions.EAST, dieLoc, d) == False
    print b1.isValidMove(Directions.WEST, dieLoc, d) == True


    b2 = Board("puzzles/puzzle2.txt")
    print b2

    dieLoc = (1,1)
    print b2.isValidMove(Directions.NORTH, dieLoc, d) == True
    print b2.isValidMove(Directions.SOUTH, dieLoc, d) == False
    print b2.isValidMove(Directions.EAST, dieLoc, d) == False
    print b2.isValidMove(Directions.WEST, dieLoc, d) == True

    d.rotate(Directions.NORTH)
    print d.getTop() == 5

    dieLoc = (3,0)
    print b2.isValidMove(Directions.NORTH, dieLoc, d) == False
    print b2.isValidMove(Directions.SOUTH, dieLoc, d) == False
    print b2.isValidMove(Directions.EAST, dieLoc, d) == True
    print b2.isValidMove(Directions.WEST, dieLoc, d) == False

    dieLoc = (3,3)
    print b2.getValidMoves(dieLoc,d) == [Directions.EAST, Directions.SOUTH, Directions.WEST]
    
    b2._die = d
    b2._dieLocation = dieLoc
    b2.moveDie(Directions.EAST)
    print b2._dieLocation == (3,4)
    print b2._die.getTop() == 4

    b3 = Board("puzzles/puzzle3.txt")
    print b3
    
    d = Die()
    dieLoc = (1,0)

    ns = b3.nextState(Directions.NORTH, dieLoc, d)
    print ns[0] == (0,0)
    print ns[1].getTop() == 5

    dieLoc = (4,5)
    print b3.isGoal(dieLoc, d) == True

    
    print ("This concludes tests for Board.py")
    
