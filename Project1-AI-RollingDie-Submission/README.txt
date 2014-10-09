command line usage:

$ python sdmaze.py <filename>

where <filename> is the pathname of a properly formatted Die Rolling Puzzle.

The puzzles should look something like the example below, with a space between each character and a newline at the end of each row.  Each character represents the initial contents of that grid location for the puzzle.

* - denotes an obstacle
S - denotes the Start location of a die
G - denotes the Goal tile
. - denotes an empty space

File example:
--------------------------------
. S . . *
. * . * .
* . . . .
G . . * .
. . . . .

-----------end of file-----------


Output:

The program will iterate through each of the three heuristic functions used in the A* search, and prompt you before running each of the 3 algorithms and consequently displaying the solution to the puzzle.

For each heuristic function, the program will print all states that make up the path to the goal state, starting with the Initial state of the board.  Each state will be displayed by showing that state's board representation, followed by the list of numbers on the faces of the die corresponding to how the die is oriented in that state.  After the last goal state is displayed, the program will display the length of the path (excluding initial state), followed by the number of A* search nodes visited and generated, respectively, for that heuristic function.  You will then be prompted before the program continues to the next function.