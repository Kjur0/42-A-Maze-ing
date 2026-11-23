"""Abstract base interface and wall bitmasks for maze generators."""

from abc import ABC, abstractmethod

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

ALL_WALLS = NORTH | EAST | SOUTH | WEST


class BaseMazeGen(ABC):
    """Interface for generators producing a 2D grid of cell wall bitmasks."""

    @abstractmethod
    def generate(self) -> list[list[int]]:
        """Generates and returns a maze grid of wall bitmask integers.

        Returns:
            A 2D list indexed as ``grid[y][x]`` containing wall bitmasks per
            cell.
        """
