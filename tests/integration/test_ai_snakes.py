"""Integration tests for AI snakes."""

from src.model import Apple
from src.game_state import GameStateManager
from src.constants import AI_1_ID, AI_2_ID, APPLE_COUNT


def test_ai_snakes_eat_apples_over_ticks():
    game = GameStateManager()

    assert len(game.snakes) == 3
    assert len(game.apples) == APPLE_COUNT

    # Simulate a few ticks, letting AI target apples
    for _ in range(20):
        game.tick(0.1)

    # AI should still be active and apples count maintained
    ai_snakes = [s for s in game.snakes if not s.is_human]
    assert len(ai_snakes) >= 1
    assert len(game.apples) == APPLE_COUNT


def test_ai_snakes_move_each_tick():
    game = GameStateManager()
    ai_1 = next(s for s in game.snakes if s.id == AI_1_ID)
    ai_2 = next(s for s in game.snakes if s.id == AI_2_ID)

    initial_positions = {AI_1_ID: ai_1.head, AI_2_ID: ai_2.head}

    game.tick(0.1)

    if ai_1.is_alive() and ai_1.segments:
        assert ai_1.head != initial_positions[AI_1_ID]

    if ai_2.is_alive() and ai_2.segments:
        assert ai_2.head != initial_positions[AI_2_ID]


def test_ai_snakes_eat_targeted_apples_and_respawn_them():
    game = GameStateManager()
    ai_1 = next(s for s in game.snakes if s.id == AI_1_ID)
    ai_2 = next(s for s in game.snakes if s.id == AI_2_ID)

    game.apples = [
        Apple(id="ai_1_target", position=(ai_1.head[0] + 1, ai_1.head[1])),
        Apple(id="ai_2_target", position=(ai_2.head[0] + 1, ai_2.head[1])),
        Apple(id="extra_1", position=(2, 2)),
        Apple(id="extra_2", position=(4, 4)),
        Apple(id="extra_3", position=(6, 6)),
    ]

    game.tick(0.1)

    assert ai_1.score == 1
    assert ai_2.score == 1
    assert ai_1.length == 4
    assert ai_2.length == 4
    assert len(game.apples) == APPLE_COUNT
