# Maze-Assignment
# Maze Generator and Solver (DFS + Backtracking)
# Hawi Jarso------UGR/4431/16------Section 2

## Project Overview
This project is a maze generator and solver built using Python Turtle graphics.  
It implements a Depth-First Search (DFS) algorithm with stack-based backtracking ("mouse logic") to generate a perfect maze and then solve it.

The program also visually animates both:
- Maze generation process
- Maze solving process

## How the Maze Generator Works
The maze is generated using a recursive DFS-style algorithm implemented with a stack:

1. Start at the initial cell (0, 0)
2. Mark the cell as visited
3. Randomly choose an unvisited neighbor (up, down, left, right)
4. Remove the wall between current cell and chosen cell:
   - northWall[row][col]
   - eastWall[row][col]
5. Push the next cell onto the stack
6. If no neighbors exist → backtrack using stack pop
7. Repeat until all cells are visited

This creates a perfect maze (no isolated sections, fully connected paths).


## Data Structures Used

### Wall Representation
- northWall[ROWS][COLS]
  - 1 = wall exists
  - 0 = wall removed

- eastWall[ROWS][COLS]
  - 1 = wall exists
  - 0 = wall removed

These arrays define the structure of the maze.

### Visited Tracking
- visited[ROWS][COLS]
  - Tracks whether a cell has been visited during generation

- solve_visited[ROWS][COLS]
  - Tracks visited cells during solving phase

### Stack (DFS Backtracking)
- Used in both:
  - Maze generation
  - Maze solving

It stores the path and allows the algorithm to backtrack when stuck.

## Start and Exit Points
- Start Position: (0, 0) (top-left corner)
- End Position: (ROWS-1, COLS-1) (bottom-right corner)

### Entrance and Exit Handling
- Left border has an opening at the start cell
- Right border has an opening at the end cell

## Maze Solver (Backtracking Algorithm)
The solver:
1. Starts from (0, 0)
2. Uses a stack-based DFS approach
3. Only moves through open paths (where walls = 0)
4. Marks visited cells to avoid loops
5. Backtracks when stuck
6. Stops when it reaches the exit

### Visual Output:
- 🔴 Red dots → current path
- 🔵 Blue dots → dead ends (backtracking points)

## Visualization (Turtle Graphics)
Two turtles are used:
- maze_turtle → draws the maze structure
- solver_turtle → animates solving process

The screen updates dynamically to show:
- Maze carving in real time
- Solver movement step-by-step

## How to Run
`bash
python maze.py
