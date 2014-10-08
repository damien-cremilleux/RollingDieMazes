"""
Directions.py

Creates an handles direction constants, and handles any calculations regarding
them.

Authors:
    Joseph Fuchs        <jjf2614@rit.edu>
    Damien Cremilleux   <dxc9849@rit.edu>

Dates editted:
    Oct. 4th, 2014 (initial revision)

"""

class Directions:
    """
    This class provides enumerated labels to denote directional movement on a 
    grid.  The grid's (row,col)=(0,0) location is assumed to be in the upper-
    lefthand corner of the grid.  Vectors pertaining to row-column space will 
    be in the form <number of rows, number of column>, where row number 
    increases downwards (south), and column number increases rightwards (east).
    
    Conventional cartesion coordinates are in the form (x,y), where these are 
    in (-y,x) or (row index,column index).
    
    NORTH is the upwards direction on the grid
    SOUTH is downwards direction on the grid
    
    EAST is the rightwards direction on the grid
    WEST is the leftwards direction on the grid
    
    """
    
    #STATIC CLASS CONSTANTS:
    #These are directions.
    ##do not change these during runtime; they should be constant
    NORTH = 0
    EAST  = 1
    SOUTH = 2
    WEST  = 3
    
    DIRECTIONS = (NORTH, EAST, SOUTH, WEST)
    
    @staticmethod
    def directionToString(direction):
        if direction == Directions.NORTH:
            return "NORTH"
        elif direction == Directions.EAST:
            return "EAST"
        elif direction == Directions.SOUTH:
            return "SOUTH"
        elif direction == Directions.WEST:
            return "WEST"
    
    @staticmethod
    def otherWay(direction):
        """
        Function: Direction -> Direction
        
        Description: this function will return the opposite direction to the 
        given argument direction.
        
        Returns: the opposite direction to the given one
        """
        return (direction + 2) % 4#this expression is ad hoc for current consts
    
    @staticmethod
    def toGridVector(direction):
        """
        Function: Direction -> (int,int)
        
        Description: this function will return a grid vector representing 
        a change in position of magnitude 1 in the grid direction, (dRow,dCol),
        of movement in the iven input direction.
        
        Returns: a movement vector in given direction.
        """
        #these expressions are ad hoc for current constants only
        return ( (direction-1)*((direction+1)%2), \
                 (-(direction-2))*(direction%2) )


################################################################################
if __name__ == "__main__":
    print ("Unit test for Direction.py mechanics:  Should return no falses")
    
    print (Directions.otherWay(Directions.NORTH) == Directions.SOUTH)
    print (Directions.otherWay(Directions.SOUTH) == Directions.NORTH)
    print (Directions.otherWay(Directions.EAST) == Directions.WEST)
    print (Directions.otherWay(Directions.WEST) == Directions.EAST)
    
    print (Directions.toGridVector(Directions.NORTH) == (-1,0))
    print (Directions.toGridVector(Directions.SOUTH) == (1,0))
    print (Directions.toGridVector(Directions.EAST) == (0,1))
    print (Directions.toGridVector(Directions.WEST) == (0,-1))
    
    print ("This concludes tests for Directions.py")