#!/usr/bin/env python3
import sys

from app.config import ConfigError, load_config
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


def build_maze(settings):
    return TEST_GRID, TEST_ENTRY, TEST_EXIT


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        settings = load_config(sys.argv[1])
        grid, entry, exit = build_maze(settings)
        path = shortest_path(grid, entry, exit)
        write_maze(settings["output_file"], grid, entry, exit, path)
    except ConfigError as e:
        print("Error:", e)
        sys.exit(1)
    except OSError as e:
        print("Error: cannot write output file:", e)
        sys.exit(1)

    show_path = False
    color_index = 0

    while True:
        if show_path:
            shown_path = path
        else:
            shown_path = ""
        draw_maze(grid, entry, exit, shown_path, WALL_COLORS[color_index])
        print_menu()

        try:
            choice = input("Choice (1-4): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if choice == "1":
            try:
                grid, entry, exit = build_maze(settings)
                path = shortest_path(grid, entry, exit)
                write_maze(settings["output_file"], grid, entry, exit, path)
            except OSError as e:
                print("Error: cannot write output file:", e)
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
