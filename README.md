# Maze Generator & Solver

## The maze generator work

The generator starts with all walls intact, creating a complete grid. A virtual "mouse" is placed at cell (1,1). 

At each step:
1. The mouse checks its four neighbors (up, down, left, right)
2. It identifies unvisited cells (those with all four walls still intact)
3. If there are candidates, it randomly chooses one
4. It eats through the wall between current cell and chosen cell
5. Any other candidate cells are saved on a stack for later
6. The mouse moves to the chosen cell and repeats
7. When the mouse reaches a dead end with no unvisited neighbors, it pops a previous cell from the stack and continues from there
8. The process ends when the stack is empty (all cells visited)

This stack-based approach creates a perfect maze where every cell is reachable and there is exactly one unique path between any two cells.

## Maze Solver (Backtracking)

The solver uses backtracking to find the path from start to end:
- Red dot shows current position
- Blue dots mark dead ends that were backtracked
- The solver explores paths until it reaches the end

## Bonus Feature

When generating with 'W' instead of 'G', there is a 1 in 20 chance that the mouse eats an extra wall. This creates cycles (loops) in the maze, shown as purple walls. Cycles can defeat the shoulder-to-wall rule.

## Controls

- G : Generate normal maze
- W : Generate maze with cycles (bonus)
- R : Reset to empty grid
- SPACE : Solve the maze
- ESC : Quit

## Data Structure

The maze uses two arrays as required:
- northWall[R][C] : 1 if cell has upper wall, 0 if missing
- eastWall[R][C] : 1 if cell has right wall, 0 if missing
- Phantom row 0 and column 0 handle boundary edges

## How to Run

pip install -r requirements.txt
python main.py

## Video Demo