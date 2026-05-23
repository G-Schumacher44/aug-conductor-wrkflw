# Conductor Agent Starter Prompt

## How To Start A Session

1. Run: `git status -sb && git log -n 5 --oneline && cat conductor/handoff-log.md`
2. Read the required docs in order from `conductor/GEMINI.md`
3. Select a mode from `conductor/CONDUCTOR_MODES.md`
4. Read the active `conductor/slice-*.md` before implementing anything

## Mode Selection

| Mode | When To Use |
|---|---|
| Patch | single-file fix, typo, config tweak |
| Slice | bounded feature — one commit or PR sequence |
| Full Conductor | multi-track initiative requiring master plan |
| Audit | read-only review, no writes |

## Final Report Before You Stop

Report:
- branch name
- commits made
- exact files added/changed
- what was built
- what remains stubbed or intentionally deferred
- verification performed
- PR link if opened

## Handoff Rules

- Every session that changes files must update `conductor/handoff-log.md`.
- Every handoff entry must include a `Commit:` field pointing to its anchor hash.
- Keep `handoff-log.md` to the current block only; move older entries to `handoff-archive.md`.
- If work is incomplete, state exactly what is blocked, what was verified, and what remains.
