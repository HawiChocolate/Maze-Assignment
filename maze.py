import turtle
import random
import time

                                          # BUILDING AND RUNNING MAZES
                                    # DFS Maze Generator + Backtracking Solver

                                    
                                               # MAZE SETTINGS
ROWS = 15
COLS = 15
CELL_SIZE = 30

# ---------------------------------------------------------
# WALL DATA STRUCTURES
# 1 = Wall exists
# 0 = Wall removed
# ---------------------------------------------------------
northWall = [[1 for _ in range(COLS)] for _ in range(ROWS)]
eastWall = [[1 for _ in range(COLS)] for _ in range(ROWS)]

# Track visited cells during maze generation
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]


                                         # START AND END POSITIONS
START_ROW = 0
START_COL = 0

END_ROW = ROWS - 1
END_COL = COLS - 1


                                             # TURTLE SCREEN SETUP
screen = turtle.Screen()
screen.title("Maze Generator and Solver - Hawi Jarso")
screen.bgcolor("white")
screen.setup(width=900, height=900)

# Smooth animation
screen.tracer(0)

# Turtle for maze drawing
maze_turtle = turtle.Turtle()
maze_turtle.hideturtle()
maze_turtle.speed(0)
maze_turtle.pensize(2)

# Turtle for solving animation
solver_turtle = turtle.Turtle()
solver_turtle.hideturtle()
solver_turtle.penup()
solver_turtle.speed(0)


                                                   # HELPER FUNCTION
# Convert row/column to screen coordinates
def get_coords(row, col):

    offset_x = -(COLS * CELL_SIZE) / 2
    offset_y = -(ROWS * CELL_SIZE) / 2

    x = offset_x + col * CELL_SIZE
    y = offset_y + row * CELL_SIZE

    return x, y


def draw_maze():

    maze_turtle.clear()

    
                                                    # DRAW INTERNAL WALLS
    for row in range(ROWS):
        for col in range(COLS):

            x, y = get_coords(row, col)

            # NORTH WALL
            if northWall[row][col] == 1:

                maze_turtle.penup()
                maze_turtle.goto(x, y + CELL_SIZE)

                maze_turtle.pendown()
                maze_turtle.goto(x + CELL_SIZE, y + CELL_SIZE)

            # EAST WALL
            if eastWall[row][col] == 1:

                maze_turtle.penup()
                maze_turtle.goto(x + CELL_SIZE, y)

                maze_turtle.pendown()
                maze_turtle.goto(x + CELL_SIZE, y + CELL_SIZE)

   
                                                    # LEFT OUTER BORDER
    # Create entrance opening
    for row in range(ROWS):

        # Skip wall for entrance
        if row == START_ROW:
            continue

        x, y = get_coords(row, 0)

        maze_turtle.penup()
        maze_turtle.goto(x, y)

        maze_turtle.pendown()
        maze_turtle.goto(x, y + CELL_SIZE)

                                            # Bottom Outer Border
    for col in range(COLS):

        x, y = get_coords(0, col)

        maze_turtle.penup()
        maze_turtle.goto(x, y)

        maze_turtle.pendown()
        maze_turtle.goto(x + CELL_SIZE, y)

    
                                                # TOP OUTER BORDER
    top_y = get_coords(ROWS - 1, 0)[1] + CELL_SIZE

    for col in range(COLS):
        if col == COLS -1:
            continue

        x, _ = get_coords(ROWS - 1, col)

        maze_turtle.penup()
        maze_turtle.goto(x, top_y)

        maze_turtle.pendown()
        maze_turtle.goto(x + CELL_SIZE, top_y)


    # RIGHT OUTER BORDER
    # Create exit opening
    # -----------------------------------------------------
    right_x = get_coords(0, COLS - 1)[0] + CELL_SIZE

    for row in range(ROWS):

        # Skip wall for exit
        if row == END_ROW:
            continue

        _, y = get_coords(row, COLS - 1)

        maze_turtle.penup()
        maze_turtle.goto(right_x, y)

        maze_turtle.pendown()
        maze_turtle.goto(right_x, y + CELL_SIZE)

    screen.update()


