def write_maze(filename, grid, entry, exit, path):
    lines = []

    for row in grid:
        line = ""
        for cell in row:
            line += format(cell, "X")
        lines.append(line)

    lines.append("")
    lines.append(f"{entry[0]},{entry[1]}")
    lines.append(f"{exit[0]},{exit[1]}")
    lines.append(path)

    with open(filename, "w") as f:
        for line in lines:
            f.write(line + "\n")
