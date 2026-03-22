"""Unit tests for core model."""

import pytest
from src.model import Snake, Apple, GameField, GameState, Timer, Direction


class TestSnake:
    """Test Snake model."""

    def test_snake_initialization(self):
        """Test snake initializes with correct default segments."""
        snake = Snake(id="test", is_human=True)
        assert len(snake.segments) == 3
        assert snake.head == snake.segments[0]
        assert snake.lives == 3
        assert snake.score == 0
        assert snake.is_alive()

    def test_snake_head_property(self):
        """Test snake head is first segment."""
        snake = Snake(id="test")
        head = snake.head
        assert head == snake.segments[0]

    def test_snake_length_property(self):
        """Test snake length matches segment count."""
        snake = Snake(id="test")
        assert snake.length == 3

    def test_snake_alive_check(self):
        """Test snake alive status."""
        snake = Snake(id="test", lives=1)
        assert snake.is_alive()
        snake.lives = 0
        assert not snake.is_alive()


class TestTimer:
    """Test Timer model."""

    def test_timer_initialization(self):
        """Test timer initializes with correct duration."""
        timer = Timer(60.0)
        assert timer.remaining_seconds == 60.0
        assert not timer.is_expired()

    def test_timer_tick(self):
        """Test timer decreases with tick."""
        timer = Timer(60.0)
        timer.tick(10.0)
        assert timer.remaining_seconds == 50.0

    def test_timer_expiration(self):
        """Test timer expires when reaching zero."""
        timer = Timer(5.0)
        timer.tick(5.0)
        assert timer.is_expired()
        assert timer.remaining_seconds == 0

    def test_timer_cannot_go_negative(self):
        """Test timer doesn't go below zero."""
        timer = Timer(5.0)
        timer.tick(10.0)
        assert timer.remaining_seconds == 0


class TestGameField:
    """Test GameField model."""

    def test_field_wrapping(self):
        """Test field wrapping coordinates."""
        field = GameField(width=20, height=20, wrap=True)
        assert field.wrap_coordinate(20, 0) == (0, 0)
        assert field.wrap_coordinate(-1, 0) == (19, 0)
        assert field.wrap_coordinate(0, 20) == (0, 0)


class TestGameState:
    """Test GameState model."""

    def test_gamestateoccupied_positions(self):
        """Test occupied positions calculation."""
        game = GameState()
        snake = Snake(id="test")
        game.snakes = [snake]
        occupied = game.get_occupied_positions()
        assert len(occupied) == 3  # Initial snake length
        assert snake.head in occupied

    def test_apple_positions(self):
        """Test apple positions calculation."""
        game = GameState()
        apple = Apple(id="test", position=(5, 5))
        game.apples = [apple]
        positions = game.get_apple_positions()
        assert (5, 5) in positions
