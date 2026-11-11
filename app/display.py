RESET = "\033[0m"
CLEAR_SCREEN = "\033[2J\033[H"

EMPTY = "  "
ENTRY = "\033[42m  " + RESET
EXIT = "\033[41m  " + RESET
PATH = "\033[43m  " + RESET
PATTERN = "\033[45m  " + RESET

WALL_COLORS = [
    "\033[47m",
    "\033[44m",
    "\033[46m",
    "\033[100m",
]

MOVES = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}


def draw_maze(grid, entry, exit, path, wall_color):
    wall = wall_color + "  " + RESET
    height = len(grid)
    width = len(grid[0])

    canvas = []
    for row in range(2 * height + 1):
        canvas.append([wall] * (2 * width + 1))

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]

            if cell == 15:
                canvas[2 * y + 1][2 * x + 1] = PATTERN
            else:
                canvas[2 * y + 1][2 * x + 1] = EMPTY

            if not cell & 2:
                canvas[2 * y + 1][2 * x + 2] = EMPTY

            if not cell & 4:
                canvas[2 * y + 2][2 * x + 1] = EMPTY

    x, y = entry
    for letter in path:
        dx, dy = MOVES[letter]
        canvas[2 * y + 1 + dy][2 * x + 1 + dx] = PATH
        x = x + dx
        y = y + dy
        canvas[2 * y + 1][2 * x + 1] = PATH

    entry_x, entry_y = entry
    canvas[2 * entry_y + 1][2 * entry_x + 1] = ENTRY

    exit_x, exit_y = exit
    canvas[2 * exit_y + 1][2 * exit_x + 1] = EXIT

    print(CLEAR_SCREEN, end="")
    for line in canvas:
        print("".join(line))


def print_menu():
    print()
    print("=== A-Maze-ing ===")
    print("1. Generate a new maze")
    print("2. Show/Hide shortest path")
    print("3. Change wall colour")
    print("4. Quit")
