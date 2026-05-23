# Slice 02: View Enrichment

Date: 2026-05-23
Status: queued
Type: workflow-slice
Owner: agent

## Objective

Enrich all 8 baseline views with typed measures, value formats, and dimension_group
definitions for date fields. Additive only — no dimensions removed or renamed from slice 01.

## Required Reads

1. `intent.md`
2. `conductor/master-plan-lookml-gold-marts.md` — architecture decisions
3. `conductor/handoff-log.md` — state from slice 01
4. `../demo/schema/gold_marts.md` — column types

## Execution Steps

### Step 1 — Create your branch

```bash
git checkout -b feat/slice-02-view-enrichment
```

### Step 2 — Add typed measures to each view

For each view, add typed measures for numeric facts:
- Revenue, cost, margin, spend fields → `type: sum`
- Rate, percentage, ratio fields → `type: average`
- ID fields used for counting → `type: count_distinct`

### Step 3 — Add value formats to financial measures

Apply `value_format_name` to financial measures:
- Dollar amounts → `value_format_name: usd`
- Decimal rates/percentages → `value_format_name: decimal_2`

### Step 4 — Convert DATE columns to dimension_group

Replace each `DATE` dimension with a `dimension_group`:

```lookml
dimension_group: <field_name> {
  type: time
  timeframes: [date, week, month, quarter, year]
  datatype: date
  sql: ${TABLE}.<column_name> ;;
}
```

### Step 5 — Run the spine validator (required gate)

Run from the **repo root**:

```bash
python3 scripts/validate.py
```

Fix any failures before writing the handoff.

### Step 6 — Mark slice stable and advance the queue

In this file: `Status: queued` → `Status: stable`

In `conductor/index.md`:
- slice-02 `ACTIVE` → `STABLE`
- slice-03 `QUEUED` → `ACTIVE`
- Update `Active slice:` line to `conductor/slice-03-model-layer.md`

### Step 7 — Write the handoff

Write an entry at the **top** of `conductor/handoff-log.md`. Move the current top entry to
`conductor/handoff-archive.md` first.

## Acceptance Criteria

- [ ] Every numeric fact field has a typed measure (sum or average)
- [ ] All financial measures have value_format_name applied
- [ ] All DATE columns converted to dimension_group
- [ ] No dimensions removed or renamed from slice 01
- [ ] scripts/validate.py exits 0 (run from repo root)
- [ ] slice-02 marked stable, conductor/index.md advanced to slice-03
- [ ] Handoff written with Exact Next Steps
