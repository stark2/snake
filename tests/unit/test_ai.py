"""Unit tests for AI behavior."""

from src.ai import (
    manhattan_distance,
    select_nearest_apple,
    choose_ai_direction,
    update_ai_snakes,
    wrapped_manhattan_distance,
)
from src.model import Snake, Apple, GameState, GameField
from src.constants import AI_1_ID, AI_2_ID, PLAYER_ID
from src.model import Direction


def test_manhattan_distance():
    assert manhattan_distance((0, 0), (3, 4)) == 7


def test_select_nearest_apple():
    snake = Snake(id=AI_1_ID)
    snake.segments = [(0, 0), (-1, 0), (-2, 0)]
    apple1 = Apple(id="a1", position=(1, 1))
    apple2 = Apple(id="a2", position=(10, 10))

    target = select_nearest_apple(snake, [apple1, apple2])
    assert target == apple1


def test_select_nearest_apple_uses_wrapped_distance_when_field_provided():
    snake = Snake(id=AI_1_ID)
    snake.segments = [(0, 0), (29, 0), (28, 0)]
    field = GameField(width=30, height=30)
    near_via_wrap = Apple(id="wrap", position=(29, 0))
    farther_direct = Apple(id="direct", position=(2, 0))

    target = select_nearest_apple(snake, [farther_direct, near_via_wrap], field)
    assert target == near_via_wrap


def test_wrapped_manhattan_distance_prefers_shortest_wrapped_route():
    field = GameField(width=30, height=30)
    assert wrapped_manhattan_distance(field, (0, 0), (29, 0)) == 1


def test_choose_ai_direction_towards_apple():
    game_state = GameState()
    game_state.game_field = GameField()
    snake = Snake(id=AI_1_ID)
    snake.segments = [(5, 5), (4, 5), (3, 5)]
    snake.direction = Direction.RIGHT
    game_state.snakes = [snake]
    game_state.apples = [Apple(id="a1", position=(7, 5))]

    direction = choose_ai_direction(snake, game_state)
    assert direction == Direction.RIGHT


def test_choose_ai_avoids_collision():
    game_state = GameState()
    game_state.game_field = GameField()

    ai = Snake(id=AI_1_ID)
    ai.segments = [(5, 5), (4, 5), (3, 5)]
    ai.direction = Direction.RIGHT

    obstacle = Snake(id=AI_2_ID)
    obstacle.segments = [(6, 5), (6, 6), (6, 7)]
    obstacle.direction = Direction.UP

    game_state.snakes = [ai, obstacle]
    game_state.apples = [Apple(id="a1", position=(8, 5))]

    new_dir = choose_ai_direction(ai, game_state)
    assert new_dir != Direction.RIGHT


def test_choose_ai_direction_prefers_wrapped_route_to_target():
    game_state = GameState()
    game_state.game_field = GameField(width=30, height=30)

    ai = Snake(id=AI_1_ID)
    ai.segments = [(0, 5), (1, 5), (2, 5)]
    ai.direction = Direction.UP

    game_state.snakes = [ai]
    game_state.apples = [Apple(id="a1", position=(29, 5))]

    new_dir = choose_ai_direction(ai, game_state)
    assert new_dir == Direction.LEFT


def test_choose_ai_direction_keeps_axis_when_no_safe_detour_exists():
    game_state = GameState()
    game_state.game_field = GameField(width=10, height=10)

    ai = Snake(id=AI_1_ID)
    ai.segments = [(5, 5), (4, 5), (3, 5)]
    ai.direction = Direction.RIGHT

    blocker_up = Snake(id=AI_2_ID)
    blocker_up.segments = [(5, 4), (5, 3), (5, 2)]

    blocker_down = Snake(id=PLAYER_ID, is_human=True)
    blocker_down.segments = [(5, 6), (5, 7), (5, 8)]

    blocker_ahead = Snake(id="blocker", is_human=False)
    blocker_ahead.segments = [(6, 5), (7, 5), (8, 5)]

    game_state.snakes = [ai, blocker_up, blocker_down, blocker_ahead]
    game_state.apples = [Apple(id="a1", position=(8, 5))]

    new_dir = choose_ai_direction(ai, game_state)
    assert new_dir == Direction.RIGHT


def test_update_ai_snakes_sets_next_direction():
    game_state = GameState()
    game_state.game_field = GameField()

    ai = Snake(id=AI_1_ID)
    ai.segments = [(5, 5), (4, 5), (3, 5)]
    ai.direction = Direction.RIGHT

    player = Snake(id=PLAYER_ID, is_human=True)
    player.segments = [(0, 0), (0, 1), (0, 2)]

    game_state.snakes = [player, ai]
    game_state.apples = [Apple(id="a1", position=(7, 5))]

    update_ai_snakes(game_state)
    assert ai.next_direction is not None
