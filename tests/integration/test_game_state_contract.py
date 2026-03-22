from src.game_state import GameStateManager
from src.model import GameStatus
from src.constants import FIELD_WIDTH, FIELD_HEIGHT


def test_game_state_contract_initial_state():
    game = GameStateManager()

    # Field constraints
    assert game.game_field.width == FIELD_WIDTH
    assert game.game_field.height == FIELD_HEIGHT
    assert game.game_field.wrap is True

    # Three snakes initial state
    assert len(game.snakes) == 3
    assert {s.id for s in game.snakes} == {"human", "ai_1", "ai_2"}

    # Apple invariants
    assert len(game.apples) == 5
    apple_positions = {apple.position for apple in game.apples}
    assert len(apple_positions) == 5
    for snake in game.snakes:
        assert snake.lives >= 0 and snake.lives <= 3
        assert len(snake.segments) >= 1
        assert snake.score == 0
        # no apple shares position with snake
        assert not any(segment in apple_positions for segment in snake.segments)

    # Timer and status
    assert isinstance(game.timer.remaining_seconds, float)
    assert game.timer.remaining_seconds == 60.0
    assert game.status == GameStatus.RUNNING


def test_game_state_contract_updates_properly():
    game = GameStateManager()
    game.tick(1.0)

    assert game.timer.remaining_seconds == 59.0
    assert game.status == GameStatus.RUNNING
    assert len(game.apples) == 5

    # Query invariants after tick
    apple_positions = {apple.position for apple in game.apples}
    assert not any(segment in apple_positions for snake in game.snakes for segment in snake.segments)
