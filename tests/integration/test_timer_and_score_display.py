"""Integration tests for timer and score display behavior."""

from types import SimpleNamespace

import pygame

from src.constants import AI_1_ID, AI_2_ID, PLAYER_ID
from src.game_state import GameStateManager
from src.model import GameStatus
from src.ui import render_game_state
import src.ui as ui_module


class FakeFont:
    """Test double for pygame fonts that records rendered text."""

    def __init__(self, rendered_texts):
        self.rendered_texts = rendered_texts

    def render(self, text, antialias, color):
        self.rendered_texts.append(text)
        surface = pygame.Surface((max(20, len(text) * 6), 16))
        surface.fill((255, 255, 255))
        return surface


def test_timer_countdown_and_hud_rendering(monkeypatch):
    rendered_texts = []
    monkeypatch.setattr(
        ui_module.pygame,
        "font",
        SimpleNamespace(Font=lambda *args, **kwargs: FakeFont(rendered_texts)),
    )

    game = GameStateManager()
    human = next(snake for snake in game.snakes if snake.id == PLAYER_ID)
    ai_1 = next(snake for snake in game.snakes if snake.id == AI_1_ID)
    ai_2 = next(snake for snake in game.snakes if snake.id == AI_2_ID)
    human.score = 3
    ai_1.score = 2
    ai_2.score = 1

    game.tick(1.0)
    surface = pygame.Surface((600, 600))
    render_game_state(surface, game)

    assert game.timer.remaining_seconds == 59.0
    assert "HUMAN: 3 (3L)" in rendered_texts
    assert "AI_1: 2 (3L)" in rendered_texts
    assert "AI_2: 1 (3L)" in rendered_texts
    assert "Time: 59s" in rendered_texts
    assert surface.get_at((10, 10))[:3] == (255, 255, 255)
    assert surface.get_at((430, 10))[:3] == (255, 255, 255)
    assert surface.get_at((10, 565))[:3] == (255, 255, 255)
    assert surface.get_at((470, 565))[:3] == (255, 255, 255)


def test_timer_expiration_triggers_game_over_overlay_with_final_scores(monkeypatch):
    rendered_texts = []
    monkeypatch.setattr(
        ui_module.pygame,
        "font",
        SimpleNamespace(Font=lambda *args, **kwargs: FakeFont(rendered_texts)),
    )

    game = GameStateManager()
    human = next(snake for snake in game.snakes if snake.id == PLAYER_ID)
    ai_1 = next(snake for snake in game.snakes if snake.id == AI_1_ID)
    ai_2 = next(snake for snake in game.snakes if snake.id == AI_2_ID)

    human.score = 4
    ai_1.score = 7
    ai_2.score = 2
    ai_2.lives = 0
    game.snakes = [human, ai_1]

    game.tick(game.config.round_duration_seconds)
    surface = pygame.Surface((600, 600))
    render_game_state(surface, game)

    assert game.status == GameStatus.GAME_OVER
    assert "GAME OVER" in rendered_texts
    assert "AI_1: 7" in rendered_texts
    assert "HUMAN: 4" in rendered_texts
    assert "AI_2: 2" in rendered_texts
