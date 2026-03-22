# Quickstart: Three-Snake Game

## Setup

1. Install Python 3.12+.
2. Install dependencies:
   - `pip install pygame`

## Running

1. From repository root, run:
   - `python src/main.py` (if using Pygame implementation)
   - or open Godot project at `godot/` and run scene.

## Controls

- Arrow keys or WASD to steer human snake.

## Gameplay

- 3 snakes active (1 human, 2 AI)
- 5 apples present; eaten apples respawn instantly at random unoccupied cell
- 60-second countdown timer shown bottom-right
- Explore score display in corners for each snake

## Exit

- Game ends automatically when timer hits 0 or all snakes are dead.
- Display final score panel.

## Phase 6 (Polish) Notes

- Reverse-move and invalid key input are ignored for the human snake.
- Configuration is in `src/config.py` with board size, tick rate, and round duration.
- Logging is available via `src/logger.py` and can be enabled by setting the logger level in `src/logger.py`.

## Demo Script

1. Start the game from repo root:
   - `python src/main.py`
2. Record a short session in OBS or native screen recording.
3. Narrate:
   - "Human snake controlled with WASD/arrow keys."
   - "AI snakes track apples and avoid collisions."
   - "Timer counts down from 60 sec and game ends with final scores." 
   - "Collision and apple-eaten events are emitted to logs."
4. Stop after game over and save clip as `video/demo.mp4`.
