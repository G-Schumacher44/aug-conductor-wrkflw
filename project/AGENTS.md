# Agent Rules — LookML Project

You are an AI agent executing structured work inside a Conductor workflow.
Read the slice spec, do the work, write the handoff.

## The Conductor Loop

- Read active slice spec → execute bounded work → write handoff
- The handoff's **Exact Next Steps** field is your recommendation for the next unit of work
- Operator reviews, approves or redirects, starts next session

## Required Reading Order

1. `intent.md` — project description and BQ context
2. `conductor/index.md` — active slice routing
3. The active `conductor/slice-*.md` — current unit of work
4. Latest entry in `conductor/handoff-log.md` — state from last agent

## Execution Rules

- Read before writing. Read the slice spec before touching any files.
- One slice at a time. Complete and hand off before starting the next.
- Scope discipline. If the slice says it's out of scope, note it in the handoff.
- No invented columns. Only use what is in the schema reference.

## Handoff Rules

Every session ends with a `conductor/handoff-log.md` entry containing:

- **Commit:** — 7-char hash
- **Objective** — what this session set out to do
- **Current State** — what was actually completed
- **Files Changed** — list of written or modified files
- **Validation** — what was verified
- **Exact Next Steps** — what the next agent should do (the scheduling mechanism)
- **Blockers** — unresolved items for operator

Newest entry at top. Move older entries to `conductor/handoff-archive.md`.

## Git Rules

- Create a feature branch: `git checkout -b feat/slice-<N>-<description>`
- Branch from the current working branch — never commit to `main` directly
- Commit after each meaningful unit of work
- Format: `type(scope): description`
