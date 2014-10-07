"""
Search.py

Takes in an a list of rolling-die-puzzle files from the command line and, if it
exists, produces a solution.

Authors:
    Joseph Fuchs        <jjf2614@rit.edu>
    Damien Cremilleux   <dxc9849@rit.edu>

Dates editted:
    Oct, 7th.  2014     (initial revision)
"""

import sys
import Search
from copy import deepcopy
from Die import Die
from Board import Board
from BoardNode import *
from Search import aStarSearch

class NoStartError(Exception):
    def __init__(self,message):
        super(Exception,self).__init__(message)

def getStartLocation(filename):
    row = 0
    for line in file:
        for col in range(0,len(line)):
            if line[col] == board.START:
                return (row,col)
        row = row + 1
    raise NoStartError("Board has no start location: "+filename)

def main():
    if len(sys.argv) == 0:
        print ("No Rolling-Die-Puzzle file provided.  Now exiting")
        return
    for filename in sys.argv:
        try:
            board = Board(filename)
            startLocation = getStartLocation(filename)
            startDie = Die()
            
            for heuristicFunction in SequenceOfHeuristics:
                startNode = BoardNode(board,startLocation,startDie)
                path = aStarSearch(heuristicFunction,startNode)
                for direction in path:
                    print (Directions.directionToString(direction))
                print ("")
                print ("Length: " + str(len(path))):
                print ("")
            
        except IOError as e:
            print (e)
        except NoStartError as e:
            print (e)
    return
            

if __name__ == "__main__":
    main()

    
    