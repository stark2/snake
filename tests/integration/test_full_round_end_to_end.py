import pytest

from src.game_state import GameStateManager


def test_full_round_fast_forward_game_over():
    game = GameStateManager()
    # artificially fast-forward the round to finish quickly in test
    assert game.is_running()

    # Simulate one second steps until game ends (timer should count down from 60 sec)
    for _ in range(65):
        game.tick(1.0)

    assert game.timer.is_expired() or not game.is_running()
    assert game.status.name == "GAME_OVER"

    # Ensure game over condition with remaining snakes 0 or expired timer
    assert game.timer.remaining_seconds == 0


def test_full_round_checker_snakes_are_terminal_state():
    game = GameStateManager()
    # after game over by timer it should keep status once over
    game.tick(100.0)
    assert game.status.name == "GAME_OVER"
    assert all(not s.is_alive() or s.lives >= 0 for s in game.snakes)
