"""Unit tests for apple manager."""

import pytest
from src.apple_manager import (
    spawn_apple_at_random_position,
    initialize_apples,
    maintain_apple_count,
)
from src.model import GameState, Apple, Snake, GameField
from src.constants import (
    APPLE_COUNT,
    FIELD_WIDTH,
    FIELD_HEIGHT,
    PLAYER_ID,
    AI_1_ID,
    AI_2_ID,
)


class TestAppleManager:
    """Test apple spawning and management."""

    def test_spawn_apple_not_on_snake(self):
        """Test apple spawned not on snake segments."""
        game_state = GameState()
        # Initialize snakes manually first
        game_state.snakes = [
            Snake(id=PLAYER_ID, is_human=True),
            Snake(id=AI_1_ID),
            Snake(id=AI_2_ID),
        ]
        initial_apple_count = len(game_state.apples)

        # Try to spawn an apple
        occupied = game_state.get_occupied_positions()
        new_apple = spawn_apple_at_random_position(
            occupied,
            game_state.apples,
            FIELD_WIDTH,
            FIELD_HEIGHT,
        )

        if new_apple:
            # Ensure apple not on any snake
            assert new_apple.position not in occupied
            assert isinstance(new_apple, Apple)

    def test_initialize_apples(self):
        """Test initial apple spawning."""
        game_state = GameState()
        game_state.snakes = [
            Snake(id=PLAYER_ID, is_human=True),
            Snake(id=AI_1_ID),
            Snake(id=AI_2_ID),
        ]
        game_state.apples = []

        initialize_apples(game_state)

        assert len(game_state.apples) == APPLE_COUNT

        # Ensure all apples have unique IDs
        apple_ids = [apple.id for apple in game_state.apples]
        assert len(set(apple_ids)) == len(apple_ids)

    def test_maintain_apple_count(self):
        """Test maintaining apple count."""
        game_state = GameState()
        game_state.snakes = [
            Snake(id=PLAYER_ID, is_human=True),
            Snake(id=AI_1_ID),
            Snake(id=AI_2_ID),
        ]
        initialize_apples(game_state)

        # Reduce apple count by removing some
        original_count = len(game_state.apples)
        game_state.apples = game_state.apples[:2] if len(game_state.apples) > 2 else []

        maintain_apple_count(game_state)

        assert len(game_state.apples) == APPLE_COUNT

    def test_apple_spawns_in_bounds(self):
        """Test apples spawn within field bounds."""
        game_state = GameState()

        for apple in game_state.apples:
            assert 0 <= apple.position[0] < FIELD_WIDTH
            assert 0 <= apple.position[1] < FIELD_HEIGHT
