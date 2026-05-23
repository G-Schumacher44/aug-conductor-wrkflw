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

### Step 6 — Run the spine validator (required gate)

Run from the **repo root**:

```bash
python scripts/validate.py
```

Fix any failures before writing the handoff.

### Step 7 — Mark slice stable and close the queue

In this file: `Status: queued` → `Status: stable`

In `conductor/index.md`:
- slice-03 `ACTIVE` → `STABLE`
- Update `Active slice:` line to `none — all slices stable`

In `conductor/master-plan-lookml-gold-marts.md`:
- Update slice index table: all rows → stable
- Update Status: active → stable

### Step 8 — Write the final handoff

Write an entry at the **top** of `conductor/handoff-log.md`. Move current entry to archive.

The final handoff should record:
- Full project state (all 8 views enriched, model labeled)
- Any join candidates (not yet added — operator decision)
- Connection name still placeholder
- What operator must do to make the project live in Looker

## Acceptance Criteria

- [ ] Every explore has a label and description
- [ ] Key dimensions have group_label applied
- [ ] PK dimensions are hidden
- [ ] No joins added without operator confirmation in handoff
- [ ] scripts/validate.py exits 0 (run from repo root)
- [ ] All slices marked stable, conductor/index.md queue shows all STABLE
- [ ] Handoff written — records full project state, notes any open blockers for operator
