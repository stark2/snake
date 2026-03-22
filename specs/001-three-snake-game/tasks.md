---
description: "Task list for Three-Snake Game feature implementation"
---

# Tasks: Three-Snake Game

**Input**: Design documents from `/specs/001-three-snake-game/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Create base feature directories: `src/`, `tests/unit/`, `tests/integration/`, `specs/001-three-snake-game/` (already exists) and add this file `specs/001-three-snake-game/tasks.md`
- [x] T002 Define runtime constants in `src/constants.py`: field width/height, apple count (5), initial snake length (3 segments), max lives (3), round duration (60)
- [x] T003 Add project dependency handling in `requirements.txt`: `pygame>=2.6` (or note Godot alternative) and testing dependencies in `requirements-dev.txt`
- [x] T004 [P] Initialize linter/formatter: `pyproject.toml` with Black + isort + flake8
- [x] T005 [P] Create game entrypoint module `src/main.py` and skeleton run loop stub with `if __name__ == '__main__'`

---

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T006 Implement core data model in `src/model.py`: `Snake`, `Apple`, `GameField`, `GameState`, `Timer`
- [x] T007 [P] Implement field wrapping logic in `src/field.py` for coordinate wrap-around (no wall collisions)
- [x] T008 [P] Implement apple manager in `src/apple_manager.py`: maintain 5 apples, random spawn at unoccupied positions, immediate respawn upon consumption
- [x] T009 [P] Implement collision detection in `src/collision.py`: snake head vs snake body, snake body vs snake head, and segment removal rules; use priority order (human, ai_1, ai_2) for simultaneous collision resolution
- [x] T010 [P] Implement scoring and lives update in `src/game_rules.py` following spec FR-006, FR-007, FR-010, including simultaneous collision resolution
- [x] T011 [P] Implement basic game state transitions in `src/game_state.py`: running, game_over; include end conditions (timer zero, all snakes dead)
- [x] T012 [P] Add unit tests for model and rule primitives in `tests/unit/test_model.py`, `tests/unit/test_collision.py`, `tests/unit/test_apple_manager.py`, `tests/unit/test_game_state.py`

---

## Phase 3: User Story 1 - Play as Human Snake (Priority: P1) 🎯 MVP

**Goal**: Human control and apple eating + collision effects.

**Independent Test**: A player can control the human snake, eat apples, grow, lose segments/lives on collision, and score updates.

### Implementation (must be sequentially reachable)

- [x] T013 [US1] Implement player input handling in `src/input_handler.py` for arrow keys and WASD
- [x] T014 [US1] Implement human snake movement logic in `src/movement.py` (apply direction, update segments, manage head and body)
- [x] T015 [US1] Implement apple consumption logic in `src/game_rules.py` to grow human snake and increment score
- [x] T016 [US1] Add integration test `tests/integration/test_human_snake_play.py` for human movement + apple consumption path
- [x] T017 [US1] Add display health and score in `src/ui.py` (text overlays)

---

## Phase 4: User Story 2 - AI Snake Behavior (Priority: P2)

**Goal**: Add two AI snakes that target the nearest apple and avoid collisions when possible.

**Independent Test**: Two AI snakes act autonomously and interact with apples and collisions.

### Implementation

- [x] T018 [US2] Implement AI target selection in `src/ai.py`: choose nearest apple using Manhattan distance per tick
- [x] T019 [US2] Implement AI movement decision in `src/ai.py` with avoidance strategy (perpendicular detours on imminent collision); handle simultaneous apple consumption with priority (human, ai_1, ai_2)
- [x] T020 [US2] Integrate AI update into main game loop in `src/main.py`
- [x] T021 [US2] Add tests `tests/unit/test_ai.py` for nearest-apple target and collision avoidance
- [x] T022 [US2] Add integration test `tests/integration/test_ai_snakes.py` confirming both AI snakes move to and eat apples

---

## Phase 5: User Story 3 - Game State Display and Timing (Priority: P3)

**Goal**: Real-time score labels for all snakes and 60-second countdown, end-of-game summary.

**Independent Test**: Score and timer are displayed correctly; game ends when time expires or all snakes dead.

### Implementation

- [x] T023 [US3] Implement countdown timer in `src/timer.py` and connect to game loop (`src/main.py`)
- [x] T024 [US3] Implement per-snake score rendering in `src/ui.py` in separate screen corners
- [x] T025 [US3] Implement end-state overlay in `src/ui.py` showing final scores when game status = game_over
- [x] T026 [US3] Add integration test `tests/integration/test_timer_and_score_display.py` for timer countdown and end condition

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T027 [P] Add robust input edge-case handling: ignore reverse direction command (snake cannot reverse into itself) in `src/input_handler.py`
- [x] T028 [P] Add configuration options in `src/config.py` for board size and snake speed
- [x] T029 [P] Add logging and observability in `src/logger.py` (clock ticks, apple eaten, collisions, game over)
- [x] T030 [P] Add smoke integration test `tests/integration/test_full_round_end_to-end.py` for full 60-second round (or artificial tick fast-forward)
- [x] T031 [P] Update docs in `specs/001-three-snake-game/quickstart.md` with run instructions for implemented codebase
- [x] T032 [P] Create a short video demo script/recording instructions in `specs/001-three-snake-game/quickstart.md`
- [x] T034 [P] Add CI quality gate: include `pytest` command and a test suite runner in `ci/` or script with pass/fail status
- [x] T035 [P] Add contract tests in `tests/integration/test_game_state_contract.py` using the definitions from `specs/001-three-snake-game/contracts/game-state-contract.md`
- [x] T036 [P] Implement simultaneous collision resolution in `src/collision.py` and `src/game_rules.py` using priority order (human, ai_1, ai_2) for deterministic behavior

---

## Dependencies Graph (by story order)

1. Foundational tasks T006-T012 must complete before story implementations begin.
2. User Story 1 tasks (T013-T017) are MVP and the first delivery item.
3. User Story 2 tasks (T018-T022) depend on foundational tasks and optionally Story 1.
4. User Story 3 tasks (T023-T026) depend on foundational tasks and at least partial Story 1+2.
5. Polish tasks (T027-T032) can run in parallel after stories are functional.

## Parallel Execution Examples

- T007, T008, T009, T010, T011 can be worked on in parallel (different modules, shared interface stable).
- T013 and T018 are independent of each other once foundations are ready, so engineering can split into two threads (human+AI).
- T023 and T024 are UI-focused and can proceed together after game loop and model are implemented.

## Implementation Strategy

1. MVP: get one snake controlled, apple spawning, eating, and basic collision/lives working (US1).
2. Add AI (US2) with nearest-apple and avoidance rules; create deterministic tests.
3. Add full UI/UX state and timer (US3); solidify game-end behavior.
4. Polish by adding configuration, logging, and thorough end-to-end tests.

## Validation for Checklist Format

- All tasks include `- [ ]`, sequential IDs, and explicit file paths.
- Story tasks have `[US1]`, `[US2]`, `[US3]` labels as required.
- Setup/foundation/polish tasks omit story labels and are grouped by phase.
