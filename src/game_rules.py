"""Game rules and mechanics."""

from typing import List, Optional, Tuple
from src.logger import log_apple_eaten
from src.model import Snake, Apple, GameState, Direction
from src.apple_manager import handle_apple_respawn
from src.collision import detect_and_handle_collisions


def check_apple_consumption(snake: Snake, apples: List[Apple]) -> Optional[Apple]:
    """
    Check if snake's head is on any apple.

    Args:
        snake: Snake to check
        apples: List of apples

    Returns:
        Eaten apple or None
    """
    head = snake.head
    for apple in apples:
        if apple.position == head:
            return apple
    return None


def handle_apple_consumption(game_state: GameState) -> List[Tuple[Snake, Apple]]:
    """
    Handle all apple consumption in priority order (human → ai_1 → ai_2).

    Args:
        game_state: The game state

    Returns:
        List of (snake, apple) tuples for consumed apples
    """
    from src.constants import COLLISION_PRIORITY

    consumed = []
    consumed_apple_ids = set()

    for snake_id in COLLISION_PRIORITY:
        snake = next((s for s in game_state.snakes if s.id == snake_id), None)
        if not snake or not snake.is_alive() or len(snake.segments) == 0:
            continue

        for apple in game_state.apples:
            if apple.id in consumed_apple_ids:
                continue

            if snake.head == apple.position:
                # Apple consumed by this snake
                snake.score += 1
                consumed.append((snake, apple))
                consumed_apple_ids.add(apple.id)
                break  # Only one apple per snake per tick

    # Respawn consumed apples and log events
    for snake, apple in consumed:
        log_apple_eaten(snake, apple.id)
        handle_apple_respawn(game_state, apple)

    return consumed


def update_game_rules(game_state: GameState) -> None:
    """
    Update game state according to rules (collisions, consumption, etc).

    Args:
        game_state: The game state to update
    """
    # Detect and handle collisions
    dead_snakes = detect_and_handle_collisions(game_state)

    # Handle apple consumption (with priority order) - returns which snakes ate
    eaten_snakes = set()
    consumed = handle_apple_consumption(game_state)
    for snake, apple in consumed:
        eaten_snakes.add(snake.id)

    # Trim tails for snakes that didn't eat
    for snake in game_state.snakes:
        if snake.is_alive() and snake.id not in eaten_snakes and len(snake.segments) > 0:
            snake.segments.pop()

    # Remove dead snakes
    game_state.snakes = [s for s in game_state.snakes if s.is_alive()]
