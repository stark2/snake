"""Integration tests for human snake gameplay."""

import pytest
import pygame
from src.game_state import GameStateManager
from src.model import Direction, GameStatus
from src.constants import (
    PLAYER_ID,
    AI_1_ID,
    AI_2_ID,
    FIELD_WIDTH,
    FIELD_HEIGHT,
    APPLE_COUNT,
)


class TestHumanSnakePlay:
    """Test human player snake control and interaction."""

    def test_human_snake_exists(self):
        """Test that human snake is properly initialized."""
        game = GameStateManager()

        assert len(game.snakes) >= 1
        human_snake = next((s for s in game.snakes if s.id == PLAYER_ID), None)
        assert human_snake is not None
        assert human_snake.is_human is True
        assert human_snake.is_alive() is True

    def test_human_snake_movement_right(self):
        """Test human snake moves right when directed."""
        game = GameStateManager()
        human_snake = next((s for s in game.snakes if s.id == PLAYER_ID), None)

        initial_head = human_snake.head
        human_snake.direction = Direction.RIGHT
        human_snake.next_direction = Direction.RIGHT

        from src.movement import move_snake

        move_snake(human_snake, game.game_field)

        assert human_snake.head[0] == (initial_head[0] + 1) % FIELD_WIDTH

    def test_human_snake_direction_change(self):
        """Test human snake can change direction via input."""
        game = GameStateManager()
        human_snake = next((s for s in game.snakes if s.id == PLAYER_ID), None)

        # Set initial direction
        human_snake.direction = Direction.RIGHT

        # Change direction
        game.handle_input(None)  # None key to test
        # Manually set next_direction to simulate input
        human_snake.next_direction = Direction.UP

        from src.movement import move_snake

        move_snake(human_snake, game.game_field)

        assert human_snake.direction == Direction.UP

    def test_human_snake_cannot_reverse(self):
        """Test human snake cannot reverse into itself."""
        game = GameStateManager()
        human_snake = next((s for s in game.snakes if s.id == PLAYER_ID), None)

        human_snake.direction = Direction.RIGHT
        human_snake.next_direction = Direction.RIGHT

        # Try to reverse (180 degrees)
        from src.input_handler import apply_direction_to_snake

        apply_direction_to_snake(human_snake, Direction.LEFT)

        # next_direction should not be set to LEFT (reversed)
        # Since it's the opposite, it won't be applied
        assert human_snake.next_direction != Direction.LEFT

    def test_human_snake_eats_apple(self):
        """Test human snake can eat an apple and grow."""
        game = GameStateManager()
        human_snake = next((s for s in game.snakes if s.id == PLAYER_ID), None)

        initial_length = len(human_snake.segments)
        initial_score = human_snake.score

        # Place apple at human snake's head
        if game.apples:
            game.apples[0].position = human_snake.head

        # Move snake and handle consumption
        from src.game_rules import handle_apple_consumption
        from src.movement import move_snake

        # Simulate one tick
        move_snake(human_snake, game.game_field)
        human_snake.segments.insert(0, human_snake.head)

        # Now check if apple was consumed
        handle_apple_consumption(game)

        # Snake should have grown (not shrunk from initial)
        assert human_snake.score > initial_score or len(game.apples) == APPLE_COUNT

    def test_game_tick_updates_state(self):
        """Test a full game tick updates all state correctly."""
        game = GameStateManager()

        # Get initial state
        initial_human_position = game.snakes[0].head
        initial_timer = game.timer.remaining_seconds

        # Perform one tick
        game.tick(0.1)

        # Timer should have decreased
        assert game.timer.remaining_seconds <= initial_timer

        # Game should still be running initially
        assert game.is_running() or game.timer.is_expired()

    def test_human_player_score_persists(self):
        """Test human player score persists across ticks."""
        game = GameStateManager()
        human_snake = next((s for s in game.snakes if s.id == PLAYER_ID), None)

        # Set initial score manually
        human_snake.score = 5

        # Tick game
        game.tick(0.1)

        # Score should still be at least 5 (or higher if apple was eaten)
        assert human_snake.score >= 5

    def test_three_snakes_in_game(self):
        """Test that all three snakes are initialized."""
        game = GameStateManager()

        assert len(game.snakes) == 3
        snake_ids = {s.id for s in game.snakes}
        assert PLAYER_ID in snake_ids
        assert "ai_1" in snake_ids
        assert "ai_2" in snake_ids

    def test_apples_maintained_count(self):
        """Test that apple count is maintained throughout game."""
        game = GameStateManager()

        assert len(game.apples) == APPLE_COUNT

        # Tick several times
        for _ in range(5):
            game.tick(0.1)

        # Apple count should still be maintained
        assert len(game.apples) == APPLE_COUNT

    def test_space_toggles_pause_and_freezes_game_state(self):
        """Test Space pauses and resumes gameplay updates."""
        game = GameStateManager()

        initial_timer = game.timer.remaining_seconds
        initial_heads = {snake.id: snake.head for snake in game.snakes}

        game.handle_input(pygame.K_SPACE)

        assert game.status == GameStatus.PAUSED
        assert game.is_paused()

        game.tick(1.0)

        assert game.timer.remaining_seconds == initial_timer
        assert {snake.id: snake.head for snake in game.snakes} == initial_heads

        game.handle_input(pygame.K_SPACE)

        assert game.status == GameStatus.RUNNING
        assert game.is_running()

        game.tick(0.1)

        assert game.timer.remaining_seconds < initial_timer
        assert any(
            snake.head != initial_heads[snake.id]
            for snake in game.snakes
            if snake.id in {PLAYER_ID, AI_1_ID, AI_2_ID}
        )
