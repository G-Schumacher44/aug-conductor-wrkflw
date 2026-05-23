# Slice 05: Routine Maintenance

Date: 2026-05-23
Status: active
Type: workflow-slice-maintenance

## Objective

Run a routine Conductor health check on this project. Validate the spine,
verify all planned work is complete, surface any open blockers, and write
a maintenance status entry to the handoff log.

This slice is designed for automated execution — a cron job fires the agent
with no human present. The agent orients from the spine alone.

## Steps

1. Run `python scripts/validate.py` from the repo root — capture full output
2. Read `conductor/index.md` — verify all slices show STABLE (no stuck ACTIVE)
3. Read `conductor/handoff-log.md` — count open Blockers in the most recent entry
4. Write a maintenance entry to `conductor/handoff-log.md` (see format below)
5. Move the previous handoff entry to `conductor/handoff-archive.md`
6. Commit: `chore(maintenance): conductor health check YYYY-MM-DD`

## Maintenance Entry Format

```
## Maintenance Check — YYYY-MM-DD

Date: <today>
Commit: <7-char hash>
Type: automated-maintenance

### Status
<clean | degraded>

### Validation
- scripts/validate.py: <X passed | Y warnings | Z failed>
<list any specific failures verbatim>

### Queue State
- Slices: <N> total — <N> STABLE
<list any non-STABLE slices, or "All slices STABLE">

### Open Blockers
- <count> open blockers from last handoff
<list each verbatim, or "None">

### Next Run
Cron-driven — operator sets schedule. No action required.
```

**Status:** `clean` = 0 failures + all slices STABLE + 0 blockers. `degraded` = anything else.

## Acceptance Criteria

- [ ] scripts/validate.py run and output captured
- [ ] Queue state verified (all slices checked)
- [ ] Blockers counted and listed
- [ ] Maintenance entry written to handoff-log.md
- [ ] Previous handoff entry moved to handoff-archive.md
- [ ] Committed with chore(maintenance): prefix
- [ ] No code changes made (read-and-report only)
- [ ] No auto-fixes attempted — failures documented only
