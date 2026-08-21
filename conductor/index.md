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

1. Tick every satisfied acceptance-criteria checkbox in the slice doc, then run the
   validator gate (`scripts/validate.py`) and fix any failures
2. Mark completed slice `status: stable` in its slice doc
3. Update queue table (ACTIVE → STABLE). Leave the next slice `QUEUED` — don't flip it
   to `ACTIVE` until a session actually starts it
4. Update `Active slice:` line to `none — awaiting slice-NN`
5. Commit slice doc + index.md + handoff-log.md together

## Reference

- [Handoff Log](./handoff-log.md)
