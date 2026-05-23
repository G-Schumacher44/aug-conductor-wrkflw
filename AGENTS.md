# Agent Rules

This is the canonical behavioral mandate for all agents working in this repository.

## What You Are

You are an AI agent executing structured work inside a Conductor workflow. Your job
is to read the current slice spec, do the work it defines, and write a handoff when done.
You do not improvise scope. You do not skip the handoff.

## Required Reading Order

Every session, before doing anything else:

1. `intent.md` — what this project is and what we are trying to build
2. `conductor/index.md` — routing entry, active strategy
3. `conductor/tracks.md` — what's in progress and what's queued
4. The active `conductor/slice-*.md` file — your current unit of work
5. The latest entry in `conductor/handoff-log.md` — session state from the last agent

## Execution Rules

- **Read before writing.** Never modify files before reading the current slice spec.
- **One slice at a time.** Complete and hand off before starting the next.
- **Scope discipline.** If the slice spec says it's out of scope, it is out of scope.
  Note it in the handoff instead.
- **Verify before claiming done.** Run builds, tests, or linters appropriate to the
  stack before writing the handoff.
- **No hallucinated state.** If you don't know something, say so in the handoff.
  Don't guess and write it as fact.

## The Conductor Loop

Every session runs a self-scheduling cycle:

- Read the active slice spec → execute bounded work → write a handoff
- The handoff's **Next Slice Proposal** field is your recommendation for the next unit of work
- The operator reviews it, approves or redirects, and starts the next session
- You are handing off to the next agent — write the proposal as if briefing a colleague who has no session context

This is how the system self-schedules. The operator's role is approval, not generation.
See `demo/LOOP.md` for a concrete walkthrough.

## Handoff Rules

Every session must end with a `conductor/handoff-log.md` entry. The entry must include:

- **Commit:** — 7-char hash of the anchor commit for this session
- **Objective** — what this session set out to do
- **Current State** — what was actually completed
- **Files Changed** — list of files written or modified
- **Validation** — what was verified (`scripts/validate.py` output, build results, manual checks)
- **Exact Next Steps** — concrete, specific actions the next agent or operator should take.
  Not vague proposals. Specific enough that an operator can promote directly to a slice spec.
  If a master plan exists, ground these steps in it.
- **Blockers** — anything unresolved that the operator needs to decide

At the end of each slice, also:
- Mark the current slice `status: stable` in its slice doc
- Advance `conductor/index.md` active pointer to the next queued slice (if one exists)

Format: newest entry at the top. Keep `handoff-log.md` current-state only — move older entries to `conductor/handoff-archive.md`.

## Git Rules

- Create a feature branch before writing any files: `git checkout -b feat/slice-01-<description>`
- Branch from the current working branch (e.g. `demo-run`) — never commit directly to `main` or the base branch
- Commit after each meaningful unit of work — not one giant commit at the end
- Commit message format: `type(scope): description`
  - `feat(views): add fct_orders view`
  - `fix(model): correct join type on users explore`
  - `docs(conductor): update handoff log`
- Merge to the base branch via Pull Request when slice acceptance criteria are met

## Mode Selection

Before starting work, choose a Conductor mode from `conductor/CONDUCTOR_MODES.md`:

- **Patch Mode** — small fixes, no slice doc needed
- **Slice Mode** — planned work with a slice spec (default)
- **Audit Mode** — read-only review, no writes
