# Slice 01: LookML Bootstrap — Schema Discovery & View Generation

Date: 2026-05-23
Status: active
Type: workflow-slice
Owner: agent

## Objective

Read the schema reference, generate an initial LookML view for every table,
write a model file with explores, validate, and record a handoff.

## Required Reads

1. `intent.md` — BQ project ID, dataset name, entities, modeling goals
2. `../demo/schema/gold_marts.md` — authoritative schema (all 8 tables, every column)
3. `conductor/index.md` — routing
4. This slice

## Execution Steps

### Step 1 — Create your branch

```bash
git checkout -b feat/slice-01-lookml-bootstrap
```

All commits for this slice go on this branch. Do not commit to `main` directly.

### Step 2 — Read the schema reference

Open `../demo/schema/gold_marts.md`. It lists all 8 tables with every column name and type.

Do not use `bq` CLI, do not connect to BigQuery, do not invent columns.
Only generate views for what is explicitly listed in the schema reference.

### Step 3 — Generate view files

For each table: create `views/<table_name>.view.lkml`

Type mapping:
- `STRING` → `type: string`
- `INTEGER` / `FLOAT` → `type: number`
- `BOOLEAN` → `type: yesno`
- `DATE` → `type: date`

Rules:
- One `dimension` per column
- One measure only: `measure: count { type: count }` — **no other measures in slice 01**
- `sql_table_name: \`your-gcp-project.gold_marts.<table_name>\``
- No value formats, descriptions, or hidden fields — baseline only

Commit after each view: `feat(views): add <table_name> view`

### Step 4 — Generate the model file

Create `models/gold_marts.model.lkml`:

```lookml
connection: "your-looker-connection-name"

include: "/views/*.view.lkml"

explore: fct_finance_revenue {}
explore: fct_sales_operations {}
explore: fct_customer_segments {}
explore: fct_product_profitability {}
explore: fct_marketing_attribution {}
explore: fct_shipping_analysis {}
explore: fct_cart_abandonment {}
explore: fct_daily_dashboard {}
```

Connection name is a placeholder — operator fills in when provisioning a Looker connection.

Commit: `feat(model): add gold_marts model with 8 explores`

### Step 5 — Validate LookML syntax (optional)

If `lkml` is available in your environment:

```bash
lkml views/*.view.lkml models/*.model.lkml
```

Note the result in the handoff Validation field. Skip if tooling is not approved.

### Step 6 — Write the handoff

Write an entry at the **top** of `conductor/handoff-log.md` (above the comment marker):

```
## Slice 01 — LookML Bootstrap

Date: <today>
Commit: <7-char hash>

### Objective
Bootstrap LookML views for all 8 gold_marts tables.

### Current State
- views/ — 8 view files generated
- models/gold_marts.model.lkml — model with 8 explores

### Files Changed
- views/fct_*.view.lkml (8 files)
- models/gold_marts.model.lkml
- conductor/slice-01-lookml-bootstrap.md (stable)
- conductor/index.md (queue advanced to slice-02)

### Validation
- scripts/validate.py: <X passed | Y warnings | 0 failed>
- lkml: <exit 0 for all views and model | "not run — not approved">

### Exact Next Steps
1. Add typed measures (sum, average, count_distinct) for numeric fields in each view
2. Add dimension_group for DATE columns with timeframes: [date, week, month, quarter, year]
3. Add value_format_name to financial measures (decimal_2 or usd)
4. Run scripts/validate.py from repo root — fix any failures
5. Mark slice-02 stable, advance queue to slice-03

### Blockers
- Connection name is a placeholder — operator sets it when connecting to Looker
```

`Commit:` is the hash of your last work commit so far (e.g. Step 4's `feat(model): ...`
commit — check `git log -1 --format=%h`), not the handoff commit itself, which doesn't
exist yet.

### Step 7 — Tick satisfied acceptance criteria, then run the spine validator (required gate)

Go to the **Acceptance Criteria** section below and tick (`- [x]`) every item that is now
true — including "Handoff written", since Step 6 just did that. Only tick what is
actually true.

Then run, from the **repo root** (not from project/):

```bash
python3 scripts/validate.py
```

This is the required gate. It runs while slice-01 is still `Active slice:` in
`conductor/index.md`, so it genuinely checks this slice's acceptance criteria, not a
short-circuited "none". Fix any failures before proceeding — all checks must pass. Once
clean, paste the real `X passed | Y warnings | 0 failed` line into the handoff's
`### Validation` field you wrote in Step 6.

### Step 8 — Mark slice stable, advance the queue, and commit

In this file: change `Status: active` → `Status: stable`

In `conductor/index.md`:
- Update queue row: slice-01 `ACTIVE` → `STABLE`
- Leave slice-02 `QUEUED` — do not flip it to `ACTIVE` yet. Its acceptance criteria are
  all unchecked, and a validator run after this point would fail on the next slice's
  progress instead of reporting this one's completion.
- Update `Active slice:` line to `none — awaiting slice-02` (the operator promotes it to
  `ACTIVE` when a session starts slice-02 — same pattern used to close out slice-04 in
  Demo 2).

Commit the slice doc, `conductor/index.md`, and `conductor/handoff-log.md` together:
`docs(handoff): record slice 01 completion`

## Acceptance Criteria

- [ ] One .view.lkml per table (8 total)
- [ ] Every view has exactly one measure: count
- [ ] No non-baseline measures (no sum, average, max, min)
- [ ] models/gold_marts.model.lkml with 8 explores
- [ ] CI stub present at .github/workflows/lookml-ci.yml
- [ ] Handoff written with Exact Next Steps
- [ ] No hardcoded credentials
