"""Runtime configuration for Three-Snake Game."""

from dataclasses import dataclass
from src.constants import FIELD_WIDTH, FIELD_HEIGHT


@dataclass
class GameConfig:
    """Configurable game settings."""

    field_width: int = FIELD_WIDTH
    field_height: int = FIELD_HEIGHT
    apple_count: int = 5
    initial_snake_length: int = 3
    max_lives: int = 3
    round_duration_seconds: int = 60
    game_tick_rate_hz: int = 5


# Default configuration instance, import and override as needed.
DEFAULT_CONFIG = GameConfig()
