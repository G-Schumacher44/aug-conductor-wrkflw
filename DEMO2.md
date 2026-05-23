# Run Demo 2 — Iterative Feature Work

You are an agent working with the operator in an active pair programming session.
`project/` is an established LookML project. A new business requirement has arrived:
the data team has provisioned `gcs-automation-project.gold_marts.fct_promotions`.

This demo runs in two phases with a human review gate between them.

---

## Phase 1 — Orient and Present the Plan

**Do not execute any work yet.** Read the project state and present what you're about to do.

### 1 — Orient from the Conductor spine

Read in order:

1. `project/AGENTS.md` — behavioral rules
2. `project/intent.md` — project description and BQ context
3. `project/conductor/index.md` — current queue state
4. `project/conductor/handoff-log.md` — what the last agent left, including Exact Next Steps
5. `project/conductor/slice-04-promotions-view.md` — the active slice spec

### 2 — Present the plan to the operator

After reading, summarize out loud:

- What the last agent completed (from the handoff)
- What slice-04 will do and why (derived from the Exact Next Steps in the handoff)
- What files will be created or changed
- What the validator will check

**Stop here. Wait for the operator to review `slice-04-promotions-view.md` and confirm
or adjust the scope before executing.**

The operator may edit the slice spec directly. When they say "go" — proceed to Phase 2.

---

## Phase 2 — Execute

### 3 — Create your branch

```bash
git checkout -b feat/slice-04-promotions-view
```

### 4 — Read the schema

Open `demo/schema/gold_marts.md`. Find `fct_promotions`. Do not invent columns.

### 5 — Generate the view file

Create `project/views/fct_promotions.view.lkml`:

- One `dimension` per column:
  - `STRING` → `type: string`
  - `INTEGER` / `FLOAT` → `type: number`
  - `BOOLEAN` → `type: yesno`
  - `DATE` → `type: date`
- One measure only: `measure: count { type: count }`
- `sql_table_name: \`gcs-automation-project.gold_marts.fct_promotions\``
- No value formats, no descriptions, no hidden fields — baseline only

Commit: `feat(views): add fct_promotions view`

### 6 — Update the model file

Add a ninth explore to `project/models/gold_marts.model.lkml`:

```lookml
explore: fct_promotions {}
```

Commit: `feat(model): add fct_promotions explore`

### 7 — Run the spine validator

```bash
python3 scripts/validate.py
```

Required gate. Fix any failures before proceeding.

### 8 — Write the handoff

Mark `project/conductor/slice-04-promotions-view.md` `status: stable`.
Advance `project/conductor/index.md` — slice-04 ACTIVE → STABLE.
Move current handoff entry to `project/conductor/handoff-archive.md`.

Write an entry at the top of `project/conductor/handoff-log.md`:

```
## Slice 04 — Promotions View

Date: <today>
Commit: <7-char hash>

### Objective
Add fct_promotions baseline view and explore to the established gold_marts project.

### Current State
- project/views/fct_promotions.view.lkml — baseline view (11 dimensions, count measure)
- project/models/gold_marts.model.lkml — 9 explores

### Files Changed
- project/views/fct_promotions.view.lkml (new)
- project/models/gold_marts.model.lkml (updated)
- project/conductor/slice-04-promotions-view.md (stable)
- project/conductor/index.md (queue closed)

### Validation
- python3 scripts/validate.py: <X passed | Y warnings | 0 failed>
- lkml: not run — pending tooling approval

### Exact Next Steps
1. Enrich fct_promotions: sum for revenue_attributed and cost, average for roas
2. Add dimension_group for start_date and end_date
3. Add value_format_name: usd for revenue/cost measures
4. Add group_label to dimensions for field picker organization
5. Consider hidden: yes on promotion_id (primary key)

### Blockers
- None
```

Commit: `docs(handoff): record slice 04 completion`

---

## Rules

- Use only columns from `demo/schema/gold_marts.md` — no invented fields
- No hardcoded credentials
- Only `type: count` measures — baseline only for this slice
- `demo/views/fct_promotions.view.lkml` is reference output — write to `project/views/`
- Commit as you go

---

## What This Demo Shows

The Conductor iterative loop in a live pair programming session:

```
Handoff Exact Next Steps → operator writes slice spec
→ agent reads + presents plan → operator reviews diff → approves or adjusts
→ agent executes → output diff reviewed live in IDE
→ handoff written → loop ready for next session
```

The slice spec is the contract between operator and agent. The review gate is where
judgment lives — the agent proposes, the operator approves.
