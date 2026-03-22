"""Game state and main game loop logic."""

import pygame
from src.config import GameConfig, DEFAULT_CONFIG
from src.logger import log_tick, log_game_over
from src.model import (
    GameState,
    Snake,
    GameField,
    GameStatus,
    Timer,
    Direction,
)
from src.constants import PLAYER_ID, AI_1_ID, AI_2_ID
from src.apple_manager import initialize_apples
from src.ai import update_ai_snakes
from src.movement import move_snake
from src.game_rules import update_game_rules
from src.timer import advance_round_timer, round_should_end


class GameStateManager(GameState):
    """Extended GameState with game loop logic."""

    def __init__(self, config: GameConfig = DEFAULT_CONFIG):
        """Initialize game state with three snakes and apples."""
        self.config = config
        super().__init__(
            game_field=GameField(width=config.field_width, height=config.field_height),
            snakes=[],
            apples=[],
            timer=Timer(config.round_duration_seconds),
            status=GameStatus.RUNNING,
        )

        # Create three snakes at separate start positions to avoid immediate collision
        center_x = config.field_width // 2
        center_y = config.field_height // 2

        self.snakes = [
            Snake(
                id=PLAYER_ID,
                is_human=True,
                segments=[
                    (center_x, center_y),
                    (center_x - 1, center_y),
                    (center_x - 2, center_y),
                ],
                direction=Direction.RIGHT,
            ),
            Snake(
                id=AI_1_ID,
                is_human=False,
                segments=[
                    (center_x, center_y + 4),
                    (center_x - 1, center_y + 4),
                    (center_x - 2, center_y + 4),
                ],
                direction=Direction.RIGHT,
            ),
            Snake(
                id=AI_2_ID,
                is_human=False,
                segments=[
                    (center_x, center_y - 4),
                    (center_x - 1, center_y - 4),
                    (center_x - 2, center_y - 4),
                ],
                direction=Direction.RIGHT,
            ),
        ]
        self.scoreboard_snakes = list(self.snakes)

        # Initialize apples
        initialize_apples(self)

    def handle_input(self, key: int) -> None:
        """
        Handle keyboard input for human player.

        Args:
            key: Pygame key code
        """
        if self.is_game_over():
            return

        if key == pygame.K_SPACE:
            self.toggle_pause()
            return

        if not self.is_running():
            return

        player = next((s for s in self.snakes if s.id == PLAYER_ID), None)
        if not player:
            return

        from src.input_handler import handle_player_input

        handle_player_input(key, player)

    def toggle_pause(self) -> None:
        """Toggle paused state for the current round."""
        if self.is_game_over():
            return

        if self.is_paused():
            self.status = GameStatus.RUNNING
        else:
            self.status = GameStatus.PAUSED

    def tick(self, dt: float) -> None:
        """
        Update game state by dt seconds.

        Args:
            dt: Delta time in seconds
        """
        if self.is_game_over() or self.is_paused():
            return

        # Update timer
        advance_round_timer(self, dt)
        log_tick(dt, self.timer.remaining_seconds)

        # Update AI snakes direction before moving
        update_ai_snakes(self)

        # Move all snakes
        for snake in self.snakes:
            if snake.is_alive():
                move_snake(snake, self.game_field)

        # Update game rules (collisions, consumption)
        update_game_rules(self)

        # Check end conditions
        if round_should_end(self):
            self.status = GameStatus.GAME_OVER
            log_game_over(
                status=self.status.value,
                duration=self.config.round_duration_seconds - self.timer.remaining_seconds,
                scores={snake.id: snake.score for snake in self.scoreboard_snakes},
            )

    @staticmethod
    def _draw_digit(surface: pygame.Surface, x: int, y: int, digit: int, color, size: int = 10):
        """Draw a digit using lines."""
        # Define segments for each digit (0-9)
        segments = {
            0: [1,1,1,0,1,1,1],
            1: [0,0,1,0,0,1,0],
            2: [1,0,1,1,1,0,1],
            3: [1,0,1,1,0,1,1],
            4: [0,1,1,1,0,1,0],
            5: [1,1,0,1,0,1,1],
            6: [1,1,0,1,1,1,1],
            7: [1,0,1,0,0,1,0],
            8: [1,1,1,1,1,1,1],
            9: [1,1,1,1,0,1,1],
        }
        if digit not in segments:
            return
        seg = segments[digit]
        # Positions: top, top-left, top-right, middle, bottom-left, bottom-right, bottom
        lines = [
            ((x+2, y), (x+size-2, y)),  # top
            ((x, y+2), (x, y+size//2-1)),  # top-left
            ((x+size-1, y+2), (x+size-1, y+size//2-1)),  # top-right
            ((x+2, y+size//2), (x+size-2, y+size//2)),  # middle
            ((x, y+size//2+1), (x, y+size-2)),  # bottom-left
            ((x+size-1, y+size//2+1), (x+size-1, y+size-2)),  # bottom-right
            ((x+2, y+size-1), (x+size-2, y+size-1)),  # bottom
        ]
        for i, line in enumerate(lines):
            if seg[i]:
                pygame.draw.line(surface, color, *line)

    @staticmethod
    def _lighten_color(color: tuple[int, int, int], amount: int = 60) -> tuple[int, int, int]:
        """Return a brighter version of a color for head rendering."""
        return tuple(min(255, channel + amount) for channel in color)

    @classmethod
    def _draw_snake(cls, surface: pygame.Surface, snake: Snake, color, cell_size: int) -> None:
        """Draw a snake body with a more visible head and outline."""
        for index, segment in enumerate(snake.segments):
            x, y = segment
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)

            if index == 0:
                cls._draw_snake_head(surface, rect, snake.direction, color)
                continue

            inner_rect = rect.inflate(-4, -4)
            pygame.draw.rect(surface, color, rect, border_radius=5)
            pygame.draw.rect(surface, (255, 255, 255), rect, width=1, border_radius=5)
            pygame.draw.rect(surface, cls._lighten_color(color, 20), inner_rect, border_radius=4)

    @classmethod
    def _draw_snake_head(
        cls,
        surface: pygame.Surface,
        rect: pygame.Rect,
        direction: Direction,
        color,
    ) -> None:
        """Draw a snake head with eyes facing its movement direction."""
        head_color = cls._lighten_color(color, 80)
        inner_rect = rect.inflate(-2, -2)
        pygame.draw.rect(surface, head_color, rect, border_radius=6)
        pygame.draw.rect(surface, (255, 255, 255), rect, width=2, border_radius=6)
        pygame.draw.rect(surface, color, inner_rect, border_radius=5)

        eye_radius = 2
        pupil_radius = 1
        eye_positions = cls._get_eye_positions(rect, direction)
        for eye_x, eye_y in eye_positions:
            pygame.draw.circle(surface, (255, 255, 255), (eye_x, eye_y), eye_radius)
            pygame.draw.circle(surface, (0, 0, 0), (eye_x, eye_y), pupil_radius)

    @staticmethod
    def _get_eye_positions(rect: pygame.Rect, direction: Direction) -> list[tuple[int, int]]:
        """Return eye coordinates for a snake head based on facing direction."""
        left = rect.left + 6
        right = rect.right - 6
        top = rect.top + 6
        bottom = rect.bottom - 6
        center_x = rect.centerx
        center_y = rect.centery

        if direction == Direction.LEFT:
            return [(left, top), (left, bottom)]
        if direction == Direction.RIGHT:
            return [(right, top), (right, bottom)]
        if direction == Direction.UP:
            return [(left, top), (right, top)]
        return [(left, bottom), (right, bottom)]

    @classmethod
    def _draw_score_block(
        cls,
        surface: pygame.Surface,
        snake: Snake,
        anchor: tuple[int, int],
        color,
        font,
        align: str = "left",
    ) -> None:
        """Draw a score block with score and lives, aligned to a screen edge."""
        if font:
            label = f"{snake.id.upper()}: {snake.score}  {snake.lives}L"
            surface_text = font.render(label, True, (255, 255, 255))
            x = anchor[0] - surface_text.get_width() if align == "right" else anchor[0]
            surface.blit(surface_text, (x, anchor[1]))
            return

        block_width = cls._measure_score_block_width(snake)
        x = anchor[0] - block_width if align == "right" else anchor[0]
        y = anchor[1]
        score_str = str(snake.score)

        cursor_x = x
        for char in score_str:
            cls._draw_digit(surface, cursor_x, y, int(char), (255, 255, 255))
            cursor_x += 15

        cursor_x += 4
        cls._draw_life_icons(surface, cursor_x, y + 5, snake.lives, color)

    @staticmethod
    def _measure_score_block_width(snake: Snake) -> int:
        """Measure width of fallback score + life icon block."""
        digit_width = max(1, len(str(snake.score))) * 15
        life_width = max(0, snake.lives) * 10
        return digit_width + 4 + life_width

    @staticmethod
    def _draw_life_icons(
        surface: pygame.Surface,
        start_x: int,
        center_y: int,
        lives: int,
        color,
    ) -> None:
        """Draw compact life indicators next to the score."""
        for index in range(lives):
            cx = start_x + index * 10 + 4
            pygame.draw.circle(surface, (255, 255, 255), (cx, center_y), 4)
            pygame.draw.circle(surface, color, (cx, center_y), 3)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render game state to pygame surface.

        Args:
            surface: Pygame surface to render to
        """
        from src.constants import (
            COLOR_PLAYER_SNAKE,
            COLOR_AI_SNAKE_1,
            COLOR_AI_SNAKE_2,
            COLOR_APPLE,
        )

        cell_size = 20

        # Draw snakes
        snake_colors = {
            PLAYER_ID: COLOR_PLAYER_SNAKE,
            AI_1_ID: COLOR_AI_SNAKE_1,
            AI_2_ID: COLOR_AI_SNAKE_2,
        }

        for snake in self.snakes:
            color = snake_colors.get(snake.id, (255, 255, 255))
            self._draw_snake(surface, snake, color, cell_size)

        # Draw apples
        for apple in self.apples:
            x, y = apple.position
            pygame.draw.circle(
                surface,
                COLOR_APPLE,
                (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2),
                cell_size // 2,
            )

        # Draw UI text
        font = None
        try:
            font = pygame.font.Font(None, 24)
        except (ImportError, NotImplementedError, Exception):
            # Pygame font may not be available in some environments (e.g., headless CI)
            font = None

        # Draw scores for each snake in corners
        snake_position_map = {
            "human": ((10, 10), "left"),
            "ai_1": ((surface.get_width() - 10, 10), "right"),
            "ai_2": ((10, surface.get_height() - 40), "left"),
        }

        for snake in self.scoreboard_snakes:
            (pos, align) = snake_position_map.get(snake.id, ((10, 10), "left"))
            color = snake_colors.get(snake.id, (255, 255, 255))
            self._draw_score_block(surface, snake, pos, color, font, align=align)

        # Draw timer
        if font:
            timer_text = font.render(
                f"Time: {self.timer.get_remaining_seconds()}s",
                True,
                (255, 255, 255),
            )
            surface.blit(
                timer_text,
                (surface.get_width() - 150, surface.get_height() - 30),
            )
        else:
            # Fallback: draw timer as digits
            timer_str = str(self.timer.get_remaining_seconds())
            x_offset = surface.get_width() - 150
            for char in timer_str:
                if char.isdigit():
                    self._draw_digit(surface, x_offset, surface.get_height() - 30, int(char), (255, 255, 255))
                    x_offset += 15

        # Draw pause overlay
        if self.is_paused():
            if font:
                pause_font = pygame.font.Font(None, 40)
                paused_text = pause_font.render("PAUSED", True, (255, 255, 255))
                prompt_text = font.render("Press Space to resume", True, (255, 255, 255))
                surface.blit(
                    paused_text,
                    (
                        surface.get_width() // 2 - paused_text.get_width() // 2,
                        16,
                    ),
                )
                surface.blit(
                    prompt_text,
                    (
                        surface.get_width() // 2 - prompt_text.get_width() // 2,
                        54,
                    ),
                )

        # Draw game over screen
        if self.is_game_over():
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0, 0))

            if font:
                big_font = pygame.font.Font(None, 48)
                game_over_text = big_font.render("GAME OVER", True, (255, 255, 255))
                surface.blit(
                    game_over_text,
                    (
                        surface.get_width() // 2 - game_over_text.get_width() // 2,
                        surface.get_height() // 2 - 100,
                    ),
                )

                # Final scores
                scores_font = pygame.font.Font(None, 32)
                y_offset = surface.get_height() // 2
                for snake in sorted(self.scoreboard_snakes, key=lambda s: s.score, reverse=True):
                    score_line = scores_font.render(
                        f"{snake.id.upper()}: {snake.score}",
                        True,
                        (255, 255, 255),
                    )
                    surface.blit(
                        score_line,
                        (
                            surface.get_width() // 2 - score_line.get_width() // 2,
                            y_offset,
                        ),
                    )
                    y_offset += 40
            else:
                # Fallback non-font game over text in console
                print("GAME OVER - final scores:", {snake.id: snake.score for snake in self.scoreboard_snakes})
