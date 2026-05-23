# Slice 01: LookML Bootstrap — Schema Discovery & View Generation

Date: 2026-05-23
Status: active
Type: workflow-slice
Owner: agent

```yaml
conductor_mode: slice
context_budget: medium
stage_required: false
handoff_required: true
stable_tag_required: false
```

## Objective

Read the project intent, discover the BigQuery schema for each declared dataset,
and generate an initial LookML view file for every table found. Write a model
file stub with explores. Record a handoff when done.

## Required Reads

1. `intent.md` — BQ project ID, dataset names, entities, relationships, modeling goals
2. `AGENTS.md` — LookML conventions, type mapping, naming rules
3. `conductor/index.md` — routing
4. This slice

## Mode And Context Contract

- Mode: `slice`
- Required reads: listed above
- Forbidden reads without reason: unrelated directories, external repos
- Stage/DUOS: not required for this slice
- Tag posture: no tag — bootstrap is not a stable milestone

## Execution Steps

### Step 1 — Validate Intent

Read `intent.md`. Confirm:
- GCP Project ID is filled in (not a placeholder)
- At least one dataset is named
- At least one entity is listed

If any placeholder values remain, stop and ask the operator to fill in `intent.md`.

### Step 2 — Read the Schema Reference

Open `demo/schema/gold_marts.md`. This is the authoritative schema for the demo — all
8 tables, every column name and type, in one file.

Do not use `bq` CLI, do not connect to BigQuery, do not invent columns.
Only generate views for what is explicitly listed in the schema reference.

### Step 3 — Generate View Files

For each table discovered:
- Create `views/<table_name>.view.lkml`
- Map every column to a LookML dimension using the type mapping in `AGENTS.md`
- Add a `count` measure
- Add `sum` and `average` measures for columns that represent money, quantity, or duration
- Set `sql_table_name: \`<project>.<dataset>.<table>\``

Commit each view file as you go: `feat(views): add <table_name> view`

### Step 4 — Generate Model File

Create `models/gold_marts.model.lkml`:
- Set `connection: "<your-looker-connection-name>"` (operator will fill in the real value)
- Add one `explore:` block per primary entity listed in `intent.md`
- Leave a `# TODO` comment for any relationships not yet confirmed

Commit: `feat(model): add initial model and explores`

### Step 5 — Write Handoff

Write a `conductor/handoff-log.md` entry recording:
- Tables discovered and views generated
- Any schema gaps (tables with no useful columns, ambiguous types)
- Connection name placeholder (operator must fill in)
- **Next Slice Proposal** — what the next agent should do, in order

## Acceptance Criteria

- [ ] One `.view.lkml` file exists for every table in `gold_marts`
- [ ] `models/gold_marts.model.lkml` exists with at least one explore
- [ ] Every view has a `count` measure
- [ ] Handoff log entry written with Next Slice Proposal
- [ ] No placeholder values in generated LookML (except connection name)
- [ ] No hardcoded credentials
