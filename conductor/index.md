# Conductor Index

Status: stable
Type: conductor-index

## Active Slice

Active slice: none — all slices stable

## Queue

| Status | Slice |
|---|---|
| STABLE | conductor/slice-01-initial-bootstrap.md |

## Required Reads

- [Master Plan Template](./master-plan-template.md)
- [Agent Rules](./AGENTS.md)
- [Conductor Modes](./CONDUCTOR_MODES.md)
- [Track Registry](./tracks.md)
- [Workflow Pattern](./README.md)

## Agent — end-of-slice responsibilities

1. Write the handoff entry (top of `conductor/handoff-log.md`)
2. Tick every satisfied acceptance-criteria checkbox in the slice doc — including
   "Handoff written", now that step 1 is done — then run the validator gate
   (`scripts/validate.py`) while the slice is still `ACTIVE`, and fix any failures
3. Mark completed slice `status: stable` in its slice doc
4. Update queue table (ACTIVE → STABLE). Leave the next slice `QUEUED` — don't flip it
   to `ACTIVE` until a session actually starts it
5. Update `Active slice:` line to `none — awaiting slice-NN`
6. Commit slice doc + index.md + handoff-log.md together

## Reference

- [Handoff Log](./handoff-log.md)
