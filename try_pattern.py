import sys

from mazegen.pattern import pattern_cells

width = int(sys.argv[1])
height = int(sys.argv[2])

cells = pattern_cells(width, height)
if not cells:
    print("Maze too small for the 42 pattern")

for y in range(height):
    line = ""
    for x in range(width):
        if (x, y) in cells:
            line += "##"
        else:
            line += ". "
    print(line)
