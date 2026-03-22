# Data Model: Three-Snake Game

## Entities

- Snake
  - id: string ("human", "ai_1", "ai_2")
  - segments: list of coordinates [(x, y)] with head first
  - direction: vector or enum (up/down/left/right)
  - lives: integer (0..3)
  - score: integer (apples eaten)
  - is_human: boolean

- Apple
  - id: string
  - position: coordinate (x, y)

- GameField
  - width: integer
  - height: integer
  - wrap: boolean (true)
  - apple_count: integer (5)

- Timer
  - remaining_seconds: integer (0..60)

## Relationships

- Snake eats Apple: increments Snake.score, grows Snake.segments, triggers Apple respawn.
- Snake collisions: Snake A head intersects Snake B segment => Snake B loses segments/lives based on hit.
- Game end conditions: Timer expiration OR all snakes lives == 0.

## Validation rules

- Apple position must not overlap any snake segment at spawn.
- At game start, exactly 3 snakes exist and 5 apples exist.
- Snake length increments by one per apple eaten.
- Snake lives decrement by 1 when hit, and snake is removed at 0 lives.

## States

- `running`: normal game tick updates
- `game_over`: timer == 0 OR all snakes dead
- `pausing`: not supported for this mode (immutable requirement)
