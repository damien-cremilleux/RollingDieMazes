"""
Main.py

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
from Board import NoStartError

def main():
    if len(sys.argv) == 1:
        print ("No Rolling-Die-Puzzle file provided.  Now exiting")
        return
    for i in range(1,len(sys.argv)):
        filename = sys.argv[i]
        try:
            board = Board(filename)
            startLocation = board._dieLocation
            startDie = Die()
            
            for heuristicFunction in SequenceOfHeuristics:
                print ("")
                raw_input("Press ENTER to continue to next heuristic")
                print ("")
                print ("Heuristic Function: "+heuristicFunction.__name__)
                print (board)
                closedCounter = Counter()#global counter for node closing
                frontierCounter = Counter()#global counter for node expansion
                emptyPath = tuple()
                startNode = BoardNode(board,startLocation,startDie,closedCounter,frontierCounter,emptyPath)
                path = aStarSearch(heuristicFunction,startNode)
                if path:#if path is found
                    for direction in path:
                        board.moveDie(direction)
                        print (board)
                    print ("")
                    print ("Length: " + str(len(path)))
                else:#if path not found
                    print ("No Solution")
                print ("Number Visited:  "+str(closedCounter.getCount()))
                print ("Number Expanded: "+str(frontierCounter.getCount()))
                print ("End of heuristic '"+heuristicFunction.__name__+"'")
                ##reset board for next heuristic
                board._die = Die()
                board._dieLocation = startLocation
            
        except IOError as e:
            print (e)
        except NoStartError as e:
            print (e)
    return
            

if __name__ == "__main__":
    main()

    
    