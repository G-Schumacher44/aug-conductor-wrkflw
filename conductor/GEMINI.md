# GEMINI agent guide — Conductor

## What This Directory Is

The workflow engine for this project. Conductor owns the technical roadmap, execution slices, lifecycle conventions, and durable planning context.

## Read This First

Before planning or implementing, read in order:

1. `README.md`
2. `conductor/index.md`
3. `conductor/CONDUCTOR_MODES.md`
4. `conductor/README.md`
5. `conductor/GEMINI.md`
6. `conductor/tracks.md`
7. the active `conductor/slice-*.md` file
8. `conductor/handoff-log.md` when resuming active work

Use `docs/` (or `demo/`) for project-specific context: schema references, intent docs, and domain background.

Do not start from `archive/` or `handoff-archive.md` unless the active slice explicitly sends you there.

## Authority Order

1. `AGENTS.md`
2. root `GEMINI.md` / `CLAUDE.md`
3. `conductor/GEMINI.md`
4. `conductor/index.md`
5. `conductor/README.md`
6. active Conductor workflow docs

## Locked Contract

- **Conductor Owns Workflow:** scope, gates, dependency mapping, and definition of done live here.
- **Slices Are Execution Artifacts:** each active slice must be small enough to land as a bounded commit or PR sequence.
- **Modes Bound Context:** choose Patch, Slice, Full Conductor, or Audit Mode from `CONDUCTOR_MODES.md` before reading broadly.

## Workflow Rules

When creating or updating a slice:

1. anchor it to the current track in `tracks.md`
2. spell out exact writable surfaces and scope boundaries
3. include validation gates and the smallest sufficient verification steps
4. call out explicit out-of-scope items
5. declare `conductor_mode`, handoff posture, and tag posture
6. update `conductor/tracks.md` if the active initiative registry changes

When closing a slice:

1. update `handoff-log.md` with objective, current state, files changed, and exact next steps
2. move older handoff entries to `handoff-archive.md` so `handoff-log.md` stays current-state only
3. move the slice to `archive/` after the stable checkpoint is cut

## Git Discipline

- `main` branch is the stable baseline.
- Branch from `main` for a specific slice or session.
- Make scoped, focused commits within that slice.
- Merge feature branches back to `main` via Pull Request when stable.
