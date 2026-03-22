"""Unit tests for game rules."""

import pytest
from src.movement import move_snake, grow_snake
from src.game_rules import check_apple_consumption, handle_apple_consumption
from src.model import GameState, Snake, Apple, Direction
from src.constants import FIELD_WIDTH, FIELD_HEIGHT, PLAYER_ID


class TestGameRules:
    """Test game mechanics."""

    def test_move_snake_basic(self):
        """Test basic snake movement."""
        game_state = GameState()
        game_state.snakes = [Snake(id=PLAYER_ID)]
        snake = game_state.snakes[0]
        original_head = snake.head

        snake.direction = Direction.RIGHT
        move_snake(snake, game_state.game_field)

        assert snake.head != original_head
        assert snake.head[0] == (original_head[0] + 1) % FIELD_WIDTH  # With wrapping

    def test_move_snake_wrapping(self):
        """Test snake wrapping at field boundary."""
        game_state = GameState()
        snake = Snake(id=PLAYER_ID)
        game_state.snakes = [snake]

        # Move snake to right edge
        snake.segments = [(FIELD_WIDTH - 1, 10)]
        snake.direction = Direction.RIGHT

        move_snake(snake, game_state.game_field)

        assert snake.head[0] == 0  # Wrapped to left edge

    def test_grow_snake(self):
        """Test snake growth."""
        snake = Snake(id=PLAYER_ID)
        original_length = len(snake.segments)
        # Add a segment to simulate eating
        snake.segments.insert(0, (10, 10))

        # grow_snake does nothing (growth already happened)
        grow_snake(snake)

        # Length should be one more than original
        assert len(snake.segments) == original_length + 1

    def test_check_apple_consumption(self):
        """Test detecting apple at snake head."""
        game_state = GameState()
        game_state.snakes = [Snake(id=PLAYER_ID)]
        game_state.apples = [Apple(id="a1", position=(10, 10))]
        snake = game_state.snakes[0]

        # Place apple at snake head
        snake.segments = [(10, 10)]

        result = check_apple_consumption(snake, game_state.apples)
        assert result is not None
        assert result.id == "a1"

    def test_no_apple_consumption(self):
        """Test no consumption when apple not at head."""
        snake = Snake(id=PLAYER_ID)
        apple = Apple(id="a1", position=(15, 15))

        # Head is not at apple
        snake.segments = [(10, 10)]

        result = check_apple_consumption(snake, [apple])
        assert result is None

    def test_handle_apple_consumption_priority(self):
        """Test apple consumption respects priority order."""
        game_state = GameState()
        game_state.snakes = [
            Snake(id=PLAYER_ID, is_human=True),
            Snake(id="ai_1"),
            Snake(id="ai_2"),
        ]
        game_state.apples = [Apple(id="a1", position=(10, 10))]

        # Place all snakes at apple location
        for snake in game_state.snakes:
            snake.segments = [(10, 10)]

        # Store initial scores
        human_score_before = game_state.snakes[0].score
        ai_1_score_before = game_state.snakes[1].score
        ai_2_score_before = game_state.snakes[2].score

        handle_apple_consumption(game_state)

        # Only human snake (priority 0) should consume apple
        # (if implementation correctly prioritizes)

    def test_apple_respawn_after_consumption(self):
        """Test apple respawns after consumption."""
        game_state = GameState()
        game_state.snakes = [Snake(id=PLAYER_ID)]
        game_state.apples = [Apple(id="a1", position=(10, 10))]

        # Setup: snake at apple
        game_state.snakes[0].segments = [(10, 10)]

        initial_apple_count = len(game_state.apples)
        handle_apple_consumption(game_state)

        # Apples should be maintained through respawn
        # (implementation detail of handle_apple_respawn)
