"""Core data model for Three-Snake Game."""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from enum import Enum
from src.constants import (
    INITIAL_SNAKE_LENGTH,
    MAX_LIVES,
    FIELD_WIDTH,
    FIELD_HEIGHT,
    APPLE_COUNT,
)


class Direction(Enum):
    """Snake direction."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


@dataclass
class Snake:
    """Represents a snake in the game."""

    id: str
    segments: List[Tuple[int, int]] = field(default_factory=list)  # [(x, y), ...] head first
    direction: Direction = Direction.RIGHT
    lives: int = MAX_LIVES
    score: int = 0
    is_human: bool = False
    next_direction: Optional[Direction] = None  # For buffered input

    def __post_init__(self):
        """Initialize snake with default segments if empty."""
        if not self.segments:
            # Start at center, head first
            center_x, center_y = FIELD_WIDTH // 2, FIELD_HEIGHT // 2
            self.segments = [
                (center_x, center_y),
                (center_x - 1, center_y),
                (center_x - 2, center_y),
            ]

    @property
    def head(self) -> Tuple[int, int]:
        """Get the head position."""
        return self.segments[0]

    @property
    def length(self) -> int:
        """Get the snake length."""
        return len(self.segments)

    def is_alive(self) -> bool:
        """Check if snake is still alive."""
        return self.lives > 0


@dataclass
class Apple:
    """Represents an apple in the game."""

    id: str
    position: Tuple[int, int]


@dataclass
class GameField:
    """Represents the game field."""

    width: int = FIELD_WIDTH
    height: int = FIELD_HEIGHT
    wrap: bool = True

    def wrap_coordinate(self, x: int, y: int) -> Tuple[int, int]:
        """Wrap coordinates around field edges."""
        if self.wrap:
            x = x % self.width
            y = y % self.height
        return x, y


@dataclass
class Timer:
    """Countdown timer for the game."""

    remaining_seconds: float

    def __init__(self, duration: float = 60.0):
        """Initialize timer with duration in seconds."""
        self.remaining_seconds = float(duration)

    def tick(self, dt: float) -> None:
        """Update timer by dt seconds."""
        self.remaining_seconds = max(0, self.remaining_seconds - dt)

    def is_expired(self) -> bool:
        """Check if timer has expired."""
        return self.remaining_seconds <= 0

    def get_remaining_seconds(self) -> int:
        """Get remaining seconds as integer."""
        return int(self.remaining_seconds)


class GameStatus(Enum):
    """Game status."""

    RUNNING = "running"
    PAUSED = "paused"
    GAME_OVER = "game_over"


@dataclass
class GameState:
    """Represents the overall game state."""

    game_field: GameField = field(default_factory=GameField)
    snakes: List[Snake] = field(default_factory=list)
    apples: List[Apple] = field(default_factory=list)
    timer: Timer = field(default_factory=Timer)
    status: GameStatus = GameStatus.RUNNING

    def is_running(self) -> bool:
        """Check if game is running."""
        return self.status == GameStatus.RUNNING

    def is_paused(self) -> bool:
        """Check if game is paused."""
        return self.status == GameStatus.PAUSED

    def is_game_over(self) -> bool:
        """Check if the round has ended."""
        return self.status == GameStatus.GAME_OVER

    def get_occupied_positions(self) -> set:
        """Get all occupied positions (snake segments)."""
        occupied = set()
        for snake in self.snakes:
            for segment in snake.segments:
                occupied.add(segment)
        return occupied

    def get_apple_positions(self) -> set:
        """Get all apple positions."""
        return {apple.position for apple in self.apples}
