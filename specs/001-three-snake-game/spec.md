# Feature Specification: Three-Snake Game

**Feature Branch**: `001-three-snake-game`  
**Created**: 2026-03-22  
**Status**: Draft  
**Input**: User description: "Create a "three‑snake" version of the classic Snake game. - Overview: The game takes place on a rectangular playfield with no wall collisions (snakes wrap around edges). Three snakes are present at all times. Two of them are computer‑controlled; one is controlled by a human player via arrow keys or WASD. The objective is to eat as many apples as possible within a 60‑second round. - Apples: Five apples are on the field at any moment. Each apple spawns at a random unoccupied position. When a snake eats an apple, that apple disappears and immediately respawns at another random position on the field. Apples do not have a limit on respawns within the one‑minute game duration. - Snakes: Each snake starts with a head and two body segments. Eating an apple increases that snake’s length by one segment. Each snake has three lives. A life is lost when another snake collides with any part of it.   * Collision rules: If a snake is hit on a body segment (another snake’s head or body runs into it), it loses as many segments as were hit. If a snake’s head is hit, only the head remains (all body segments are removed). When a snake’s lives reach zero, it disappears from the field and stops playing.   * AI behaviour: The two computer‑controlled snakes autonomously navigate toward nearby apples while avoiding collisions where possible. - Scorekeeping: Each snake has an individual score counter showing how many apples it has eaten. The scores for all three snakes are displayed simultaneously (for example in separate corners of the screen). - Timer: A visible countdown timer appears in the bottom right corner of the screen. The round lasts exactly 60 seconds. The game ends when the timer reaches zero or all snakes have lost their lives. - Controls: The human player steers their snake using the arrow keys or WASD keys. There is no pause or restart within the one‑minute round. - Win condition: At the end of the timer, or when all snakes are dead, the game displays the scores of each snake. There is no explicit winner/loser logic—players simply compare apple counts. Ensure these mechanics are reflected clearly in the specification. Use the specification to drive subsequent planning, task decomposition and implementation steps."

## Clarifications

### Session 2026-03-22

- Q: AI apple-selection strategy for autonomous snakes → A: Nearest apple (prioritize closest apple for efficient pathfinding and competitive gameplay)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Play as Human Snake (Priority: P1)

As a human player, I want to control my snake using keyboard inputs to eat apples and avoid collisions, so that I can compete with AI snakes for the highest score within the 60-second round.

**Why this priority**: This is the core gameplay experience that delivers the primary value of the game - interactive snake control and competition.

**Independent Test**: Can be fully tested by launching the game, controlling the human snake with arrow keys or WASD, eating apples, and observing score increases, all while AI snakes operate autonomously.

**Acceptance Scenarios**:

1. **Given** the game is started, **When** I press arrow keys or WASD, **Then** the human snake changes direction accordingly
2. **Given** the human snake's head reaches an apple position, **When** the game updates, **Then** the apple disappears, snake length increases by one, score increments, and a new apple spawns
3. **Given** the human snake collides with another snake's body, **When** the collision occurs, **Then** the human snake loses segments equal to the collision point and loses a life if applicable

---

### User Story 2 - AI Snake Behavior (Priority: P2)

As a player observing the game, I want AI snakes to autonomously navigate toward apples and avoid collisions, so that they provide competitive gameplay without requiring additional human input.

**Why this priority**: AI behavior enables the multi-snake gameplay concept and ensures the game remains engaging even without multiple human players.

**Independent Test**: Can be fully tested by running the game and observing AI snakes move toward apples, eat them, grow, and attempt to avoid collisions with other snakes.

**Acceptance Scenarios**:

1. **Given** an AI snake exists on the field, **When** apples are present, **Then** the AI snake moves toward the nearest apple
2. **Given** an AI snake's head reaches an apple, **When** the game updates, **Then** the apple disappears, AI snake length increases, score increments, and a new apple spawns
3. **Given** an AI snake detects potential collision, **When** possible, **Then** the AI changes direction to avoid the collision
4. **Given** no safe avoidance direction exists, **When** collision is imminent, **Then** the AI maintains its current axis and accepts result (for deterministic behavior)

### Edge Cases

- What happens when all snakes collide simultaneously? (Use resolution order: human, ai_1, ai_2)
- How does the game handle edge wrapping when a snake moves off-screen? (Wrap to opposite edge)
- What occurs when multiple snakes target the same apple? (Consumption priority: human, ai_1, ai_2)
- How are collisions resolved when snakes move into the same position simultaneously? (Evaluate in priority order: human action first, then ai_1, then ai_2)
- What happens if all apples are eaten before respawning? (New apples spawn immediately at unoccupied positions)

---

### User Story 3 - Game State Display and Timing (Priority: P3)

As a player, I want to see real-time scores for all snakes and a countdown timer, so that I can track progress and know when the round ends.

**Why this priority**: Score and timer display provide essential feedback for gameplay and clearly communicate game state.

**Independent Test**: Can be fully tested by starting the game and verifying that scores update when snakes eat apples, timer counts down from 60 seconds, and game ends when timer reaches zero.

**Acceptance Scenarios**:

1. **Given** a snake eats an apple, **When** the score updates, **Then** the corresponding snake's score display increments by one
2. **Given** the game starts, **When** time passes, **Then** the timer displays decreasing seconds from 60
3. **Given** the timer reaches zero, **When** the round ends, **Then** final scores for all snakes are displayed

### Edge Cases

- What happens when all snakes collide simultaneously?
- How does the game handle edge wrapping when a snake moves off-screen?
- What occurs when multiple snakes target the same apple?
- How are collisions resolved when snakes move into the same position simultaneously?
- What happens if all apples are eaten before respawning?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a rectangular playfield where snakes can move without wall collisions, wrapping around edges instead
- **FR-002**: System MUST maintain exactly three snakes at game start: one human-controlled and two AI-controlled
- **FR-003**: System MUST spawn and maintain exactly five apples on the field at all times, respawning immediately when eaten
- **FR-004**: System MUST allow human player to control their snake using arrow keys or WASD keys
- **FR-005**: System MUST implement AI behavior for computer-controlled snakes to navigate toward apples while avoiding collisions
- **FR-006**: System MUST increase snake length by one segment when eating an apple
- **FR-007**: System MUST implement collision detection where snakes lose segments or lives when hit by other snakes
- **FR-008**: System MUST track and display individual scores for each snake based on apples eaten
- **FR-009**: System MUST display a countdown timer starting at 60 seconds
- **FR-010**: System MUST end the game when timer reaches zero or all snakes lose their lives
- **FR-011**: System MUST display final scores when the game ends

### Key Entities *(include if feature involves data)*

- **Snake**: Represents a game entity with position, direction, segments, lives, and score; can be human or AI controlled
- **Apple**: Represents food items with random spawn positions on the playfield
- **Game Field**: Represents the rectangular play area with wrap-around boundaries
- **Score**: Tracks apples eaten for each snake
- **Timer**: Counts down from 60 seconds to control game duration

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Game runs for exactly 60 seconds from start to end
- **SC-002**: All three snakes move simultaneously and respond to controls/collisions within each game tick
- **SC-003**: Apples maintain count of five throughout gameplay, respawning immediately when eaten
- **SC-004**: Snake lengths increase correctly upon eating apples, with proper collision segment loss
- **SC-005**: Scores accurately reflect apples eaten for each snake
- **SC-006**: Game ends appropriately when timer expires or all snakes are eliminated
