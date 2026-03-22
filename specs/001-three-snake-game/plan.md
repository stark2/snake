# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Three-Snake Snake is a 60-second competitive arcade game where 3 snakes share a wrap-around grid. One snake is human-controlled (arrow keys/WASD); two are AI. Five apples are always present, respawning immediately on consumption. Snakes grow by one segment per apple, have three lives, and lose segments/lives when hit by other snakes (body-body or head collisions). The game ends at timeout or when every snake is dead, then displays final scores.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12 (Pygame 2.6)  
**Primary Dependencies**: Pygame (desktop prototype)  
**Storage**: N/A (in-memory runtime state)  
**Testing**: pytest + Pygame unit tests. Add scenario simulation tests for collision rules and score tracking.  
**Target Platform**: Desktop (Windows/macOS/Linux)  
**Project Type**: Game prototype / single-player local multiplayer
**Performance Goals**: 60 FPS stable on target environment;
**Constraints**: 60-second round, fixed 5 apples, exactly 3 snakes; no pause or restart mid-round;
**Scale/Scope**: one game mode, single round, one human player + 2 AI players

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Constitution present at `.specify/memory/constitution.md` with game development principles.
- Principles checked: Player-Centric Design, Performance Optimization, Modular Architecture, Comprehensive Testing, Cross-Platform Compatibility.
- No violations identified for a simple game prototype.

**Pass**.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: Single project game prototype.

- `src/` for Pygame implementation (or `godot/` for Godot project if chosen)
- `tests/unit/` and `tests/integration/` for behavior and play loop tests
- `specs/001-three-snake-game/` for all design artifacts


## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
