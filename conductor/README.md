# Conductor

Conductor owns the workflow pipeline, planning artifacts, control-doc hierarchy, and execution context for this project.

## What Lives Here

- `index.md` — machine-first routing entry for context-pack and workflow discovery
- `README.md` — directory conventions, lifecycle model, and archive policy
- `AGENTS.md` — local workflow rules for Conductor (rename to `CLAUDE.md` or `GEMINI.md` for your CLI)
- `CONDUCTOR_MODES.md` — execution-mode contract for Patch, Slice, Full Conductor, and Audit work
- `tracks.md` — active initiative registry
- `slice-*.md` — active commit/PR-sized execution artifacts
- `handoff-log.md` — current-state handoff only
- `handoff-archive.md` — historical handoff entries (not in the hot read path)
- `archive/` — completed workflow docs after their stable checkpoint

## Naming And Placement

- Machine-first routing stays at `conductor/index.md`.
- Active workflow docs stay at `conductor/slice-*.md`.
- Completed slices move to `conductor/archive/` after the stable checkpoint is cut.
- `handoff-log.md` holds only the current active handoff block; older entries move to `handoff-archive.md`.

## Spec Package Pattern

- The active `slice-*.md` file is the implementation contract for the current commit/PR-sized chunk.
- When a template field is missing and needed for safe execution, extend the template and treat the new field as canonical going forward.
- `README.md` is the human-facing contract; `index.md` is the machine-facing router.
- `index.md`, `tracks.md`, and `handoff-log.md` should stay current-state only; move history elsewhere.

## Lifecycle Model

- Active in-flight slice docs remain in `conductor/` until they are manually moved to archive.
- Completed slices move to `conductor/archive/` after the stable checkpoint is cut.
- `handoff-log.md` is the active handoff surface only; older entries move to `handoff-archive.md`.
