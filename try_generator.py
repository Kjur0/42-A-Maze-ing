import sys

from app.display import WALL_COLORS, draw_maze
from mazegen.generator import MazeGenerator
from mazegen.solver import shortest_path

width = int(sys.argv[1])
height = int(sys.argv[2])
seed = int(sys.argv[3])

entry = (0, 0)
exit = (width - 1, height - 1)

generator = MazeGenerator(width, height, entry, exit, seed=seed)
grid = generator.generate()
path = shortest_path(grid, entry, exit)

draw_maze(grid, entry, exit, path, WALL_COLORS[0])
if not generator.pattern:
    print("Maze too small for the 42 pattern")
print("Path:", path)
