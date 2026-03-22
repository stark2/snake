"""Unit tests for collision detection."""

import pytest
from src.collision import (
    check_snake_collision,
    find_collision_segment_index,
    handle_collision_damage,
)
from src.model import Snake, Direction


class TestCollisionDetection:
    """Test collision detection."""

    def test_no_collision(self):
        """Test no collision when snakes don't touch."""
        snake1 = Snake(id="s1")
        snake2 = Snake(id="s2")
        # Move snake2 far away from default center (15,15) now
        snake2.segments = [(25, 25), (25, 26), (25, 27)]
        assert not check_snake_collision(snake1, snake2)

    def test_head_collision(self):
        """Test collision when head hits body."""
        snake1 = Snake(id="s1")
        snake2 = Snake(id="s2")
        # Set snake2's position to collide with snake1's head
        snake2.segments = [(10, 10), (10, 11), (10, 12)]
        snake1.segments = [(10, 10), (11, 10), (12, 10)]
        # Now snake1's head (10,10) collides with snake2's head
        # But we need snake2's body to be at snake1's head position
        snake2.segments = [(9, 9), (10, 10), (11, 11)]
        assert check_snake_collision(snake1, snake2)

    def test_collision_segment_index(self):
        """Test finding collision segment index."""
        snake = Snake(id="test")
        snake.segments = [(10, 10), (11, 10), (12, 10)]

        # Collision with head
        assert find_collision_segment_index((10, 10), snake) == 0

        # Collision with body
        assert find_collision_segment_index((11, 10), snake) == 1

        # No collision
        assert find_collision_segment_index((15, 15), snake) == -1

    def test_head_collision_damage(self):
        """Test damage when head is hit."""
        snake = Snake(id="test", lives=3)
        snake.segments = [(10, 10), (11, 10), (12, 10)]

        handle_collision_damage(snake, 0)  # Head hit

        assert len(snake.segments) == 1  # Only head remains
        assert snake.lives == 2  # Lost one life

    def test_body_collision_damage(self):
        """Test damage when body is hit."""
        snake = Snake(id="test", lives=3)
        snake.segments = [(10, 10), (11, 10), (12, 10)]

        handle_collision_damage(snake, 1)  # Body at index 1

        assert len(snake.segments) == 1  # Keeps only up to hit point
        assert snake.lives == 2

    def test_body_collision_damage_ai_no_life_loss(self):
        """AI snake should lose segments but not lives on collision."""
        snake = Snake(id="ai_1", lives=3, is_human=False)
        snake.segments = [(10, 10), (11, 10), (12, 10)]

        handle_collision_damage(snake, 1, deduct_life=False)

        assert len(snake.segments) == 1
        assert snake.lives == 3

    def test_body_collision_damage_human_life_loss(self):
        """Human snake should lose lives on collision."""
        snake = Snake(id="human", lives=3, is_human=True)
        snake.segments = [(10, 10), (11, 10), (12, 10)]

        handle_collision_damage(snake, 1, deduct_life=True)

        assert len(snake.segments) == 1
        assert snake.lives == 2

    def test_no_collision_damage(self):
        """Test no damage with invalid segment index."""
        snake = Snake(id="test", lives=3)
        snake.segments = [(10, 10), (11, 10), (12, 10)]

        handle_collision_damage(snake, -1)

        assert len(snake.segments) == 3  # Unchanged
        assert snake.lives == 3  # No damage
