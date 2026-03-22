"""Logging and observability utilities for Three-Snake Game."""

import logging
from src.model import Snake

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("three_snake_game")


def log_tick(elapsed: float, remaining: float) -> None:
    logger.debug("Tick: elapsed=%ss, remaining=%ss", elapsed, remaining)


def log_apple_eaten(snake: Snake, apple_id: str) -> None:
    logger.info("Apple eaten: snake=%s apple=%s score=%s", snake.id, apple_id, snake.score)


def log_collision(attacker_id: str, victim_id: str, hit_type: str, victim_lives: int) -> None:
    logger.info(
        "Collision: attacker=%s victim=%s hit_type=%s victim_lives=%s",
        attacker_id,
        victim_id,
        hit_type,
        victim_lives,
    )


def log_snake_dead(snake_id: str) -> None:
    logger.warning("Snake dead: %s", snake_id)


def log_game_over(status: str, duration: float, scores: dict) -> None:
    logger.info("Game over: status=%s duration=%ss scores=%s", status, duration, scores)
