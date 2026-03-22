"""Field wrapping and coordinate logic."""

from typing import Tuple
from src.model import GameField


def wrap_coordinates(field: GameField, x: int, y: int) -> Tuple[int, int]:
    """
    Wrap coordinates around field edges.

    Args:
        field: The game field
        x: X coordinate
        y: Y coordinate

    Returns:
        Wrapped (x, y) tuple
    """
    if field.wrap:
        x = x % field.width
        y = y % field.height
    return x, y


def is_within_bounds(field: GameField, x: int, y: int) -> bool:
    """
    Check if coordinates are within field bounds (before wrapping).

    Args:
        field: The game field
        x: X coordinate
        y: Y coordinate

    Returns:
        True if within bounds, False otherwise
    """
    return 0 <= x < field.width and 0 <= y < field.height
