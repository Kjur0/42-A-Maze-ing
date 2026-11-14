PATTERN_42 = [
    "X.X.XXX",
    "X.X...X",
    "XXX.XXX",
    "..X.X..",
    "..X.XXX",
]

PATTERN_WIDTH = len(PATTERN_42[0])
PATTERN_HEIGHT = len(PATTERN_42)


def pattern_cells(width, height):
    if width < PATTERN_WIDTH + 2 or height < PATTERN_HEIGHT + 2:
        return set()

    left = width // 2 - PATTERN_WIDTH // 2
    top = height // 2 - PATTERN_HEIGHT // 2

    cells = set()
    for row in range(PATTERN_HEIGHT):
        for col in range(PATTERN_WIDTH):
            if PATTERN_42[row][col] == "X":
                cells.add((left + col, top + row))

    return cells
