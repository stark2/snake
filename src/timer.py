"""Timer helpers for the game loop."""

from src.model import GameState


def advance_round_timer(game_state: GameState, dt: float) -> None:
    """Advance the round timer by the elapsed delta time."""
    game_state.timer.tick(dt)


def round_should_end(game_state: GameState) -> bool:
    """Determine whether the round has reached a terminal state."""
    scoreboard_snakes = getattr(game_state, "scoreboard_snakes", game_state.snakes)
    all_snakes_eliminated = not any(snake.is_alive() for snake in scoreboard_snakes)
    return game_state.timer.is_expired() or all_snakes_eliminated
