import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import random

from config import *
from maze import Maze
from generator import MazeGenerator
from solver import MazeSolver

class Renderer:
    def __init__(self, maze):
        self.maze = maze
        self.rows = maze.rows
        self.cols = maze.cols

    def draw_maze(self):
        """Draws all walls of the maze."""
        cell_width = 1.6 / self.cols
        cell_height = 1.6 / self.rows
        start_x = -0.8
        start_y = -0.8
        
        glLineWidth(2.0)
        glBegin(GL_LINES)
        
        # Draw normal walls (white)
        glColor3f(1.0, 1.0, 1.0)
        
        # North walls (horizontal)
        for row in range(self.rows + 1):
            y = start_y + row * cell_height
            for col in range(self.cols):
                x1 = start_x + col * cell_width
                x2 = x1 + cell_width
                if self.maze.northWall[row][col + 1] == 1:
                    glVertex2f(x1, y)
                    glVertex2f(x2, y)
        
        # East walls (vertical)
        for col in range(self.cols + 1):
            x = start_x + col * cell_width
            for row in range(self.rows):
                y1 = start_y + row * cell_height
                y2 = y1 + cell_height
                if self.maze.eastWall[row + 1][col] == 1:
                    glVertex2f(x, y1)
                    glVertex2f(x, y2)
        
        glEnd()
        
        # Draw CYCLE walls (purple) - overlay on top
        glColor3f(0.8, 0.0, 0.8)  # Purple
        glLineWidth(3.0)  # Slightly thicker to stand out
        glBegin(GL_LINES)
        
        for wall in self.maze.cycle_walls:
            r1, c1, r2, c2 = wall
            # Calculate line coordinates for this wall
            if r1 == r2:  # Horizontal wall (north/south)
                if c2 > c1:  # East wall
                    x = start_x + c1 * cell_width
                    y1 = start_y + (r1 - 1) * cell_height
                    y2 = start_y + r1 * cell_height
                    glVertex2f(x, y1)
                    glVertex2f(x, y2)
                else:  # West wall
                    x = start_x + c2 * cell_width
                    y1 = start_y + (r1 - 1) * cell_height
                    y2 = start_y + r1 * cell_height
                    glVertex2f(x, y1)
                    glVertex2f(x, y2)
            elif c1 == c2:  # Vertical wall (east/west)
                if r2 > r1:  # North wall
                    y = start_y + r1 * cell_height
                    x1 = start_x + (c1 - 1) * cell_width
                    x2 = start_x + c1 * cell_width
                    glVertex2f(x1, y)
                    glVertex2f(x2, y)
                else:  # South wall
                    y = start_y + r2 * cell_height
                    x1 = start_x + (c1 - 1) * cell_width
                    x2 = start_x + c1 * cell_width
                    glVertex2f(x1, y)
                    glVertex2f(x2, y)
        
        glEnd()
        glLineWidth(2.0)  # Reset

    def draw_dot(self, r, c, color, size=10.0):
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
        glClear(GL_COLOR_BUFFER_BIT)
        self.draw_maze()
        
        # Generator mouse (red)
        if generator and not generator.done:
            self.draw_dot(generator.current_cell[0], generator.current_cell[1], (1.0, 0.0, 0.0), 14)
        
        # Solver elements
        if solver:
            if self.maze.start_cell:
                self.draw_dot(self.maze.start_cell[0], self.maze.start_cell[1], (0.0, 1.0, 0.0), 12)
            if self.maze.end_cell:
                self.draw_dot(self.maze.end_cell[0], self.maze.end_cell[1], (1.0, 0.5, 0.0), 12)
            
            for de_r, de_c in solver.dead_ends:
                self.draw_dot(de_r, de_c, (0.0, 0.0, 1.0), 8)
            
            if not solver.done:
                self.draw_dot(solver.current_cell[0], solver.current_cell[1], (1.0, 0.0, 0.0), 14)
            
            for pr, pc in solver.path:
                self.draw_dot(pr, pc, (1.0, 0.0, 0.0), 5)

def main():
    pygame.init()
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Maze - G:Normal W:Cycles R:Reset SPACE:Solve")
    
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    maze = Maze(ROWS, COLS)
    renderer = Renderer(maze)
    generator = None
    solver = None
    
    state = "IDLE"
    clock = pygame.time.Clock()
    running = True
    last_step = time.time()
    
    print("=" * 60)
    print("MAZE GENERATOR & SOLVER")
    print("=" * 60)
    print("G - Generate NORMAL maze (all white walls)")
    print("W - Generate maze with CYCLES (PURPLE walls show extra walls)")
    print("R - Reset to empty grid")
    print("SPACE - Solve the maze (red dots path, blue dead ends)")
    print("ESC - Quit")
    print("=" * 60)
    print("\nPress G or W to start!\n")
    
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_g:
                    maze = Maze(ROWS, COLS)
                    generator = MazeGenerator(maze)
                    generator.create_cycles = False
                    renderer = Renderer(maze)
                    solver = None
                    state = "GENERATING"
                    print("\nGenerating NORMAL maze (all white walls)...")
                
                if event.key == pygame.K_w:
                    maze = Maze(ROWS, COLS)
                    generator = MazeGenerator(maze)
                    generator.create_cycles = True
                    renderer = Renderer(maze)
                    solver = None
                    state = "GENERATING"
                    print("\nGenerating maze with CYCLES (PURPLE walls = extra walls)...")
                
                if event.key == pygame.K_r:
                    maze = Maze(ROWS, COLS)
                    generator = None
                    solver = None
                    renderer = Renderer(maze)
                    state = "IDLE"
                    print("\nReset to empty grid. Press G or W to generate.")
                
                if event.key == pygame.K_SPACE and state == "READY":
                    start_row = random.randint(1, ROWS)
                    end_row = random.randint(1, ROWS)
                    maze.start_cell = (start_row, 1)
                    maze.end_cell = (end_row, COLS)
                    maze.create_openings()
                    solver = MazeSolver(maze)
                    state = "SOLVING"
                    print(f"\nSolving from {maze.start_cell} to {maze.end_cell}")
        
        if state == "GENERATING" and generator:
            if current_time - last_step > GEN_SPEED / 1000.0:
                generator.step()
                last_step = current_time
                if generator.done:
                    state = "READY"
                    print("\nMAZE COMPLETE!")
                    if generator.create_cycles and maze.cycle_walls:
                        print(f"  Created {len(maze.cycle_walls)} cycle walls (PURPLE)")
                        print("  These extra walls create LOOPS in the maze!")
                    print("\nPress SPACE to solve, R to reset")
        
        elif state == "SOLVING" and solver:
            if current_time - last_step > SOLVE_SPEED / 1000.0:
                solver.step()
                last_step = current_time
                if solver.done:
                    state = "FINISHED"
                    if solver.success:
                        print(f"\nSOLVED! Path: {len(solver.path)} | Dead ends: {len(solver.dead_ends)}")
                    else:
                        print("\nNo path found!")
        
        renderer.draw_state(generator if state == "GENERATING" else None, solver)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()