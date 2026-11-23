#!/usr/bin/env python3
"""Entry point and interactive terminal viewer for the maze generator."""

import sys

from app.config import Coords, MazeConfig, MazeConfigError
from app.display import WALL_COLORS, draw_maze, print_menu
from app.writer import write_maze
from mazegen.solver import shortest_path

TEST_GRID = [
    [9, 5, 5, 3],
    [10, 9, 7, 10],
    [12, 6, 13, 6],
]
TEST_ENTRY = (0, 0)
TEST_EXIT = (3, 2)


def build_maze(config: MazeConfig) -> tuple[list[list[int]], Coords, Coords]:
    """Builds a maze grid and returns the grid with entry and exit cells.

    Args:
        config: Validated maze configuration.

    Returns:
        A tuple of ``(grid, entry, exit)``.
    """
    # TODO: Replace with KruskalMazeGen(config).generate() once implemented.
    raise NotImplementedError("Maze generator is not implemented yet.")


def main() -> None:
    """Runs the CLI maze generator and interactive display loop."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    try:
        config = MazeConfig.from_file(sys.argv[1])
        grid, entry, exit_pos = build_maze(config)
        path = shortest_path(grid, entry, exit_pos)  # type: ignore
        write_maze(
            config.output_file,
            grid,
            entry,
            exit_pos,
            path
        )  # type: ignore
    except MazeConfigError as exc:
        print("Error:", exc, file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print("Error: cannot write output file:", exc, file=sys.stderr)
        sys.exit(1)

    show_path = False
    color_index = 0

    while True:
        shown_path = path if show_path else ""
        draw_maze(
            grid,
            entry,
            exit_pos,
            shown_path,
            WALL_COLORS[color_index]
        )  # type: ignore
        print_menu()

        try:
            choice = input("Choice (1-4): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if choice == "1":
            try:
                grid, entry, exit_pos = build_maze(config)
                path = shortest_path(grid, entry, exit_pos)  # type: ignore
                write_maze(
                    config.output_file,
                    grid,
                    entry,
                    exit_pos,
                    path
                )  # type: ignore
            except OSError as exc:
                print("Error: cannot write output file:", exc)
                break
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(WALL_COLORS)
        elif choice == "4":
            print("ELO!")
            break


if __name__ == "__main__":
    main()
