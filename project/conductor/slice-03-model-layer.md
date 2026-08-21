# Slice 03: Model Layer

Date: 2026-05-23
Status: queued
Type: workflow-slice
Owner: agent

## Objective

Polish the model file — add explore labels, field group_label organization, and descriptions.
No joins until operator confirms shared grain between tables.

## Required Reads

1. `intent.md`
2. `conductor/master-plan-lookml-gold-marts.md` — architecture decisions
3. `conductor/handoff-log.md` — state from slice 02
4. `models/gold_marts.model.lkml`

## Execution Steps

### Step 1 — Create your branch

```bash
git checkout -b feat/slice-03-model-layer
```

### Step 2 — Add labels and descriptions to explores

For each explore block in `models/gold_marts.model.lkml`:

```lookml
explore: fct_finance_revenue {
  label: "Finance Revenue"
  description: "Daily revenue, margin, and cost metrics by product and channel"
}
```

### Step 3 — Add group_label to dimensions and measures

Within each view, group related fields:

```lookml
dimension: revenue_usd {
  group_label: "Revenue"
  ...
}
```

### Step 4 — Hide primary key dimensions

Add `hidden: yes` to ID fields used as primary keys — they should not appear in the field picker.

### Step 5 — Document join opportunities

Review which tables share a grain (e.g., date, product_id). Document any confirmed shared
grains in the handoff. Do **not** add joins without operator confirmation — note them as
candidates only.

### Step 6 — Write the final handoff

Write an entry at the **top** of `conductor/handoff-log.md`. Move current entry to archive.

The final handoff should record:
- Full project state (all 8 views enriched, model labeled)
- Any join candidates (not yet added — operator decision)
- Connection name still placeholder
- What operator must do to make the project live in Looker

### Step 7 — Tick satisfied acceptance criteria, then run the spine validator (required gate)

Tick (`- [x]`) every item in this file's **Acceptance Criteria** section that is now
true — including "Handoff written", since Step 6 just did that.

Run from the **repo root**:

```bash
python3 scripts/validate.py
```

This is the required gate. It runs while slice-03 is still `Active slice:` in
`conductor/index.md`, so it genuinely checks this slice's acceptance criteria, not a
short-circuited "none". Fix any failures before proceeding. Once clean, paste the real
`X passed | Y warnings | 0 failed` line into the handoff's `### Validation` field.

### Step 8 — Mark slice stable, close the queue, and commit

In this file: `Status: queued` → `Status: stable`

In `conductor/index.md`:
- slice-03 `ACTIVE` → `STABLE`
- Update `Active slice:` line to `none — all slices stable`

In `conductor/master-plan-lookml-gold-marts.md`:
- Update slice index table: all rows → stable
- Update Status: active → stable

Commit the slice doc, `conductor/index.md`, `conductor/master-plan-lookml-gold-marts.md`,
and `conductor/handoff-log.md` (plus `conductor/handoff-archive.md`) together.

## Acceptance Criteria

- [ ] Every explore has a label and description
- [ ] Key dimensions have group_label applied
- [ ] PK dimensions are hidden
- [ ] No joins added without operator confirmation in handoff
- [ ] Handoff written — records full project state, notes any open blockers for operator
