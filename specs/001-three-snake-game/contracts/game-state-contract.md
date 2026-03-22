# Game State Contract

This contract defines the runtime state and external event expectations for the three-snake game.

## GameState

- field: { width: int, height: int, wrap: true }
- snakes: [
  {id: str, is_human: bool, segments: [{x:int,y:int}], direction: "up"|"down"|"left"|"right", lives: int, score: int}
  ]
- apples: [{id: str, position: {x:int, y:int}}]
- timer: {remaining_seconds: int}
- status: "running"|"game_over"

## Input Events

- `move_human(direction)` => direction in ["up","down","left","right"]
- `tick(dt)` => updates timer and state (dt in seconds)

## Output Events

- `apple_eaten(snake_id, apple_id)`
- `snake_hit(victim_id, attacker_id, hit_type)` where hit_type is "body" or "head"
- `snake_dead(snake_id)`
- `game_over(result)` where result includes final scores

## Invariants

- Exactly 3 snakes at start.
- 5 apples at all times while status is `running`.
- No apple shares position with any snake segment.
- All snakes have lives in range [0,3].
- Snake length is >=1 (head must exist).
