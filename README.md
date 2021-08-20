# Tile-Puzzle-Solver
## Objective
Implement code to solve 3-puzzles, 8-puzzles and 15-puzzles. Puzzle files are formatted as follows:
2 4 3
7 1 6
5 8 X

## Implementation
The file shows the starting configuration of the tiles in the puzzle and the ‘X’ marks the location of the empty space. The puzzles are stored in sub-folders based on size. The tiles need to be rearranged to be in numerical order with the empty space at the end. For the 15-puzzle, it would look like:
*1 2 3 4
*5 6 7 8
*9 10 11 12
*13 14 15 X

Individual tiles can slide up/down/left/right into the empty space (or this can be thought of moving the empty space up/down/left/right by swapping it with the relevant adjacent tile). Puzzles may have more than one possible solution and some may require fewer tile swaps than others. And some will be unsolvable like:
2 1 
3 X

This program determines whether the puzzle can be solved and if so, provides a sequence of tile moves that would be needed to transform the starting configuration into the ending one. The code outputs the solution to the puzzle that it finds, as well as the number of tile moves required by the solution. This to specified by empty space moves – up, down, left, and right. If there is more than one solution, only one will be outputted. The code also tracks:

- How long in milliseconds it takes to find a solution to a particular crossword
- How many basic operations are performed
