"""Snake movement and positioning logic."""

from src.model import Snake, GameField


def move_snake(snake: Snake, game_field: GameField) -> None:
    """
    Move a snake by one step in its current direction.
    Apply wrapping if enabled. Snake segments grow and are trimmed by game rules.

    The snake head is added at the start of the segments list. Tail trimming
    is handled by update_game_rules() based on whether the snake ate an apple.

    Args:
        snake: Snake to move
        game_field: The game field for wrapping
    """
    if not snake.is_alive() or len(snake.segments) == 0:
        return

    # Use next_direction if available, else use current direction
    direction = snake.next_direction or snake.direction
    snake.direction = direction
    snake.next_direction = None

    # Calculate new head position
    dx, dy = direction.value
    current_head = snake.head
    new_x = current_head[0] + dx
    new_y = current_head[1] + dy

    # Wrap if necessary
    new_x, new_y = _wrap_position(game_field, new_x, new_y)

    # Add new head (tail trimming handled by game rules)
    snake.segments.insert(0, (new_x, new_y))


def _wrap_position(game_field: GameField, x: int, y: int) -> tuple:
    """
    Wrap coordinates around field edges if wrapping is enabled.

    Args:
        game_field: The game field (with width, height, wrap flag)
        x: X coordinate
        y: Y coordinate

    Returns:
        Wrapped (x, y) coordinates
    """
    if game_field.wrap:
        x = x % game_field.width
        y = y % game_field.height
    return x, y


def grow_snake(snake: Snake) -> None:
    """
    Keep snake tail (snake grows by 1).
    Called after apple consumption. Tail was already not removed in this move.

    Args:
        snake: Snake to grow
    """
    # No action needed - snake already grew because tail wasn't removed
    pass
