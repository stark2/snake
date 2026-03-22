"""Collision detection logic."""

from typing import List, Tuple, Optional
from src.logger import log_collision, log_snake_dead
from src.model import Snake, GameState
from src.constants import COLLISION_PRIORITY


def check_snake_collision(snake1: Snake, snake2: Snake) -> bool:
    """
    Check if snake1's head collides with any part of snake2.

    Args:
        snake1: Snake to check (head position)
        snake2: Snake to check against

    Returns:
        True if collision detected
    """
    head = snake1.head
    return head in snake2.segments


def find_collision_segment_index(head: Tuple[int, int], snake: Snake) -> int:
    """
    Find which segment of a snake was hit (index in segments list).

    Args:
        head: Position of the attacking head
        snake: Snake being hit

    Returns:
        Index of the hit segment, or -1 if no collision
    """
    if head not in snake.segments:
        return -1
    return snake.segments.index(head)


def handle_collision_damage(snake: Snake, segment_index: int, deduct_life: bool = True) -> None:
    """
    Apply damage to a snake based on collision location.

    If head is hit (index 0): snake loses all body segments, keeps head.
    If body is hit: snake loses all segments from hit point onwards.

    Args:
        snake: Snake to damage
        segment_index: Index of the hit segment
        deduct_life: If True, decrement snake lives; otherwise, only segments are trimmed
    """
    if segment_index == -1:
        return

    if segment_index == 0:
        # Head hit: keep only head
        snake.segments = [snake.segments[0]]
    else:
        # Body hit: keep segments up to hit point
        snake.segments = snake.segments[:segment_index]

    if deduct_life:
        snake.lives = max(0, snake.lives - 1)


def detect_and_handle_collisions(game_state: GameState) -> List[str]:
    """
    Detect all collisions and apply damage in priority order.

    Priority order is defined by COLLISION_PRIORITY constant.
    All snakes are evaluated in order for attacking potential collisions.

    Args:
        game_state: The game state

    Returns:
        List of snake IDs that died (lives reached 0)
    """
    dead_snakes = []

    # Build a map of snakes by ID for quick lookup
    snake_map = {snake.id: snake for snake in game_state.snakes}

    # Process collisions in priority order
    for attacker_id in COLLISION_PRIORITY:
        if attacker_id not in snake_map:
            continue

        attacker = snake_map[attacker_id]
        if not attacker.is_alive() or len(attacker.segments) == 0:
            continue

        # Check collision with all other snakes
        for victim_id, victim in snake_map.items():
            if victim_id == attacker_id or not victim.is_alive() or len(victim.segments) == 0:
                continue

            # Check if attacker's head hits victim
            collision_index = find_collision_segment_index(attacker.head, victim)
            if collision_index != -1:
                hit_type = "head" if collision_index == 0 else "body"
                deduct_life = victim.is_human

                handle_collision_damage(victim, collision_index, deduct_life=deduct_life)
                log_collision(attacker_id, victim_id, hit_type, victim.lives)

                # AI snakes do not die from collision-based life loss
                if deduct_life and not victim.is_alive():
                    dead_snakes.append(victim_id)
                    log_snake_dead(victim_id)

    return dead_snakes
