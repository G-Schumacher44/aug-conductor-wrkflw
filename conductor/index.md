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

1. Mark completed slice `status: stable` in its slice doc
2. Update queue table (ACTIVE → STABLE, next QUEUED → ACTIVE)
3. Update `Active slice:` line to point to next slice
4. Commit slice doc + index.md + handoff-log.md together

## Reference

- [Handoff Log](./handoff-log.md)
