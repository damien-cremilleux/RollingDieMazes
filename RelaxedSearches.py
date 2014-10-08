"""
RelaxedSearches.py

Contains implementations for the AStarSearchNode for alternate versions of

Authors:
    Joseph Fuchs        <jjf2614@rit.edu>
    Damien Cremilleux   <dxc9849@rit.edu>
"""

from Search import AStarSearchNode
from Directions import *
from Board import Board

class NoOrientationNode(AStarSearchNode):
    """
    Creates a search node for an alternate version of Rolling Die Puzzles that
    only cares about reaching the goal square, regardless of die orientation.
    
    cellCosts - a grid of cell values that store the cost as we 
    compute them.
    """
    __slots__ = ("board","location","path")
    def __init__(self,board,loc,path=tuple()):
        self.board = board
        self.location = loc
        self.path = path
        #ignore die orientation, only care about location
    def __eq__(self,other):
        return (self.location == other.location)
    def __ne__(self,other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash(self.location)
    def evaluatePath(self):
        return len(self.getPath())
    def getPath(self):
        return self.path
    def notifyClosing(self):
        return#do nothing
    def notifyExpansion(self):
        return#do nothing
    def isGoal(self):
        return self.board._goalLocation == self.location
    def successorStates(self):
        successors = list()
        for dir in (Directions.DIRECTIONS):
            change = Directions.toGridVector(dir)
            newLoc = Board._addTuples(change,self.location)
            newRow = newLoc[0]
            newCol = newLoc[1]
            if (newRow >= 0 and newRow < len(self.board._grid)):
                if (newCol >= 0 and newCol <len(self.board._grid[0])):
                    if (not self.board._grid[newRow][newCol] == Board.OBSTACLE):
                        newNode = NoOrientationNode(self.board,newLoc,self.path+(dir,))
                        successors.append(newNode)
        return successors