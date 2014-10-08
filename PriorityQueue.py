"""
PriorityQueue.py

Contains a priority queue datastructure

Authors:
    Joseph Fuchs        <jjf2614@rit.edu>
    Damien Cremilleux   <dxc9849@rit.edu>

Dates editted:
    Oct. 4th, 2014 (partially completed)
    Oct. 5th, 2014 (initial revision)
    Oct. 6th, 2014 (changed a little thing tha I can't remember)
"""

class PriorityQueue:
    
    ##Static constants
    @staticmethod
    def GREATER_THAN(objA,objB):
        """Default comparator; returns bool for objA > objB"""
        return objA > objB
    
    """
    heapArray           = the underlying heap data in array form
    isMoreImportantThan = a comparator that returns true if and only if the 
                        left argument is more important thant the right
    """
    __slots__ = ("heapArray","isMoreImportantThan")
    
    def __init__(self,comparator=PriorityQueue.GREATER_THAN):
        """
        Function: (Function: Type X Type -> bool) -> null
        
        Description: initializes
        """
        self.isMoreImportantThan = comparator
    
    def _swap(self,i,j):
        temp = self.heapArray[i]
        self.heapArray[i] = self.heapArray[j]
        self.heapArray[j] = temp
    
    def _siftUp(self,index):
        if index == 0:
            return
        bot = self.heapArray[index]
        topInd = PriorityQueue._up(index)
        top = self.heapArray[topInd]
        if (not self.isMoreImportantThan(top,bot)):
            self._swap(topInd,index)
            self._siftUp(topInd)
            return
        
    def _sinkDown(self,index):
        top = self.heapArray[index]
        leftInd = PriorityQueue._left(index)
        if (leftInd >= len(self.heapArray)):
            return
        left = self.heapArray[leftInd]
        rightInd = PriorityQueue._right(index)
        if (rightInd >= len(self.heapArray)):
            if (not self.isMoreImportantThan(top,left)):
                self._swap(index,leftInd)
                self._sinkDown(leftInd)
            return
        if (self.isMoreImportantThan(left,right)):
            if (not self.isMoreImportantThan(top,left)):
                self._swap(index,leftInd)
                self._sinkDown(leftInd)
                return
        else:
            if (not self.isMoreImportantThan(top,right)):
                self._swap(index,rightInd)
                self._sinkDown(rightInd)
                return
        if (not self.isMoreImportantThan(top,bot)):
            temp = top
            top = bot
            self._sinkDown(PriorityQueue._left(index)]
        
    @staticmethod
    def _up(index):
        if index % 2 == 0:
            return (index-2)/2
        else:
            return (index-1)/2

    @staticmethod 
    def _left(index):
        return 2*index+1

    @staticmethod
    def _right(index):
        return 2*index+2
    
    #treat public
    def push(self,obj):
        self.heapArray.append(obj)
        i = len(heapArray) - 1
        self._siftUp(i)
        
    #assumes not empty
    #treat public
    def pop(self):
        returnVal = self.heapArray[0]
        heapArray[0] = self.heapArray.pop()
        self._sinkDown(0)
        return returnVal
    
    #treat public
    def isEmpty(self):
        return len(self.heapArray) == 0

################################################################################
if __name__ == "__main__":
    print ("Unit test for PriorityQueue.py mechanics:  Should return no falses")
    
    print ("TODO: DEVELOP SOME UNIT TESTS FOR THE PriorityQueue")
    
    print ("This concludes tests for PriorityQueue.py")