# Research: Three-Snake Game

## Decision: Game engine / implementation stack

- Selected prototype target: Python + Pygame for quickest iteration, cross-platform desktop proof of concept.
- Alternative: Godot + GDScript for engine features, GUI, and exports; chosen in case of larger scope.

## Decision: Apple spawn and collision rules

- Apples: 5 active at all times, immediate respawn in random unoccupied location.
- Collision: hit-body reduces impacted snake by hit segments; hit-head resets snake to head-only.
- Lives: each snake begins with 3 lives and is removed when lives hit 0.

## Decision: AI behavior

- AI chooses nearest apple using Manhattan distance and uses simple greedy pathfinding.
- On potential collision, AI attempts perpendicular moves before forced approach.
- If multiple snakes target same apple simultaneously, consumption priority is: human → ai_1 → ai_2.

## Decision: Score and UI

- Separate score display for each snake (top corners or sides).
- Bottom-right countdown timer (60 sec), plus game over scoreboard overlay.

## Alternatives considered

- Weighted apple preference based on current length or score difference
- Full A* pathfinding across moving obstacles (higher complexity) vs greedy steer (lower complexity)

## Rationale

- Keep rules aligned with provided feature requirements.
- Emphasize deterministic core behavior to enable stable testing and incremental AI improvement.
