import sys

from app.config import ConfigError, load_config
from app.writer import write_maze
from mazegen.solver import shortest_path

TEST_GRID = [
    [9, 5, 5, 3],
    [10, 9, 7, 10],
    [12, 6, 13, 6],
]
TEST_ENTRY = (0, 0)
TEST_EXIT = (3, 2)

if len(sys.argv) != 2:
    print("Usage: python3 a_maze_ing.py config.txt")
    sys.exit(1)

try:
    settings = load_config(sys.argv[1])
    path = shortest_path(TEST_GRID, TEST_ENTRY, TEST_EXIT)
    print("Path:", path)
    write_maze(settings["output_file"], TEST_GRID, TEST_ENTRY, TEST_EXIT, path)
    print(f"Maze saved to {settings['output_file']}")
except ConfigError as e:
    print("Error:", e)
    sys.exit(1)
except OSError as e:
    print("Error: cannot write output file:", e)
    sys.exit(1)
