"""Game UI rendering logic."""

import pygame
from src.model import GameState
from src.constants import (
    COLOR_PLAYER_SNAKE,
    COLOR_AI_SNAKE_1,
    COLOR_AI_SNAKE_2,
    COLOR_APPLE,
    PLAYER_ID,
    AI_1_ID,
    AI_2_ID,
)

CELL_SIZE = 20
HUD_MARGIN = 10
HUD_TEXT_COLOR = (255, 255, 255)
SNAKE_LABELS = {
    PLAYER_ID: "HUMAN",
    AI_1_ID: "AI_1",
    AI_2_ID: "AI_2",
}
BITMAP_GLYPHS = {
    " ": ["000", "000", "000", "000", "000"],
    "(": ["010", "100", "100", "100", "010"],
    ")": ["010", "001", "001", "001", "010"],
    ":": ["000", "010", "000", "010", "000"],
    "_": ["000", "000", "000", "000", "111"],
    "0": ["111", "101", "101", "101", "111"],
    "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"],
    "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"],
    "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"],
    "7": ["111", "001", "001", "001", "001"],
    "8": ["111", "101", "111", "101", "111"],
    "9": ["111", "101", "111", "001", "111"],
    "A": ["010", "101", "111", "101", "101"],
    "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"],
    "G": ["111", "100", "101", "101", "111"],
    "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"],
    "L": ["100", "100", "100", "100", "111"],
    "M": ["101", "111", "111", "101", "101"],
    "N": ["101", "111", "111", "111", "101"],
    "O": ["111", "101", "101", "101", "111"],
    "R": ["110", "101", "110", "101", "101"],
    "S": ["111", "100", "111", "001", "111"],
    "T": ["111", "010", "010", "010", "010"],
    "U": ["101", "101", "101", "101", "111"],
    "V": ["101", "101", "101", "101", "010"],
}


def render_game_state(surface: pygame.Surface, game_state: GameState) -> None:
    """
    Render the complete game state to the Pygame surface.

    Args:
        surface: Pygame surface to render to
        game_state: The current game state
    """
    # Draw snakes
    snake_colors = {
        PLAYER_ID: COLOR_PLAYER_SNAKE,
        AI_1_ID: COLOR_AI_SNAKE_1,
        AI_2_ID: COLOR_AI_SNAKE_2,
    }

    for snake in game_state.snakes:
        color = snake_colors.get(snake.id, (255, 255, 255))
        for segment in snake.segments:
            x, y = segment
            pygame.draw.rect(
                surface,
                color,
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )

    # Draw apples
    for apple in game_state.apples:
        x, y = apple.position
        pygame.draw.circle(
            surface,
            COLOR_APPLE,
            (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
            CELL_SIZE // 2,
        )

    # Draw UI overlays
    _render_hud(surface, game_state)
    _render_game_over_overlay(surface, game_state)


def _render_hud(surface: pygame.Surface, game_state: GameState) -> None:
    """
    Render heads-up display (scores, timer).

    Args:
        surface: Pygame surface to render to
        game_state: The current game state
    """
    font = _load_font(24)
    score_positions = {
        PLAYER_ID: (HUD_MARGIN, HUD_MARGIN),
        AI_1_ID: (surface.get_width() - 170, HUD_MARGIN),
        AI_2_ID: (HUD_MARGIN, surface.get_height() - 35),
    }
    scoreboard_snakes = _get_scoreboard_snakes(game_state)

    for snake in scoreboard_snakes:
        label = _format_score_label(snake)
        _draw_text(
            surface,
            label,
            score_positions.get(snake.id, (HUD_MARGIN, HUD_MARGIN)),
            font=font,
        )

    # Draw timer
    _draw_text(
        surface,
        f"Time: {game_state.timer.get_remaining_seconds()}s",
        (surface.get_width() - 130, surface.get_height() - 35),
        font=font,
    )


def _render_game_over_overlay(surface: pygame.Surface, game_state: GameState) -> None:
    """
    Render game over screen overlay.

    Args:
        surface: Pygame surface to render to
        game_state: The current game state
    """
    if game_state.is_running():
        return

    # Draw semi-transparent overlay
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    surface.blit(overlay, (0, 0))

    big_font = _load_font(48)
    _draw_text_centered(
        surface,
        "GAME OVER",
        surface.get_width() // 2,
        surface.get_height() // 2 - 60,
        font=big_font,
    )

    font = _load_font(32)
    scoreboard_snakes = sorted(
        _get_scoreboard_snakes(game_state),
        key=lambda snake: (-snake.score, snake.id),
    )
    for i, snake in enumerate(scoreboard_snakes):
        _draw_text_centered(
            surface,
            f"{SNAKE_LABELS.get(snake.id, snake.id.upper())}: {snake.score}",
            surface.get_width() // 2,
            surface.get_height() // 2 + i * 40,
            font=font,
        )


def _get_scoreboard_snakes(game_state: GameState):
    return getattr(game_state, "scoreboard_snakes", game_state.snakes)


def _format_score_label(snake) -> str:
    label = SNAKE_LABELS.get(snake.id, snake.id.upper())
    status = "DEAD" if not snake.is_alive() else f"{snake.lives}L"
    return f"{label}: {snake.score} ({status})"


def _load_font(size: int):
    try:
        return pygame.font.Font(None, size)
    except Exception:
        return None


def _draw_text(surface: pygame.Surface, text: str, position: tuple[int, int], font=None) -> None:
    x, y = position
    if font is not None:
        surface_text = font.render(text, True, HUD_TEXT_COLOR)
        surface.blit(surface_text, (x, y))
        return

    _draw_bitmap_text(surface, text, x, y)


def _draw_text_centered(
    surface: pygame.Surface, text: str, center_x: int, y: int, font=None
) -> None:
    if font is not None:
        surface_text = font.render(text, True, HUD_TEXT_COLOR)
        surface.blit(surface_text, (center_x - surface_text.get_width() // 2, y))
        return

    width = _bitmap_text_size(text)[0]
    _draw_bitmap_text(surface, text, center_x - width // 2, y)


def _bitmap_text_size(text: str, scale: int = 2, spacing: int = 1) -> tuple[int, int]:
    width = 0
    for index, char in enumerate(text.upper()):
        glyph = BITMAP_GLYPHS.get(char, BITMAP_GLYPHS[" "])
        width += len(glyph[0]) * scale
        if index < len(text) - 1:
            width += spacing * scale
    height = len(next(iter(BITMAP_GLYPHS.values()))) * scale
    return width, height


def _draw_bitmap_text(
    surface: pygame.Surface,
    text: str,
    x: int,
    y: int,
    color=HUD_TEXT_COLOR,
    scale: int = 2,
    spacing: int = 1,
) -> None:
    cursor_x = x
    for char in text.upper():
        glyph = BITMAP_GLYPHS.get(char, BITMAP_GLYPHS[" "])
        for row_index, row in enumerate(glyph):
            for col_index, pixel in enumerate(row):
                if pixel == "1":
                    pygame.draw.rect(
                        surface,
                        color,
                        (
                            cursor_x + col_index * scale,
                            y + row_index * scale,
                            scale,
                            scale,
                        ),
                    )
        cursor_x += len(glyph[0]) * scale + spacing * scale
