import random

from mazegen.pattern import pattern_cells

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

DIRECTIONS = [
    (NORTH, 0, -1, SOUTH),
    (EAST, 1, 0, WEST),
    (SOUTH, 0, 1, NORTH),
    (WEST, -1, 0, EAST),
]


class MazeError(Exception):
    pass


class MazeGenerator:
    def __init__(self, width, height, entry, exit, perfect=True, seed=None):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.grid = []
        self.pattern = set()

    def generate(self):
        rng = random.Random(self.seed)

        self.grid = []
        for y in range(self.height):
            self.grid.append([15] * self.width)

        self.pattern = pattern_cells(self.width, self.height)
        if self.entry in self.pattern or self.exit in self.pattern:
            raise MazeError("ENTRY or EXIT is inside the 42 pattern")

        visited = set(self.pattern)
        visited.add(self.entry)
        stack = [self.entry]

        while stack:
            x, y = stack[-1]

            options = []
            for wall, dx, dy, opposite in DIRECTIONS:
                nx = x + dx
                ny = y + dy
                inside = 0 <= nx < self.width and 0 <= ny < self.height
                if inside and (nx, ny) not in visited:
                    options.append((nx, ny, wall, opposite))

            if not options:
                stack.pop()
                continue

            nx, ny, wall, opposite = rng.choice(options)
            self.grid[y][x] -= wall
            self.grid[ny][nx] -= opposite
            visited.add((nx, ny))
            stack.append((nx, ny))

        return self.grid
