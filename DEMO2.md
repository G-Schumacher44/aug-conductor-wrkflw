# Run Demo 2 — Iterative Feature Work + Live Spec Authoring

You are an agent working with the operator in a live pair programming session.
`project/` is an established LookML project (3 slices stable). A new BigQuery table
`your-gcp-project.gold_marts.fct_promotions` has been provisioned.

This demo runs in two phases. Phase 1 is autonomous execution. Phase 2 is collaborative.

---

## Phase 1 — Execute Slice 04 (autonomous)

### 1 — Orient from the Conductor spine

Read in order:

1. `project/AGENTS.md`
2. `project/intent.md`
3. `project/conductor/index.md` — active slice is slice-04
4. `project/conductor/handoff-log.md` — state from last agent
5. `project/conductor/slice-04-promotions-view.md` — your task

### 2 — Create your branch

```bash
git checkout -b feat/slice-04-promotions-view
```

### 3 — Generate the view

Read `demo/schema/gold_marts.md` — find `fct_promotions`. Do not invent columns.

Create `project/views/fct_promotions.view.lkml`:
- One dimension per column (STRING→string, INTEGER/FLOAT→number, DATE→date)
- One measure: `count { type: count }` — only measure for this slice
- `sql_table_name: \`your-gcp-project.gold_marts.fct_promotions\``

Commit: `feat(views): add fct_promotions view`

### 4 — Update the model

Add to `project/models/gold_marts.model.lkml`:

```lookml
explore: fct_promotions {}
```

Commit: `feat(model): add fct_promotions explore`

### 5 — Validate

```bash
python3 scripts/validate.py
```

Fix any failures before proceeding.

### 6 — Write the slice-04 handoff

Mark `slice-04-promotions-view.md` `status: stable`.
Advance `conductor/index.md` — slice-04 ACTIVE → STABLE, set `Active slice: none — awaiting slice-05`.
Move current handoff entry to `conductor/handoff-archive.md`.

Write entry at the top of `conductor/handoff-log.md`:

```
## Slice 04 — Promotions View

Date: <today>
Commit: <7-char hash>

### Objective
Add fct_promotions baseline view and explore to the established gold_marts project.

### Current State
- views/fct_promotions.view.lkml — 11 dimensions, count measure
- models/gold_marts.model.lkml — 9 explores

### Files Changed
- views/fct_promotions.view.lkml (new)
- models/gold_marts.model.lkml (updated)
- conductor/slice-04-promotions-view.md (stable)
- conductor/index.md (slice-04 stable, awaiting slice-05)

### Validation
- python3 scripts/validate.py: <X passed | Y warnings | 0 failed>

### Exact Next Steps
1. Enrich fct_promotions: sum for revenue_attributed and cost, average for roas
2. Add dimension_group for start_date and end_date with date/week/month/quarter/year timeframes
3. Add value_format_name: usd for revenue/cost, decimal_2 for roas
4. Add group_label to organize dimensions in the field picker
5. Hide promotion_id — primary key, not useful in the field picker

### Blockers
- None
```

Commit: `docs(handoff): record slice 04 completion`

---

## Phase 2 — Build and Execute Slice 05 (collaborative)

**Do not start this phase until Phase 1 is committed and the operator has reviewed the handoff.**

### 7 — Propose slice-05

Read the Exact Next Steps from the handoff you just wrote.
Draft `project/conductor/slice-05-promotions-enrichment.md` based on those steps.

The slice spec should follow the standard format:
- Objective
- Required Reads
- Execution Steps (numbered, specific)
- Acceptance Criteria (checkboxes)

Add it to `conductor/index.md`:
- New row: `| ACTIVE | conductor/slice-05-promotions-enrichment.md |`
- Update `Active slice:` line to `conductor/slice-05-promotions-enrichment.md`

Commit the draft: `spec(conductor): draft slice-05 promotions enrichment`

**Stop here. Present the draft to the operator.**
The operator will review the slice spec in the IDE, adjust scope or wording, and say "go."

### 8 — Execute slice-05

After operator approval, execute slice-05 exactly as specified.

Apply to `project/views/fct_promotions.view.lkml`:
- Typed measures for numeric fields
- dimension_group for date fields
- value_format_name on financial measures
- group_label on key dimensions
- hidden: yes on promotion_id

Run `python3 scripts/validate.py` — fix any failures.

Mark slice-05 stable, advance the queue, write the handoff with Exact Next Steps.

Commit: `docs(handoff): record slice 05 completion`

---

## Rules

- Use only columns from `demo/schema/gold_marts.md`
- No hardcoded credentials
- Commit as you go
- Slice-05 spec is written by you and reviewed by the operator — it is the contract

---

## What This Demo Shows

```
Autonomous execution (slice-04)
    → handoff with Exact Next Steps
    → agent proposes next spec (slice-05)
    → operator reviews diff, adjusts, approves
    → agent executes
    → loop closes
```

The spec is the contract. The review gate is where judgment lives.
