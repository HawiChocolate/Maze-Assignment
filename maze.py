import turtle
import random
import time

# =========================================================
# BUILDING AND RUNNING MAZES
# DFS Maze Generator + Backtracking Solver
# =========================================================

# -----------------------------
# MAZE SETTINGS
# -----------------------------
R = 15                     # Rows
C = 15                     # Columns
CELL_SIZE = 30

# -----------------------------
# WALL DATA STRUCTURES
# 1 = Wall exists
# 0 = Wall removed
# -----------------------------
northWall = [[1 for _ in range(C)] for _ in range(R)]
eastWall = [[1 for _ in range(C)] for _ in range(R)]

# Tracks visited cells
visited = [[False for _ in range(C)] for _ in range(R)]

# =========================================================
# TURTLE SCREEN SETUP
# =========================================================
screen = turtle.Screen()
screen.title("Maze Generator and Solver - Hawi Jarso")
screen.bgcolor("white")
screen.setup(width=900, height=900)

# Makes animation smoother
screen.tracer(0)

# Turtle for drawing maze
t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.pensize(2)

# Turtle for solver
dot = turtle.Turtle()
dot.hideturtle()
dot.penup()
dot.speed(0)

# =========================================================
# HELPER FUNCTION
# Convert row/column into screen coordinates
# =========================================================
def get_coords(r, c):

    offset_x = -(C * CELL_SIZE) / 2
    offset_y = -(R * CELL_SIZE) / 2

    x = offset_x + c * CELL_SIZE
    y = offset_y + r * CELL_SIZE

    return x, y

# =========================================================
# DRAW MAZE
# =========================================================
def draw_maze():

    t.clear()

    # -------------------------------------------------
    # DRAW INTERNAL WALLS
    # -------------------------------------------------
    for r in range(R):
        for c in range(C):

            x, y = get_coords(r, c)

            # NORTH WALL
            if northWall[r][c] == 1:

                t.penup()
                t.goto(x, y + CELL_SIZE)

                t.pendown()
                t.goto(x + CELL_SIZE, y + CELL_SIZE)

            # EAST WALL
            if eastWall[r][c] == 1:

                t.penup()
                t.goto(x + CELL_SIZE, y)

                t.pendown()
                t.goto(x + CELL_SIZE, y + CELL_SIZE)

    # -------------------------------------------------
    # LEFT OUTER BORDER
    # -------------------------------------------------
    for r in range(R):

        x, y = get_coords(r, 0)

        t.penup()
        t.goto(x, y)

        t.pendown()
        t.goto(x, y + CELL_SIZE)

    # -------------------------------------------------
    # BOTTOM OUTER BORDER
    # -------------------------------------------------
    for c in range(C):

        x, y = get_coords(0, c)

        t.penup()
        t.goto(x, y)

        t.pendown()
        t.goto(x + CELL_SIZE, y)

    # -------------------------------------------------
    # TOP OUTER BORDER
    # -------------------------------------------------
    top_y = get_coords(R - 1, 0)[1] + CELL_SIZE

    for c in range(C):

        x, _ = get_coords(R - 1, c)

        t.penup()
        t.goto(x, top_y)

        t.pendown()
        t.goto(x + CELL_SIZE, top_y)

    # -------------------------------------------------
    # RIGHT OUTER BORDER
    # -------------------------------------------------
    right_x = get_coords(0, C - 1)[0] + CELL_SIZE

    for r in range(R):

        _, y = get_coords(r, C - 1)

        t.penup()
        t.goto(right_x, y)

        t.pendown()
        t.goto(right_x, y + CELL_SIZE)

    screen.update()

