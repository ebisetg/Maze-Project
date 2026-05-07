import random
from config import CYCLE_PROBABILITY

class MazeGenerator:
    def __init__(self, maze):
        self.maze = maze
        self.stack = []
        self.visited = set()
        self.current_cell = (1, 1)
        self.visited.add((1, 1))
        self.done = False
        self.create_cycles = False

    def step(self):
        if self.done:
            return

        r, c = self.current_cell
        neighbors = self.maze.get_neighbors(r, c)
        candidates = [n for n in neighbors if self.maze.all_walls_intact(n[0], n[1])]
        
        if candidates:
            chosen_r, chosen_c, direction = random.choice(candidates)
            
            for mr, mc, mdir in candidates:
                if (mr, mc) != (chosen_r, chosen_c):
                    self.stack.append((r, c))

            # Eat the wall to connect to chosen cell
            self.maze.remove_wall(r, c, chosen_r, chosen_c)
            self.current_cell = (chosen_r, chosen_c)
            self.visited.add(self.current_cell)
            
            # BONUS: Create cycle by eating an EXTRA wall (only when W was pressed)
            if self.create_cycles and random.random() < CYCLE_PROBABILITY:
                extra = random.choice(neighbors)
                # Mark this wall as a cycle wall BEFORE removing it
                self.maze.cycle_walls.add((r, c, extra[0], extra[1]))
                # Remove the extra wall to create a loop
                self.maze.remove_wall(r, c, extra[0], extra[1])

        else:
            if self.stack:
                found_new_path = False
                while self.stack and not found_new_path:
                    self.current_cell = self.stack.pop()
                    cr, cc = self.current_cell
                    cands = [n for n in self.maze.get_neighbors(cr, cc) 
                             if self.maze.all_walls_intact(n[0], n[1])]
                    if cands:
                        found_new_path = True
            else:
                self.done = True
                self.maze.create_openings()