# GENERATE MAZE
# DFS + Stack Backtracking
def generate_maze(start_row, start_col):

    stack = [(start_row, start_col)]

    visited[start_row][start_col] = True

    while stack:

        current_row, current_col = stack[-1]

        neighbors = []

       
                                             # CHECK UNVISITED NEIGHBORS
        # UP
        if (
            current_row + 1 < ROWS
            and not visited[current_row + 1][current_col]
        ):
            neighbors.append(
                (current_row + 1, current_col,
                 "N", current_row, current_col)
            )

        # RIGHT
        if (
            current_col + 1 < COLS
            and not visited[current_row][current_col + 1]
        ):
            neighbors.append(
                (current_row, current_col + 1,
                 "E", current_row, current_col)
            )

        # DOWN
        if (
            current_row - 1 >= 0
            and not visited[current_row - 1][current_col]
        ):
            neighbors.append(
                (current_row - 1, current_col,
                 "N", current_row - 1, current_col)
            )

        # LEFT
        if (
            current_col - 1 >= 0
            and not visited[current_row][current_col - 1]
        ):
            neighbors.append(
                (current_row, current_col - 1,
                 "E", current_row, current_col - 1)
            )

        
                                         # MOVE TO RANDOM NEIGHBOR
        if neighbors:

            next_row, next_col, wall_type, wall_row, wall_col = (
                random.choice(neighbors)
            )

            # Remove wall
            if wall_type == "N":
                northWall[wall_row][wall_col] = 0
            else:
                eastWall[wall_row][wall_col] = 0

            visited[next_row][next_col] = True

            stack.append((next_row, next_col))

            # Animate generation
            if random.random() < 0.25:
                draw_maze()

        else:             # DEAD END -> BACKTRACK
            stack.pop()

    
    # BONUS SECTION
    # Remove extra walls to create cycles
    for _ in range(3):

        random_row = random.randint(1, ROWS - 2)
        random_col = random.randint(1, COLS - 2)

        if random.choice([True, False]):
            northWall[random_row][random_col] = 0
        else:
            eastWall[random_row][random_col] = 0

    draw_maze()


# SOLVE MAZE
# Backtracking Algorithm
def solve_maze(start_row, start_col, end_row, end_col):

    stack = [(start_row, start_col)]

    solve_visited = [
        [False for _ in range(COLS)]
        for _ in range(ROWS)
    ]

    solve_visited[start_row][start_col] = True

    while stack:

        current_row, current_col = stack[-1]

        x, y = get_coords(current_row, current_col)

                                              # Draw Current Position
        solver_turtle.goto(
            x + CELL_SIZE / 2,
            y + CELL_SIZE / 2
        )

        solver_turtle.dot(10, "red")

    
        # TARGET REACHED
        if (current_row, current_col) == (end_row, end_col):

            print("Maze Solved!")
            break

        valid_moves = []

                                         # CHECK VALID MOVES

        # UP
        if (
            current_row + 1 < ROWS
            and not solve_visited[current_row + 1][current_col]
            and northWall[current_row][current_col] == 0
        ):
            valid_moves.append((current_row + 1, current_col))

        # RIGHT
        if (
            current_col + 1 < COLS
            and not solve_visited[current_row][current_col + 1]
            and eastWall[current_row][current_col] == 0
        ):
            valid_moves.append((current_row, current_col + 1))

        # DOWN
        if (
            current_row - 1 >= 0
            and not solve_visited[current_row - 1][current_col]
            and northWall[current_row - 1][current_col] == 0
        ):
            valid_moves.append((current_row - 1, current_col))

        # LEFT
        if (
            current_col - 1 >= 0
            and not solve_visited[current_row][current_col - 1]
            and eastWall[current_row][current_col - 1] == 0
        ):
            valid_moves.append((current_row, current_col - 1))

                                                # Move Forward
        if valid_moves:

            next_row, next_col = random.choice(valid_moves)

            solve_visited[next_row][next_col] = True

            stack.append((next_row, next_col))

        
        # DEAD END -> BACKTRACK
        else:

            # BLUE DOT = dead end
            solver_turtle.dot(10, "blue")

            stack.pop()

        screen.update()

        time.sleep(0.04)

 
                                                # MAIN PROGRAM


# Generate the maze
generate_maze(START_ROW, START_COL)

# Solve the maze
solve_maze(
    START_ROW,
    START_COL,
    END_ROW,
    END_COL
)

# Keep window open
turtle.done()