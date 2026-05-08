import turtle
import random
import time

# --- 1. DATA STRUCTURE SETUP ---
R, C = 15, 15
CELL_SIZE = 30
# 1 = wall exists, 0 = wall is eaten
northWall = [[1 for _ in range(C)] for _ in range(R)]
eastWall = [[1 for _ in range(C)] for _ in range(R)]
visited = [[False for _ in range(C)] for _ in range(R)]

screen = turtle.Screen()
screen.title("Maze Assignment - Hawi Jarso")
screen.tracer(0) 
t = turtle.Turtle()
t.hideturtle()

def get_coords(r, c):
    off_x, off_y = -(C * CELL_SIZE)/2, -(R * CELL_SIZE)/2
    return off_x + c * CELL_SIZE, off_y + r * CELL_SIZE

def draw_maze():
    t.clear()
    for r in range(R):
        for c in range(C):
            x, y = get_coords(r, c)
            if northWall[r][c]:
                t.penup(); t.goto(x, y + CELL_SIZE); t.pendown(); t.goto(x + CELL_SIZE, y + CELL_SIZE)
            if eastWall[r][c]:
                t.penup(); t.goto(x + CELL_SIZE, y); t.pendown(); t.goto(x + CELL_SIZE, y + CELL_SIZE)
    screen.update()

# --- 2. THE "EATING MOUSE" (Generation) ---
def generate_maze(start_r, start_c):
    stack = [(start_r, start_c)]
    visited[start_r][start_c] = True
    while stack:
        r, c = stack[-1]
        neighbors = []
        if r + 1 < R and not visited[r+1][c]: neighbors.append((r+1, c, 'N', r, c))
        if c + 1 < C and not visited[r][c+1]: neighbors.append((r, c+1, 'E', r, c))
        if r - 1 >= 0 and not visited[r-1][c]: neighbors.append((r-1, c, 'N', r-1, c))
        if c - 1 >= 0 and not visited[r][c-1]: neighbors.append((r, c-1, 'E', r, c-1))

        if neighbors:
            nr, nc, w_type, wr, wc = random.choice(neighbors)
            if w_type == 'N': northWall[wr][wc] = 0
            else: eastWall[wr][wc] = 0
            visited[nr][nc] = True
            stack.append((nr, nc))
            if random.random() < 0.2: draw_maze()
        else:
            stack.pop()
    
    # --- BONUS: THE CHALLENGE ---
    # Randomly eat one extra wall to create a cycle (breaks "shoulder-to-the-wall" rule)
    northWall[random.randint(1, R-2)][random.randint(1, C-2)] = 0
    draw_maze()

# --- 3. THE SOLVER (Red/Blue Dots) ---
def solve_maze(start_r, start_c, end_r, end_c):
    stack = [(start_r, start_c)]
    solve_visited = [[False for _ in range(C)] for _ in range(R)]
    solve_visited[start_r][start_c] = True
    
    dot = turtle.Turtle()
    dot.shape("circle")
    dot.penup()
    dot.speed(0)

    while stack:
        r, c = stack[-1]
        x, y = get_coords(r, c)
        dot.goto(x + CELL_SIZE/2, y + CELL_SIZE/2)
        dot.dot(10, "red") # RED DOT for current path
        
        if (r, c) == (end_r, end_c):
            print("Target Reached!")
            break

        valid_moves = []
        # Up
        if r + 1 < R and not solve_visited[r+1][c] and northWall[r][c] == 0: valid_moves.append((r+1, c))
        # Right
        if c + 1 < C and not solve_visited[r][c+1] and eastWall[r][c] == 0: valid_moves.append((r, c+1))
        # Down
        if r - 1 >= 0 and not solve_visited[r-1][c] and northWall[r-1][c] == 0: valid_moves.append((r-1, c))
        # Left
        if c - 1 >= 0 and not solve_visited[r][c-1] and eastWall[r][c-1] == 0: valid_moves.append((r, c-1))

        if valid_moves:
            next_r, next_c = random.choice(valid_moves)
            solve_visited[next_r][next_c] = True
            stack.append((next_r, next_c))
        else:
            dot.dot(10, "blue") # BLUE DOT for backtracking
            stack.pop()
        
        screen.update()
        time.sleep(0.05)

# --- EXECUTION ---
generate_maze(0, 0)
solve_maze(0, 0, R-1, C-1) # Start to End
turtle.done()