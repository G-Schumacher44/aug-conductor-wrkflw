# Run Demo 2 — Ad-hoc Feature Work

You are an agent. `project/` already exists as a functioning LookML project.
A new business requirement has arrived: the business team wants to analyze promotional
campaign performance. The data team has provisioned a new BigQuery table:
`your-gcp-project.gold_marts.fct_promotions`.

The operator has written a new slice spec for this work. Your job is to read the current
project state, execute the slice, validate, and hand off.

---

## What You're Building

A new LookML view for `fct_promotions` and an updated model file that includes it as a
ninth explore. This is additive work on an established Conductor-governed project.

**Schema reference:** [`demo/schema/gold_marts.md`](./demo/schema/gold_marts.md)
**Reference output:** [`demo/views/fct_promotions.view.lkml`](./demo/views/fct_promotions.view.lkml)

---

## Steps

### 1 — Orient from the Conductor spine

Read these files in order before touching anything:

1. `project/intent.md` — project description and BQ context
2. `project/conductor/index.md` — current queue state
3. `project/conductor/handoff-log.md` — what the last agent left you
4. `project/conductor/slice-04-promotions-view.md` — your active slice spec

### 2 — Create your branch

```bash
git checkout -b feat/slice-04-promotions-view
```

Branch from `demo-2-start`. All commits for this demo go on this branch.

### 3 — Read the schema

Open `demo/schema/gold_marts.md`. Find the `fct_promotions` table. Do not invent columns.

### 4 — Generate the view file

Create `project/views/fct_promotions.view.lkml`:

- One `dimension` per column, using the standard type mapping:
  - `STRING` → `type: string`
  - `INTEGER` / `FLOAT` → `type: number`
  - `BOOLEAN` → `type: yesno`
  - `DATE` → `type: date`
- One `measure: count { type: count }` — only measure for this slice
- `sql_table_name: \`your-gcp-project.gold_marts.fct_promotions\``
- No value formats, no descriptions, no hidden fields — baseline only

Commit: `feat(views): add fct_promotions view`

### 5 — Update the model file

Add a ninth explore to `project/models/gold_marts.model.lkml`:

```lookml
explore: fct_promotions {}
```

Commit: `feat(model): add fct_promotions explore`

### 6 — Run the spine validator

```bash
python scripts/validate.py
```

Required gate before writing the handoff. Fix any failures. All checks must pass.

### 7 — Write the handoff

Mark `project/conductor/slice-04-promotions-view.md` `status: stable`.

Advance `project/conductor/index.md` — move slice-04 from ACTIVE to STABLE.

Write an entry at the top of `project/conductor/handoff-log.md`:

```
## Slice 04 — Promotions View

Date: <today>
Commit: <7-char hash>

### Objective
Add fct_promotions view and explore to the established gold_marts LookML project.

### Current State
- project/views/fct_promotions.view.lkml — view generated (baseline)
- project/models/gold_marts.model.lkml — 9 explores (was 8)

### Files Changed
- project/views/fct_promotions.view.lkml (new)
- project/models/gold_marts.model.lkml (updated)
- project/conductor/slice-04-promotions-view.md (marked stable)
- project/conductor/index.md (queue advanced)

### Validation
- scripts/validate.py: <X passed | 0 warnings | 0 failed>

### Exact Next Steps
1. Enrich fct_promotions: add typed measures (sum for revenue_attributed, cost;
   average for roas, discount_value), dimension_group for start_date and end_date,
   value_format_name for financial measures
2. Add group_label to dimensions for field picker organization
3. Consider hidden: yes on promotion_id (primary key)

### Blockers
- None
```

Move the previous handoff entry from `handoff-log.md` to `project/conductor/handoff-archive.md`.

Commit: `docs(handoff): record slice 04 completion`

---

## Rules

- Use only columns from `demo/schema/gold_marts.md` — no invented fields
- No hardcoded credentials
- Only `type: count` measures in this slice — baseline only
- `demo/views/fct_promotions.view.lkml` is reference output — write your output to `project/views/`
- Commit as you go, not one giant commit at the end

---

## What Happens Next

Your handoff's **Exact Next Steps** proposes view enrichment for fct_promotions.
The operator reviews and decides whether to run enrichment as slice 05 or proceed to
Demo 3 (automated maintenance). The Conductor loop continues.

See [`demo/LOOP.md`](./demo/LOOP.md) for the full explanation.
