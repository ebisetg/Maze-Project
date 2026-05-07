import random

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.start = maze.start_cell
        self.end = maze.end_cell
        
        self.current_cell = self.start
        self.stack = [self.start]
        self.visited = {self.start}
        self.dead_ends = set()
        self.path = [self.start]
        
        self.done = False
        self.success = False
        self.step_count = 0

    def step(self):
        if self.done:
            return

        self.step_count += 1
        r, c = self.current_cell
        
        if (r, c) == self.end:
            self.done = True
            self.success = True
            return

        neighbors = self.maze.get_neighbors(r, c)
        traversable = []
        
        for nr, nc, _ in neighbors:
            if not self.maze.has_wall(r, c, nr, nc) and (nr, nc) not in self.visited:
                traversable.append((nr, nc))

        if traversable:
            next_cell = random.choice(traversable)
            self.visited.add(next_cell)
            self.stack.append(self.current_cell)
            self.current_cell = next_cell
            self.path.append(next_cell)
        else:
            self.dead_ends.add(self.current_cell)
            if self.stack:
                self.current_cell = self.stack.pop()
                self.path.pop()
            else:
                self.done = True
                self.success = False
