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

### Step 0 — Promote this slice to ACTIVE

Before any work: in `conductor/index.md`, set this slice's queue row `QUEUED → ACTIVE` and
set the `Active slice:` line to this slice's path. The validator only checks the acceptance
criteria of the slice named there and short-circuits when it reads `none`, so skipping this
leaves the gate checking nothing.

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

### Step 5 — Write the handoff

Write an entry at the **top** of `conductor/handoff-log.md`. Move the current top entry to
`conductor/handoff-archive.md` first.

### Step 6 — Tick satisfied acceptance criteria, then run the spine validator (required gate)

Tick (`- [x]`) every item in this file's **Acceptance Criteria** section that is now
true — including "Handoff written", since Step 5 just did that.

Run from the **repo root**:

```bash
python3 scripts/validate.py
```

This is the required gate. It runs while slice-02 is still `Active slice:` in
`conductor/index.md`, so it genuinely checks this slice's acceptance criteria, not a
short-circuited "none". Fix any failures before proceeding. Once clean, paste the real
`X passed | Y warnings | 0 failed` line into the handoff's `### Validation` field.

### Step 7 — Mark slice stable, advance the queue, and commit

In this file: `Status: queued` → `Status: stable`

In `conductor/index.md`:
- slice-02 `ACTIVE` → `STABLE`
- Leave slice-03 `QUEUED` — do not flip it to `ACTIVE` yet; its criteria are all
  unchecked, and a later validator run would fail on slice-03's progress instead of
  reporting slice-02's completion.
- Update `Active slice:` line to `none — awaiting slice-03`

Commit the slice doc, `conductor/index.md`, and `conductor/handoff-log.md` (plus
`conductor/handoff-archive.md` if the prior entry moved) together.

## Acceptance Criteria

- [ ] Every numeric fact field has a typed measure (sum or average)
- [ ] All financial measures have value_format_name applied
- [ ] All DATE columns converted to dimension_group
- [ ] No dimensions removed or renamed from slice 01
- [ ] Handoff written with Exact Next Steps
