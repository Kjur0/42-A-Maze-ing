"""Centered '42' pattern definition and coordinate helpers for maze grids."""

Coords = tuple[int, int]

PATTERN_42 = [
    "X.X.XXX",
    "X.X...X",
    "XXX.XXX",
    "..X.X..",
    "..X.XXX",
]

PATTERN_WIDTH = len(PATTERN_42[0])
PATTERN_HEIGHT = len(PATTERN_42)


def pattern_cells(width: int, height: int) -> set[Coords]:
    """Returns centered grid coordinates belonging to the '42' pattern.

    Requires at least a 1-cell border around the pattern
    (``PATTERN_WIDTH + 2`` columns and ``PATTERN_HEIGHT + 2`` rows). Returns
    an empty set when the grid is too small to fit the pattern with padding.

    Args:
        width: Number of columns in the maze grid.
        height: Number of rows in the maze grid.

    Returns:
        A set of ``(x, y)`` coordinates for cells marked ``'X'``, or an empty
        set if the grid cannot fit the pattern.
    """
    if width < PATTERN_WIDTH + 2 or height < PATTERN_HEIGHT + 2:
        return set()

    left = width // 2 - PATTERN_WIDTH // 2
    top = height // 2 - PATTERN_HEIGHT // 2

    cells: set[Coords] = set()
    for row in range(PATTERN_HEIGHT):
        for col in range(PATTERN_WIDTH):
            if PATTERN_42[row][col] == "X":
                cells.add((left + col, top + row))

    return cells
