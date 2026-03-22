"""Game constants for Three-Snake Game."""

# Field dimensions (scaled x3)
FIELD_WIDTH = 30
FIELD_HEIGHT = 30

# Apple configuration
APPLE_COUNT = 5

# Snake configuration
INITIAL_SNAKE_LENGTH = 3
MAX_LIVES = 3

# Game timing
ROUND_DURATION_SECONDS = 60
GAME_TICK_RATE_HZ = 5  # Slowed down from 10 to 5 ticks per second

# Colors (RGB)
COLOR_PLAYER_SNAKE = (0, 255, 0)  # Green
COLOR_AI_SNAKE_1 = (255, 0, 0)  # Red
COLOR_AI_SNAKE_2 = (0, 0, 255)  # Blue
COLOR_APPLE = (255, 255, 0)  # Yellow
COLOR_BACKGROUND = (0, 0, 0)  # Black

# Snake IDs
PLAYER_ID = "human"
AI_1_ID = "ai_1"
AI_2_ID = "ai_2"

# Collision priority (for deterministic resolution)
COLLISION_PRIORITY = [PLAYER_ID, AI_1_ID, AI_2_ID]
