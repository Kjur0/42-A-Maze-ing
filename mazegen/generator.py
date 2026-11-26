import random
from typing import Optional

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
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.grid: list[list[int]] = []
        self.pattern: set[tuple[int, int]] = set()

    def generate(self) -> list[list[int]]:
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

        if not self.perfect:
            self.add_loops(rng)
        return self.grid

    def is_open_block(self, left: int, top: int) -> bool:
        if left < 0 or top < 0:
            return False
        if left + 3 > self.width or top + 3 > self.height:
            return False
        for y in range(top, top + 3):
            for x in range(left, left + 3):
                if x < left + 2 and self.grid[y][x] & EAST:
                    return False
                if y < top + 2 and self.grid[y][x] & SOUTH:
                    return False
        return True

    def has_open_area(self, x: int, y: int) -> bool:
        for top in range(y - 2, y + 1):
            for left in range(x - 2, x + 1):
                if self.is_open_block(left, top):
                    return True
        return False

    def add_loops(self, rng: random.Random) -> None:
        walls: list[tuple[int, int, int, int, int, int]] = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pattern:
                    continue
                if x + 1 < self.width and (x + 1, y) not in self.pattern:
                    if self.grid[y][x] & EAST:
                        walls.append((x, y, x + 1, y, EAST, WEST))
                if y + 1 < self.height and (x, y + 1) not in self.pattern:
                    if self.grid[y][x] & SOUTH:
                        walls.append((x, y, x, y + 1, SOUTH, NORTH))

        rng.shuffle(walls)
        cells = self.width * self.height - len(self.pattern)
        to_remove = max(2, cells // 10)

        removed = 0
        for x, y, nx, ny, wall, opposite in walls:
            if removed == to_remove:
                break
            self.grid[y][x] -= wall
            self.grid[ny][nx] -= opposite
            if self.has_open_area(x, y) or self.has_open_area(nx, ny):
                self.grid[y][x] += wall
                self.grid[ny][nx] += opposite
            else:
                removed += 1
