"""Main entrypoint for Three-Snake Game."""

import os
import sys

# Ensure repo root is on sys.path for run modes like `python src/main.py`.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pygame
from src.config import DEFAULT_CONFIG
from src.game_state import GameStateManager
from src.logger import log_game_over


def main():
    """Main game loop."""
    pygame.init()
    # Some pygame builds require explicit font module initialization
    try:
        pygame.font.init()
    except Exception:
        pass

    # Screen setup by configuration
    screen_width = DEFAULT_CONFIG.field_width * 20  # 20 pixels per cell
    screen_height = DEFAULT_CONFIG.field_height * 20
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Three-Snake Game")

    clock = pygame.time.Clock()
    game = GameStateManager(config=DEFAULT_CONFIG)
    running = True

    while running:
        elapsed_ms = clock.tick(game.config.game_tick_rate_hz)
        delta_seconds = elapsed_ms / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.handle_input(event.key)

        # Update game state
        game.tick(delta_seconds)

        # Render
        screen.fill((0, 0, 0))
        game.render(screen)
        pygame.display.flip()

        if game.is_game_over():
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
