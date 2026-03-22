"""Player input handling for human-controlled snake."""

import pygame
from src.model import Direction, Snake


def get_direction_from_key(key: int) -> Direction | None:
    """
    Map a pygame key code to a game Direction.

    Args:
        key: Pygame key code

    Returns:
        Direction enum or None if key is not mapped
    """
    key_to_direction = {
        pygame.K_UP: Direction.UP,
        pygame.K_w: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_s: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_a: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_d: Direction.RIGHT,
    }

    return key_to_direction.get(key)


def apply_direction_to_snake(snake: Snake, direction: Direction) -> None:
    """
    Apply a direction to a snake, preventing 180-degree reversal.

    Args:
        snake: Snake to update
        direction: Direction to apply
    """
    if direction is None:
        return

    # Prevent reverse direction (snake cannot turn 180 degrees into itself)
    opposite = {
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT,
    }

    # Only allow direction change if it's not the opposite of current direction
    if direction != opposite[snake.direction]:
        snake.next_direction = direction


def handle_player_input(key: int, player_snake: Snake) -> None:
    """
    Process a single keyboard input for the player snake.
    Handles direction buffering and prevents invalid moves.

    Args:
        key: Pygame key code pressed
        player_snake: The human player's snake
    """
    direction = get_direction_from_key(key)
    if direction:
        apply_direction_to_snake(player_snake, direction)
