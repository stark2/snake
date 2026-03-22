# Three-Snake Game

Three-Snake Game is a small Pygame arcade prototype built from a Spec Kit workflow. The repository now contains both the playable game and the specification artifacts used to design it.

In each 60-second round, one human-controlled snake competes against two AI snakes on a wrap-around grid. Five apples are always present, scores are tracked per snake, and the round ends when the timer expires or all snakes are eliminated.

## Gameplay Summary

- 1 human snake and 2 AI snakes are active at the start of each round
- The board wraps at the edges instead of using wall collisions
- 5 apples stay on the field and respawn immediately when eaten
- Each snake starts with length 3 and has 3 lives
- Eating an apple increases that snake's length and score
- The default round length is 60 seconds
- The current default game tick rate is 5 updates per second

## Controls

- `Arrow keys` or `WASD`: steer the human snake
- `Space`: toggle pause in the current implementation

## Tech Stack

- Python 3.12+
- Pygame 2.6+
- pytest for unit and integration testing
- black, isort, and flake8 for code quality

## Project Layout

```text
.
├── src/                          # Game code
├── tests/unit/                   # Unit tests
├── tests/integration/            # Gameplay and contract tests
├── ci/run-tests.sh               # CI-style test entrypoint
├── specs/001-three-snake-game/   # Feature spec, research, plan, tasks
└── pyproject.toml                # Tooling configuration
```

## Getting Started

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements-dev.txt
```

3. Start the game from the repository root:

```bash
python src/main.py
```

## Development Commands

Run the game:

```bash
python src/main.py
```

Run tests:

```bash
./ci/run-tests.sh
```

Or directly with pytest:

```bash
python -m pytest tests/ -q
```

Format and lint:

```bash
black src tests
isort src tests
flake8 src tests
```

## Configuration

Default gameplay settings live in `src/config.py` and `src/constants.py`, including:

- board size: `30 x 30`
- apple count: `5`
- initial snake length: `3`
- max lives per snake: `3`
- round duration: `60` seconds
- tick rate: `5 Hz`

## Specifications and Planning Artifacts

This repository still includes the planning material for the feature under `specs/001-three-snake-game/`, including:

- `spec.md` for feature requirements
- `plan.md` for implementation planning
- `research.md` and `data-model.md` for design notes
- `tasks.md` for delivery breakdown
- `contracts/` and `checklists/` for supporting docs

These files are useful if you want to trace implementation decisions back to the original specification.
