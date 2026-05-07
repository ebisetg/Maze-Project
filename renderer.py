from OpenGL.GL import *
from config import *

class Renderer:
    def __init__(self, maze):
        self.maze = maze
        self.rows = maze.rows
        self.cols = maze.cols

    def draw_maze(self):
        """Draws all walls of the maze."""
        glColor3f(1.0, 1.0, 1.0)  # White walls
        glLineWidth(2.0)
        
        # Calculate cell size in OpenGL coordinates
        # Map: rows 1..ROWS to y from -0.8 to 0.8
        #      cols 1..COLS to x from -0.8 to 0.8
        cell_width = 1.6 / self.cols
        cell_height = 1.6 / self.rows
        start_x = -0.8
        start_y = -0.8
        
        glBegin(GL_LINES)
        
        # Draw horizontal lines (north walls)
        for row in range(self.rows + 1):
            y = start_y + row * cell_height
            for col in range(self.cols):
                x1 = start_x + col * cell_width
                x2 = x1 + cell_width
                
                # Check if this north wall exists
                if row < self.rows:
                    # For cells (row+1, col+1) - north wall
                    if self.maze.northWall[row][col + 1] == 1:
                        glVertex2f(x1, y)
                        glVertex2f(x2, y)
                else:
                    # Bottom boundary (phantom row)
                    if self.maze.northWall[row][col + 1] == 1:
                        glVertex2f(x1, y)
                        glVertex2f(x2, y)
        
        # Draw vertical lines (east walls)
        for col in range(self.cols + 1):
            x = start_x + col * cell_width
            for row in range(self.rows):
                y1 = start_y + row * cell_height
                y2 = y1 + cell_height
                
                # Check if this east wall exists
                if col < self.cols:
                    # For cells (row+1, col+1) - east wall
                    if self.maze.eastWall[row + 1][col] == 1:
                        glVertex2f(x, y1)
                        glVertex2f(x, y2)
                else:
                    # Right boundary
                    if self.maze.eastWall[row + 1][col] == 1:
                        glVertex2f(x, y1)
                        glVertex2f(x, y2)
        
        glEnd()

    def draw_dot(self, r, c, color, size=10.0):
        """Draws a dot at cell center."""
        # Calculate center of cell
        cell_width = 1.6 / self.cols
        cell_height = 1.6 / self.rows
        start_x = -0.8
        start_y = -0.8
        
        x = start_x + (c - 0.5) * cell_width
        y = start_y + (r - 0.5) * cell_height
        
        glColor3f(*color)
        glPointSize(size)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    def draw_state(self, generator=None, solver=None):
        """Draws the current state."""
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Draw the maze walls
        self.draw_maze()
        
        # Draw start and end if they exist
        if hasattr(self.maze, 'start_cell') and self.maze.start_cell:
            self.draw_dot(self.maze.start_cell[0], self.maze.start_cell[1], (0.0, 1.0, 0.0), 12)
        if hasattr(self.maze, 'end_cell') and self.maze.end_cell:
            self.draw_dot(self.maze.end_cell[0], self.maze.end_cell[1], (1.0, 0.5, 0.0), 12)
        
        # Draw generator mouse
        if generator and not generator.done:
            self.draw_dot(generator.current_cell[0], generator.current_cell[1], (1.0, 0.0, 0.0), 12)
        
        # Draw solver elements
        if solver:
            for de_r, de_c in solver.dead_ends:
                self.draw_dot(de_r, de_c, (0.0, 0.0, 1.0), 6)
            
            if not solver.done:
                self.draw_dot(solver.current_cell[0], solver.current_cell[1], (1.0, 0.0, 0.0), 12)
            
            # Draw path
            if len(solver.path) > 1:
                glLineWidth(3.0)
                glColor3f(0.0, 1.0, 0.0)
                glBegin(GL_LINE_STRIP)
                for pr, pc in solver.path:
                    cell_width = 1.6 / self.cols
                    cell_height = 1.6 / self.rows
                    start_x = -0.8
                    start_y = -0.8
                    x = start_x + (pc - 0.5) * cell_width
                    y = start_y + (pr - 0.5) * cell_height
                    glVertex2f(x, y)
                glEnd()