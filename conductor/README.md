# Conductor

Conductor owns the workflow pipeline, planning artifacts, control-doc hierarchy, and execution context for this project.

---

## The Canonical Workflow

```
Master Plan
    ↓
Slice specs (full index for known scope / per-PR for iterative)
    ↓
Agent runs
    ↓
Handoff with Exact Next Steps
    ↓
    ├── Known scope   → advance index pointer → agent runs next spec
    └── Iterative     → Exact Next Steps guide operator to write next spec → agent runs
```

### Step 1 — Master Plan

The operator writes `conductor/master-plan-*.md` before any agent runs. It defines:

- Full project objective and what "done" looks like
- All phases and the slice breakdown for each
- Architecture decisions and constraints
- Cross-repo dependencies (if any)

The master plan is the constant. Every agent session reads the relevant section so it knows where the current slice sits in the full arc. Without it, agents propose next steps blind. With it, every handoff is grounded.

### Step 2 — Slice Specs

The operator writes slice specs from the master plan. Two patterns:

**Full index** — write all specs upfront in one commit. Use when scope is fully known.
`conductor/index.md` becomes a queue. Agent advances the pointer after each slice.

```
## Queue
- [STABLE] conductor/slice-01-*.md
- [ACTIVE] conductor/slice-02-*.md
- [QUEUED] conductor/slice-03-*.md
```

**Per-PR / iterative** — write one spec at a time, merge it, agent runs it. Use when scope
emerges from what the agent finds. The agent's "Exact Next Steps" guide the operator in
writing the next spec. The operator adds judgment; the agent provides the raw material.

Both patterns use the same slice format. The difference is how many specs exist before
the agent starts running.

### Step 3 — Agent Execution

Agent reads `conductor/index.md` → finds active slice → executes → at the end of each slice:

1. Marks current slice `status: stable` in the slice doc
2. Advances `conductor/index.md` active pointer to next queued slice
3. Writes handoff with **Exact Next Steps** — specific enough to promote directly to a spec
4. Commits all three together

### Step 4 — Handoff and Continuation

The handoff's **Exact Next Steps** bridge the two modes:

- **Known scope**: operator reviews, approves, next agent run picks up from updated index
- **Iterative**: operator uses steps to write the next slice spec, merges it, agent runs

"Exact Next Steps" are not vague proposals. They are concrete enough that the operator's
job is review and format, not generation. The master plan is what makes this possible —
the agent knows what comes after the current slice.

---

## What Lives Here

- `index.md` — machine-first routing, active slice pointer, queue
- `README.md` — workflow contract (this file)
- `AGENTS.md` — agent behavioral rules (rename to `CLAUDE.md` or `GEMINI.md` for your CLI)
- `CONDUCTOR_MODES.md` — execution-mode contract: Patch, Slice, Full Conductor, Audit
- `master-plan-*.md` — full project scope and slice breakdown (operator-authored)
- `tracks.md` — active initiative registry and cross-repo dependencies
- `slice-*.md` — active execution artifacts (one per commit/PR-sized unit of work)
- `handoff-log.md` — current-state handoff only
- `handoff-archive.md` — historical handoff entries (not in the hot read path)
- `archive/` — completed workflow docs after their stable checkpoint

---

## Naming And Placement

- Active slice routing stays at `conductor/index.md`.
- Active workflow docs stay at `conductor/slice-*.md`.
- Completed slices move to `conductor/archive/` after the stable checkpoint is cut.
- `handoff-log.md` holds only the current active handoff block; older entries move to `handoff-archive.md`.

---

## Lifecycle Model

- Active in-flight slice docs remain in `conductor/` until manually moved to archive.
- Completed slices move to `conductor/archive/` after the stable checkpoint is cut.
- `handoff-log.md` is the active handoff surface only; older entries move to `handoff-archive.md`.
- Master plan docs remain active until the full objective is met; then archive.
