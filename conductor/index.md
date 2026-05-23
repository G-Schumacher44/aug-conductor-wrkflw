# Conductor Index

Status: active
Type: conductor-index

Machine-first routing entry for Conductor-aware agents.

---

## Context Pack

- [Project Intent](../intent.md)
- [Master Plan Template](./master-plan-template.md)
- [Agent Rules](../AGENTS.md)
- [Conductor Modes](./CONDUCTOR_MODES.md)
- [Track Registry](./tracks.md)

---

## Active Strategy

**Active Slice:** [Slice 01: Initial Project Bootstrap](./slice-01-initial-bootstrap.md)

### Queue

| Status | Slice |
|---|---|
| ACTIVE | [slice-01-initial-bootstrap.md](./slice-01-initial-bootstrap.md) |

> This is the outer demo repo's Conductor index — it routes the agent to the bootstrap
> slice which scaffolds `project/` as a standalone Conductor project.
> Once `project/` is scaffolded, execution continues from `project/conductor/index.md`.

---

## Queue Format (for reference)

When running a full-index workflow, update this table as slices complete:

```
| STABLE | slice-01-*.md |
| ACTIVE | slice-02-*.md |
| QUEUED | slice-03-*.md |
```

Agent end-of-slice responsibilities:
1. Mark current slice `status: stable` in the slice doc
2. Update this table (ACTIVE → STABLE, next QUEUED → ACTIVE)
3. Commit slice doc + index.md + handoff-log.md together

---

## Reference

- [Handoff Log](./handoff-log.md)
- [Workflow Pattern](./README.md)
