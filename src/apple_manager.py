"""Apple management logic."""

import random
from typing import List, Set, Tuple
from src.model import Apple, GameState
from src.constants import APPLE_COUNT


_apple_id_counter = 0


def _next_apple_id() -> str:
    global _apple_id_counter
    value = _apple_id_counter
    _apple_id_counter += 1
    return f"apple_{value}"


def spawn_apple_at_random_position(
    occupied_positions: Set[Tuple[int, int]],
    existing_apples: List[Apple],
    field_width: int,
    field_height: int,
) -> Apple:
    """
    Spawn an apple at a random unoccupied position.

    Args:
        occupied_positions: Set of occupied positions (snake segments)
        existing_apples: List of existing apples
        field_width: Width of the field
        field_height: Height of the field

    Returns:
        New Apple instance
    """
    apple_positions = {apple.position for apple in existing_apples}
    all_occupied = occupied_positions | apple_positions

    while True:
        x = random.randint(0, field_width - 1)
        y = random.randint(0, field_height - 1)
        position = (x, y)

        if position not in all_occupied:
            return Apple(id=_next_apple_id(), position=position)


def initialize_apples(game_state: GameState) -> None:
    """
    Initialize the game with APPLE_COUNT apples.

    Args:
        game_state: The game state to initialize
    """
    occupied = game_state.get_occupied_positions()
    game_state.apples = []

    for _ in range(APPLE_COUNT):
        apple = spawn_apple_at_random_position(
            occupied,
            game_state.apples,
            game_state.game_field.width,
            game_state.game_field.height,
        )
        game_state.apples.append(apple)


def handle_apple_respawn(game_state: GameState, eaten_apple: Apple) -> None:
    """
    Respawn an eaten apple at a new random position.

    Args:
        game_state: The game state
        eaten_apple: The apple that was eaten
    """
    # Remove only one eaten apple (in case IDs are duplicated from prior state)
    removed = False
    new_apples = []
    for a in game_state.apples:
        if not removed and a.id == eaten_apple.id:
            removed = True
            continue
        new_apples.append(a)
    game_state.apples = new_apples

    # Spawn new apple
    occupied = game_state.get_occupied_positions()
    new_apple = spawn_apple_at_random_position(
        occupied,
        game_state.apples,
        game_state.game_field.width,
        game_state.game_field.height,
    )
    game_state.apples.append(new_apple)


def maintain_apple_count(game_state: GameState) -> None:
    """
    Ensure game state maintains exactly APPLE_COUNT apples.

    Args:
        game_state: The game state
    """
    while len(game_state.apples) < APPLE_COUNT:
        occupied = game_state.get_occupied_positions()
        apple = spawn_apple_at_random_position(
            occupied,
            game_state.apples,
            game_state.game_field.width,
            game_state.game_field.height,
        )
        game_state.apples.append(apple)
