"""Configuration models and validation utilities for maze generation.

Provides immutable configuration structures and file-loading helpers to define
and validate maze dimensions, entry/exit coordinates, generation modes, and
optional random seeds.

Typical usage example:

  config = MazeConfig(
      width=20,
      height=15,
      entry=(0, 0),
      exit=(19, 14),
      output_file="maze.txt",
      perfect=True,
      seed=42,
  )
"""

import sys
from dataclasses import dataclass, field
from typing import Any, Protocol

from mazegen.pattern import PATTERN_HEIGHT, PATTERN_WIDTH, pattern_cells

Coords = tuple[int, int]


class Parser(Protocol):
    """Protocol for functions that parse a raw string config value."""

    def __call__(self, value: str, /) -> Any:
        """Parses a raw configuration string into a typed value.

        Args:
          value: Stripped string value read from the configuration file.

        Returns:
          The converted value for the configuration field.
        """


@dataclass(frozen=True)
class KeySpec:
    """Specification for a configuration file key.

    Attributes:
    required: Whether the key must be present in the configuration file.
    parser: Callable protocol used to convert the raw string value.
    """

    required: bool
    parser: Parser = field(repr=False)


def _parse_int(value: str) -> int:
    """Parses a base-10 integer string."""
    return int(value)


def _parse_coords(value: str) -> Coords:
    """Parses an 'x,y' coordinate pair into two integers."""
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError("Expected 'x,y'")
    return (int(parts[0].strip()), int(parts[1].strip()))


def _parse_bool(value: str) -> bool:
    """Parses a case-insensitive 'true' or 'false' string into a boolean."""
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    raise ValueError(f"Expected boolean. Got: {value}")


def _parse_str(value: str) -> str:
    """Validates that a string is non-empty."""
    if value == "":
        raise ValueError("Expected non-empty string.")
    return value


CONFIG_KEYS: dict[str, KeySpec] = {
    "WIDTH": KeySpec(required=True, parser=_parse_int),
    "HEIGHT": KeySpec(required=True, parser=_parse_int),
    "ENTRY": KeySpec(required=True, parser=_parse_coords),
    "EXIT": KeySpec(required=True, parser=_parse_coords),
    "OUTPUT_FILE": KeySpec(required=True, parser=_parse_str),
    "PERFECT": KeySpec(required=True, parser=_parse_bool),
    "SEED": KeySpec(required=False, parser=_parse_int),
}


def _check_in_bounds(coords: Coords, width: int, height: int) -> bool:
    """Checks whether a coordinate pair lies inside the maze bounds."""
    x, y = coords
    return 0 <= x < width and 0 <= y < height


class MazeConfigError(ValueError):
    """Invalid or inconsistent maze configuration parameters."""


@dataclass(frozen=True)
class MazeConfig:
    """Configuration parameters for generating and solving the maze.

    Attributes:
        width: Number of columns in the maze grid.
        height: Number of rows in the maze grid.
        entry: Entry cell coordinates.
        exit: Exit cell coordinates.
        output_file: The file to save the output to.
        perfect: Whether the maze should have a single path with no loops.
        seed: Optional seed for reproducible random generation.
    """

    width: int
    height: int
    entry: Coords
    exit: Coords
    output_file: str
    perfect: bool = True
    seed: int | None = None

    @classmethod
    def from_file(cls, path: str) -> "MazeConfig":
        """Loads and validates maze configuration from a key-value file.

        Args:
            path: Path to the configuration text file.

        Returns:
            A validated MazeConfig instance built from the file entries.

        Raises:
            MazeConfigError: The file cannot be read, contains syntax errors,
                is missing required keys, or has invalid maze values.
        """
        raw: dict[str, str] = {}
        try:
            with open(path, encoding="utf-8") as file:
                for line in file:
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#"):
                        continue
                    if "=" not in stripped:
                        raise MazeConfigError("Configuration is invalid")

                    key, value = stripped.split("=", 1)
                    key = key.strip().upper()
                    value = value.strip()

                    if key not in CONFIG_KEYS:
                        raise MazeConfigError(f"Invalid key: {key}")
                    if key in raw:
                        raise MazeConfigError(f"Duplicate key: {key}")

                    raw[key] = value
        except OSError as exc:
            raise MazeConfigError(
                "The configuration file couldn't be read"
            ) from exc

        parsed: dict[str, Any] = {}

        for key, spec in CONFIG_KEYS.items():
            if key not in raw:
                if spec.required:
                    raise MazeConfigError(f"Key {key} is missing")
                continue

            try:
                parsed[key] = spec.parser(raw[key])
            except ValueError as exc:
                raise MazeConfigError(
                    f"Invalid value for {key}: '{raw[key]}'"
                ) from exc

        return cls(
            width=parsed["WIDTH"],
            height=parsed["HEIGHT"],
            entry=parsed["ENTRY"],
            exit=parsed["EXIT"],
            output_file=parsed["OUTPUT_FILE"],
            perfect=parsed["PERFECT"],
            seed=parsed.get("SEED"),
        )

    def __post_init__(self) -> None:
        """Validates maze configuration.

        Raises:
            MazeConfigError: Dimensions are non-positive, entry or exit is out
                of bounds or identical, or an endpoint falls inside the '42'
                pattern.
        """
        if self.width <= 0:
            raise MazeConfigError("The maze is too narrow (WIDTH <= 0)")
        if self.height <= 0:
            raise MazeConfigError("The maze is too short (HEIGHT <= 0)")

        if not _check_in_bounds(self.entry, self.width, self.height):
            raise MazeConfigError("The entry point is out of bounds")
        if not _check_in_bounds(self.exit, self.width, self.height):
            raise MazeConfigError("The exit point is out of bounds")
        if self.entry == self.exit:
            raise MazeConfigError("Endpoints (entry & exit) are overlapping")

        if self.contains_pattern:
            blocked = pattern_cells(self.width, self.height)
            if self.entry in blocked:
                raise MazeConfigError("Entry point is in the '42' pattern")
            if self.exit in blocked:
                raise MazeConfigError("Exit point is in the '42' pattern")
        else:
            print(
                "Warning: the maze is too small to fit '42' pattern",
                file=sys.stderr,
            )

    @property
    def contains_pattern(self) -> bool:
        """Whether the maze is large enough for the '42' pattern."""
        return (
            self.width >= PATTERN_WIDTH + 2
            and self.height >= PATTERN_HEIGHT + 2
        )