# =========================================================
# GENERATE MAZE
# Uses DFS + Stack Backtracking
# =========================================================
def generate_maze(start_r, start_c):

    stack = [(start_r, start_c)]

    visited[start_r][start_c] = True

    while stack:

        r, c = stack[-1]

        neighbors = []

        # -------------------------------------------------
        # CHECK NEIGHBOR CELLS
        # -------------------------------------------------

        # UP
        if r + 1 < R and not visited[r + 1][c]:
            neighbors.append((r + 1, c, "N", r, c))

        # RIGHT
        if c + 1 < C and not visited[r][c + 1]:
            neighbors.append((r, c + 1, "E", r, c))

        # DOWN
        if r - 1 >= 0 and not visited[r - 1][c]:
            neighbors.append((r - 1, c, "N", r - 1, c))

        # LEFT
        if c - 1 >= 0 and not visited[r][c - 1]:
            neighbors.append((r, c - 1, "E", r, c - 1))

        # -------------------------------------------------
        # MOVE TO RANDOM NEIGHBOR
        # -------------------------------------------------
        if neighbors:

            nr, nc, wall_type, wr, wc = random.choice(neighbors)

            # Remove wall
            if wall_type == "N":
                northWall[wr][wc] = 0
            else:
                eastWall[wr][wc] = 0

            visited[nr][nc] = True

            stack.append((nr, nc))

            # Animate generation
            if random.random() < 0.25:
                draw_maze()

        # -------------------------------------------------
        # DEAD END -> BACKTRACK
        # -------------------------------------------------
        else:
            stack.pop()

    # =====================================================
    # BONUS SECTION
    # Add extra openings to create cycles
    # =====================================================
    for _ in range(3):

        r = random.randint(1, R - 2)
        c = random.randint(1, C - 2)

        if random.choice([True, False]):
            northWall[r][c] = 0
        else:
            eastWall[r][c] = 0

    draw_maze()

# =========================================================
# SOLVE MAZE
# Uses Backtracking Algorithm
# =========================================================
def solve_maze(start_r, start_c, end_r, end_c):

    stack = [(start_r, start_c)]

    solve_visited = [[False for _ in range(C)] for _ in range(R)]

    solve_visited[start_r][start_c] = True

    while stack:

        r, c = stack[-1]

        x, y = get_coords(r, c)

        # -------------------------------------------------
        # DRAW CURRENT POSITION (RED)
        # -------------------------------------------------
        dot.goto(x + CELL_SIZE / 2, y + CELL_SIZE / 2)
        dot.dot(10, "red")

        # -------------------------------------------------
        # TARGET REACHED
        # -------------------------------------------------
        if (r, c) == (end_r, end_c):

            print("Target Reached!")
            break

        valid_moves = []

        # -------------------------------------------------
        # CHECK VALID MOVES
        # -------------------------------------------------

        # UP
        if (
            r + 1 < R
            and not solve_visited[r + 1][c]
            and northWall[r][c] == 0
        ):
            valid_moves.append((r + 1, c))

        # RIGHT
        if (
            c + 1 < C
            and not solve_visited[r][c + 1]
            and eastWall[r][c] == 0
        ):
            valid_moves.append((r, c + 1))

        # DOWN
        if (
            r - 1 >= 0
            and not solve_visited[r - 1][c]
            and northWall[r - 1][c] == 0
        ):
            valid_moves.append((r - 1, c))

        # LEFT
        if (
            c - 1 >= 0
            and not solve_visited[r][c - 1]
            and eastWall[r][c - 1] == 0
        ):
            valid_moves.append((r, c - 1))

        # -------------------------------------------------
        # MOVE FORWARD
        # -------------------------------------------------
        if valid_moves:

            next_r, next_c = random.choice(valid_moves)

            solve_visited[next_r][next_c] = True

            stack.append((next_r, next_c))

        # -------------------------------------------------
        # DEAD END -> BACKTRACK
        # -------------------------------------------------
        else:

            # Blue dots show dead ends
            dot.dot(10, "blue")

            stack.pop()

        screen.update()

        time.sleep(0.04)

# =========================================================
# MAIN EXECUTION
# =========================================================

# Generate the maze
generate_maze(0, 0)

# Solve the maze
solve_maze(0, 0, R - 1, C - 1)

# Keep window open
turtle.done()