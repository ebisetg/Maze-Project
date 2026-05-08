import numpy as np
from config import ROWS, COLS

class Maze:
   
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        
        # Initialize all walls intact (1 = wall exists)
        self.northWall = np.ones((rows + 1, cols + 1), dtype=int)
        self.eastWall = np.ones((rows + 1, cols + 1), dtype=int)
        
        # Start and End cells 
        self.start_cell = None
        self.end_cell = None
        
        # Track cycle walls (purple) - stores (r1, c1, r2, c2) for walls that create cycles
        self.cycle_walls = set()

    def is_valid(self, r, c):
        return 1 <= r <= self.rows and 1 <= c <= self.cols

    def get_neighbors(self, r, c):
        neighbors = []
        if self.is_valid(r + 1, c): neighbors.append((r + 1, c, 'N'))
        if self.is_valid(r - 1, c): neighbors.append((r - 1, c, 'S'))
        if self.is_valid(r, c + 1): neighbors.append((r, c + 1, 'E'))
        if self.is_valid(r, c - 1): neighbors.append((r, c - 1, 'W'))
        return neighbors

    def remove_wall(self, r1, c1, r2, c2):
        if r1 == r2:
            if c2 > c1:
                self.eastWall[r1][c1] = 0
            else:
                self.eastWall[r1][c2] = 0
        elif c1 == c2:
            if r2 > r1:
                self.northWall[r1][c1] = 0
            else:
                self.northWall[r2][c1] = 0

    def has_wall(self, r1, c1, r2, c2):
        if r1 == r2:
            if c2 > c1:
                return self.eastWall[r1][c1] == 1
            else:
                return self.eastWall[r1][c2] == 1
        elif c1 == c2:
            if r2 > r1:
                return self.northWall[r1][c1] == 1
            else:
                return self.northWall[r2][c1] == 1
        return True

    def all_walls_intact(self, r, c):
        if self.northWall[r][c] == 0: return False
        if self.northWall[r-1][c] == 0: return False
        if self.eastWall[r][c] == 0: return False
        if self.eastWall[r][c-1] == 0: return False
        return True
    
    def create_openings(self):
        
        if self.start_cell:
            r, c = self.start_cell
            if c == 1:
                self.eastWall[r][0] = 0
        if self.end_cell:
            r, c = self.end_cell
            if c == self.cols:
                self.eastWall[r][self.cols] = 0
