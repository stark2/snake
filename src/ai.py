"""AI behavior for snake bots."""

from typing import Iterable, List, Optional, Tuple

from src.field import wrap_coordinates
from src.model import Apple, Direction, GameField, GameState, Snake


OPPOSITE_DIRECTION = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def shortest_wrapped_delta(current: int, target: int, size: int) -> int:
    """Return the shortest signed delta on a wrapped axis."""
    forward = (target - current) % size
    backward = (current - target) % size
    if forward <= backward:
        return forward
    return -backward


def wrapped_manhattan_distance(
    field: GameField, start: Tuple[int, int], end: Tuple[int, int]
) -> int:
    """Measure distance using the shortest wrapped path on each axis."""
    dx = abs(shortest_wrapped_delta(start[0], end[0], field.width))
    dy = abs(shortest_wrapped_delta(start[1], end[1], field.height))
    return dx + dy


def select_nearest_apple(
    snake: Snake, apples: List[Apple], field: Optional[GameField] = None
) -> Optional[Apple]:
    if not apples or not snake.segments:
        return None

    head = snake.head
    distance_fn = (
        (lambda apple: wrapped_manhattan_distance(field, head, apple.position))
        if field
        else (lambda apple: manhattan_distance(head, apple.position))
    )
    nearest = min(apples, key=distance_fn)
    return nearest


def _directions_toward_target(
    snake: Snake, target: Apple, field: GameField
) -> List[Direction]:
    """Return ordered directions that reduce wrapped distance to the target."""
    head_x, head_y = snake.head
    delta_x = shortest_wrapped_delta(head_x, target.position[0], field.width)
    delta_y = shortest_wrapped_delta(head_y, target.position[1], field.height)

    ordered: List[Direction] = []
    horizontal = Direction.RIGHT if delta_x > 0 else Direction.LEFT
    vertical = Direction.DOWN if delta_y > 0 else Direction.UP

    if delta_x == 0 and delta_y == 0:
        return ordered

    if delta_x == 0:
        return [vertical]

    if delta_y == 0:
        return [horizontal]

    if abs(delta_x) >= abs(delta_y):
        ordered.extend([horizontal, vertical])
    else:
        ordered.extend([vertical, horizontal])

    return ordered


def _perpendicular_directions(direction: Direction) -> List[Direction]:
    if direction in (Direction.LEFT, Direction.RIGHT):
        return [Direction.UP, Direction.DOWN]
    return [Direction.LEFT, Direction.RIGHT]


def _occupied_positions_for_ai(snake: Snake, game_state: GameState) -> set[Tuple[int, int]]:
    occupied = set(game_state.get_occupied_positions())
    if snake.segments:
        occupied.discard(snake.segments[-1])
    return occupied


def _is_safe_direction(
    snake: Snake, direction: Direction, game_state: GameState, occupied: set[Tuple[int, int]]
) -> bool:
    next_head = wrap_coordinates(
        game_state.game_field,
        snake.head[0] + direction.value[0],
        snake.head[1] + direction.value[1],
    )
    return next_head not in occupied


def _unique_directions(directions: Iterable[Direction]) -> List[Direction]:
    seen = set()
    ordered = []
    for direction in directions:
        if direction not in seen:
            ordered.append(direction)
            seen.add(direction)
    return ordered


def choose_ai_direction(snake: Snake, game_state: GameState) -> Optional[Direction]:
    """Pick AI direction toward nearest apple while avoiding collisions when possible."""
    if not snake.is_alive() or not snake.segments:
        return None

    target = select_nearest_apple(snake, game_state.apples, game_state.game_field)
    if not target:
        return snake.direction

    current_dir = snake.direction
    occupied = _occupied_positions_for_ai(snake, game_state)

    target_directions = [
        direction
        for direction in _directions_toward_target(snake, target, game_state.game_field)
        if direction != OPPOSITE_DIRECTION[current_dir]
    ]
    for direction in target_directions:
        if _is_safe_direction(snake, direction, game_state, occupied):
            return direction

    for direction in _perpendicular_directions(current_dir):
        if _is_safe_direction(snake, direction, game_state, occupied):
            return direction

    fallback_candidates = _unique_directions(
        [current_dir]
        + [
            direction
            for direction in Direction
            if direction != OPPOSITE_DIRECTION[current_dir]
        ]
    )
    for direction in fallback_candidates:
        if _is_safe_direction(snake, direction, game_state, occupied):
            return direction

    return snake.direction


def update_ai_snakes(game_state: GameState) -> None:
    """Update AI direction for each AI snake before movement."""
    for snake in game_state.snakes:
        if snake.is_human or not snake.is_alive():
            continue

        new_direction = choose_ai_direction(snake, game_state)
        if new_direction:
            snake.next_direction = new_direction
