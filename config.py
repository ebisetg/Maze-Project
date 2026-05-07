# Configuration for the Maze Project

# Grid dimensions (R rows, C columns)
ROWS = 20
COLS = 30

# Visual settings
CELL_SIZE = 30
WINDOW_WIDTH = COLS * CELL_SIZE + 100
WINDOW_HEIGHT = ROWS * CELL_SIZE + 100

# Animation speed
GEN_SPEED = 5
SOLVE_SPEED = 30

# Colors
COLOR_BG = (0.1, 0.1, 0.1)
COLOR_WALL = (1.0, 1.0, 1.0)
COLOR_MOUSE = (1.0, 0.0, 0.0)
COLOR_DEAD_END = (0.0, 0.0, 1.0)
COLOR_PATH = (1.0, 0.0, 0.0)  # Red path (not green)
COLOR_CYCLE = (1.0, 1.0, 0.0)  # Yellow for cycles
COLOR_START_EMPTY = (0.3, 0.3, 0.3)  # Dark grey for openings

# BONUS: Cycle probability when W is pressed
CYCLE_PROBABILITY = 0.05
