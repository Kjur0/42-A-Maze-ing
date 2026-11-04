from collections import deque

DIRECTIONS = [
    (1, 0, -1, "N"),
    (2, 1, 0, "E"),
    (4, 0, 1, "S"),
    (8, -1, 0, "W"),
]


def shortest_path(grid, entry, exit):
    queue = deque([entry])
    seen = {entry}
    came_from: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

    while queue:
        x, y = queue.popleft()

        if (x, y) == exit:
            break

        for wall, dx, dy, letter in DIRECTIONS:
            if grid[y][x] & wall:
                continue

            next_cell = (x + dx, y + dy)
            if next_cell in came_from:
                continue

            seen.add(next_cell)
            came_from[next_cell] = ((x, y), letter)
            queue.append(next_cell)

    if exit not in seen:
        return ""

    path = ""
    cell = exit
    while cell != entry:
        previous, letter = came_from[cell]
        path = letter + path
        cell = previous

    return path
