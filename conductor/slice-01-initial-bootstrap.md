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

Read the schema reference file, scaffold `project/` as a new Conductor-governed repo,
generate a LookML view for every table, write a model stub with explores, and record
a handoff in `project/conductor/handoff-log.md`.

## Required Reads

1. `intent.md` — BQ project ID, dataset names, entities, modeling goals
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

### Step 0 — Scaffold project/

Before creating a branch or writing any LookML, scaffold `project/` as a new repo.
See `DEMO.md` Step 0 for the full file list and content spec.

Create this structure:
```
project/
  AGENTS.md                        ← agent behavioral rules for this LookML project
  intent.md                        ← BQ project, dataset, entities (pre-filled)
  conductor/
    index.md                       ← active slice routing
    tracks.md                      ← cross-repo connections (stub)
    handoff-log.md                 ← agent writes here after Step 6
    slice-01-lookml-bootstrap.md   ← the slice spec you are executing, adapted for project/ paths
  views/                           ← agent generates .view.lkml files here
  models/                          ← agent generates .model.lkml here
  .github/
    workflows/
      lookml-ci.yml                ← CI stub (lkml + LAMS; spectacles commented out)
```

### Step 1 — Create Your Branch

After scaffolding project/:

```bash
git checkout -b feat/slice-01-lookml-bootstrap
```

All commits for this slice go on this branch. Do not commit to `demo-run` or `main` directly.

### Step 2 — Validate Intent

Read `project/intent.md`. Confirm:
- GCP Project ID is filled in (not a placeholder)
- At least one dataset is named
- At least one entity is listed

If any placeholder values remain, stop and ask the operator to fill in `project/intent.md`.

### Step 3 — Read the Schema Reference

Open `demo/schema/gold_marts.md`. This is the authoritative schema for the demo — all
8 tables, every column name and type, in one file.

Do not use `bq` CLI, do not connect to BigQuery, do not invent columns.
Only generate views for what is explicitly listed in the schema reference.

### Step 4 — Generate View Files

For each table discovered:
- Create `project/views/<table_name>.view.lkml`
- Map every column to a LookML dimension using the type mapping in `AGENTS.md`
- Add a `count` measure — this is the **only** measure for slice 01 (no sum, average, max, min)
- Set `sql_table_name: \`<project>.<dataset>.<table>\``

Commit each view file as you go: `feat(views): add <table_name> view`

### Step 5 — Generate Model File

Create `project/models/gold_marts.model.lkml`:
- Set `connection: "<your-looker-connection-name>"` (operator will fill in the real value)
- Add one `explore:` block per primary entity listed in `project/intent.md`

Commit: `feat(model): add initial model and explores`

### Step 6 — Validate LookML syntax (Optional)

If `lkml` is available and approved in your environment, run a syntax check:

```bash
pip install lkml
lkml project/views/*.view.lkml
lkml project/models/gold_marts.model.lkml
```

A clean exit means valid LookML syntax. If `lkml` is not available or not approved,
skip this step — note it in the handoff and record Looker IDE as the pending validation gate.

### Step 7 — Run the spine validator (required gate)

```bash
node scripts/validate.js
```

Required before writing the handoff. Checks the Conductor spine, reads this slice's
acceptance criteria checkboxes, and reports pass/warn/fail. Fix any failures before
proceeding to Step 8.

### Step 8 — Write Handoff

Write a `project/conductor/handoff-log.md` entry recording:
- Tables discovered and views generated
- Any schema gaps (tables with no useful columns, ambiguous types)
- Connection name placeholder (operator must fill in)
- **Validation** — include `scripts/validate.js` output (pass count)
- **Next Slice Proposal** — what the next agent should do, in order

## Acceptance Criteria

- [ ] `project/` is fully scaffolded (AGENTS.md, intent.md, conductor/, .github/workflows/)
- [ ] One `.view.lkml` file exists for every table in `gold_marts` (8 total)
- [ ] `project/models/gold_marts.model.lkml` exists with 8 explores
- [ ] Every view has exactly one measure: `count` — no other measures
- [ ] Handoff log entry written to `project/conductor/handoff-log.md` with Next Slice Proposal
- [ ] No placeholder values in generated LookML (except connection name)
- [ ] No hardcoded credentials
- [ ] CI stub present at `project/.github/workflows/lookml-ci.yml`
- [ ] `scripts/validate.js` exits 0
