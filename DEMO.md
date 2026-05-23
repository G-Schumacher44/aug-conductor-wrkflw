# Run This Demo

You are an agent. Your job is to bootstrap a LookML data model for a BigQuery e-commerce
dataset inside a fresh `project/` directory you will scaffold as a new repo. Follow the
steps in order. When done, write a handoff.

---

## What You're Building

A Looker data model on top of 8 pre-aggregated BigQuery fact tables covering an
e-commerce business: revenue, sales ops, customer segments, product profitability,
marketing attribution, shipping, cart abandonment, and a daily KPI dashboard.

**BQ project:** `gcs-automation-project`
**Dataset:** `gold_marts`
**Schema reference:** [`demo/schema/gold_marts.md`](./demo/schema/gold_marts.md)
**Intent (full):** [`demo/intent-example.md`](./demo/intent-example.md)
**Reference output:** [`demo/views/`](./demo/views/) — what slice 01 produces

`project/` is your output root — a full Conductor-governed LookML project you scaffold
from scratch, treating it as a new standalone repo.

---

## Steps

### 0 — Scaffold project/ as a new repo

Before writing any LookML or creating a branch, scaffold the full project structure.
Create each file listed below. `project/` is the root — all paths inside are relative to it.

**Directory structure to create:**
```
project/
  AGENTS.md
  intent.md
  conductor/
    index.md
    tracks.md
    handoff-log.md
    slice-01-lookml-bootstrap.md
  views/                         ← agent writes LookML views here
  models/                        ← agent writes model here
  .github/
    workflows/
      lookml-ci.yml
```

---

#### `project/AGENTS.md`

Agent behavioral rules for this LookML project. Write it with:

```markdown
# Agent Rules — LookML Project

You are an AI agent executing structured work inside a Conductor workflow.
Read the slice spec, do the work, write the handoff.

## The Conductor Loop

- Read active slice spec → execute bounded work → write handoff
- The handoff's **Next Slice Proposal** field is your recommendation for the next unit of work
- Operator reviews, approves or redirects, starts next session

## Required Reading Order

1. `intent.md` — project description and BQ context
2. `conductor/index.md` — active slice routing
3. The active `conductor/slice-*.md` — current unit of work
4. Latest entry in `conductor/handoff-log.md` — state from last agent

## Execution Rules

- Read before writing. Read the slice spec before touching any files.
- One slice at a time. Complete and hand off before starting the next.
- Scope discipline. If the slice says it's out of scope, note it in the handoff.
- No invented columns. Only use what is in the schema reference.

## Handoff Rules

Every session ends with a `conductor/handoff-log.md` entry containing:

- **Commit:** — 7-char hash
- **Objective** — what this session set out to do
- **Current State** — what was actually completed
- **Files Changed** — list of written or modified files
- **Validation** — what was verified
- **Next Slice Proposal** — what the next agent should do (the scheduling mechanism)
- **Blockers** — unresolved items for operator

Newest entry at top. Move older entries to `conductor/handoff-archive.md`.

## Git Rules

- Create a feature branch: `git checkout -b feat/slice-01-<description>`
- Branch from the current working branch — never commit to `main` directly
- Commit after each meaningful unit of work
- Format: `type(scope): description`
```

---

#### `project/intent.md`

```markdown
# Intent

BQ Project: gcs-automation-project
Dataset: gold_marts
Schema reference: ../demo/schema/gold_marts.md

No live BQ or Looker access in this demo — use schema reference only.

## Entities

- fct_finance_revenue
- fct_sales_operations
- fct_customer_segments
- fct_product_profitability
- fct_marketing_attribution
- fct_shipping_analysis
- fct_cart_abandonment
- fct_daily_dashboard

## Slice 01 Goal

Bootstrap LookML views for all 8 gold_marts tables.
Baseline only: one dimension per column, one count measure per view.
No joins, no PDTs, no derived tables, no value formats — baseline only.
```

---

#### `project/conductor/index.md`

```markdown
# Conductor Index

Active slice: conductor/slice-01-lookml-bootstrap.md
Status: in-progress
```

---

#### `project/conductor/tracks.md`

```markdown
# Conductor Tracks

No cross-repo tracks defined for this project.
Add tracks here when connecting to upstream or downstream repos.
```

---

#### `project/conductor/handoff-log.md`

Stub header — you will write the real entry in Step 6:

```markdown
# Handoff Log

<!-- Agent writes entries here after each slice. Newest at top. -->
```

---

#### `project/conductor/slice-01-lookml-bootstrap.md`

The slice spec you are executing. Write it with:

```markdown
# Slice 01: LookML Bootstrap

Date: <today>
Status: in-progress
Type: workflow-slice

## Objective

Read the schema reference, generate an initial LookML view for every table,
write a model file with explores, and record a handoff.

## Steps

1. Read `intent.md`
2. Read `../demo/schema/gold_marts.md` — do not invent columns
3. For each table: create `views/<table>.view.lkml`
   - One dimension per column (STRING→string, INTEGER/FLOAT→number, BOOLEAN→yesno, DATE→date)
   - One measure: count { type: count } — this is the only measure
   - sql_table_name: `gcs-automation-project.gold_marts.<table>`
4. Create `models/gold_marts.model.lkml` with 8 explores
5. Optional: validate with `lkml views/*.view.lkml`
6. Write handoff to `conductor/handoff-log.md`

## Acceptance Criteria

- [ ] One .view.lkml per table (8 total)
- [ ] Every view has exactly one measure: count
- [ ] No non-baseline measures (no sum, average, max, min)
- [ ] models/gold_marts.model.lkml with 8 explores
- [ ] CI stub present at .github/workflows/lookml-ci.yml
- [ ] scripts/validate.py exits 0 (run from repo root before writing handoff)
- [ ] Handoff written with Next Slice Proposal and validator output in Validation field
- [ ] No hardcoded credentials
```

---

#### `project/.github/workflows/lookml-ci.yml`

CI pipeline stub — comment-disabled until a Looker connection is provisioned:

```yaml
name: LookML CI
# Stub — operator enables jobs after a Looker connection is provisioned
on:
  push:
    paths: ['views/**', 'models/**']
  pull_request:

jobs:
  syntax:
    name: lkml syntax check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install lkml
      - run: lkml views/*.view.lkml models/*.model.lkml

  lint:
    name: LAMS style check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install -g @looker/look-at-me-sideways
      - run: lams --source="."

# spectacles-lookml:
#   Requires live Looker connection — uncomment after provisioning
#   steps:
#     - run: pip install spectacles
#     - run: spectacles lookml --project gold_marts

# spectacles-sql:
#   Requires Looker + BigQuery — uncomment after provisioning
#   steps:
#     - run: spectacles sql --project gold_marts --explore fct_finance_revenue
```

---

### 1 — Create your branch

After scaffolding `project/`, create a feature branch:

```bash
git checkout -b feat/slice-01-lookml-bootstrap
```

All commits for this demo go on this branch.

### 2 — Read the schema

Open `demo/schema/gold_marts.md`. It lists all 8 tables with every column name and type.
Do not invent columns. Only generate views for what is in that file.

### 3 — Generate view files

For each of the 8 tables, create `project/views/<table_name>.view.lkml`:

- One `dimension` per column, using this type mapping:
  - `STRING` → `type: string`
  - `INTEGER` / `FLOAT` → `type: number`
  - `BOOLEAN` → `type: yesno`
  - `DATE` → `type: date`
- One `measure: count { type: count }` in every view — **only measure for slice 01**
- `sql_table_name: \`gcs-automation-project.gold_marts.<table_name>\``
- No value formats, no descriptions, no hidden fields — baseline only

Commit after each view: `feat(views): add <table_name> view`

### 4 — Generate the model file

Create `project/models/gold_marts.model.lkml`:

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

Commit: `feat(model): add gold_marts model with 8 explores`

### 5 — Validate LookML syntax (Optional)

If `lkml` is available and approved in your environment:

```bash
pip install lkml
lkml project/views/*.view.lkml
lkml project/models/gold_marts.model.lkml
```

Clean exit = valid LookML syntax. If not available, skip and note it in the handoff.
See [`demo/tools/lkml-validator.md`](./demo/tools/lkml-validator.md) for the evaluation brief.

### 6 — Run the spine validator

```bash
python scripts/validate.py
```

This is a **required gate** before writing the handoff. The script checks the Conductor
spine, reads the active slice's acceptance criteria checkboxes, and reports pass/warn/fail.
Fix any failures before proceeding. No npm install required — pure Node stdlib.

All checks must pass before moving to Step 7.

### 7 — Write the handoff

Write an entry at the top of `project/conductor/handoff-log.md`:

```
## Slice 01 — LookML Bootstrap

Date: <today>
Commit: <7-char hash>

### Objective
Bootstrap LookML views for all 8 gold_marts tables.

### Current State
- project/views/ — 8 view files generated
- project/models/gold_marts.model.lkml — model with 8 explores

### Files Changed
- project/views/fct_*.view.lkml (8 files)
- project/models/gold_marts.model.lkml

### Validation
- scripts/validate.py: <X passed | 0 warnings | 0 failed>
- lkml: <exit 0 for all 8 views and model | "not run — not approved">

### Next Slice Proposal
1. Add typed measures (sum, average) for numeric fields in each view
2. Add dimension_group for DATE columns
3. Add value formats, labels, and group_label for field organization

### Blockers
- Connection name is a placeholder — operator sets it when connecting to Looker
- <any schema gaps or type ambiguities noticed>
```

Commit: `docs(handoff): record slice 01 completion`

---

## Rules

- Use only columns from `demo/schema/gold_marts.md` — no invented fields
- No hardcoded credentials
- No PDTs, no derived tables, no joins — baseline views only
- Only `type: count` measures in slice 01 — no sum, average, max, min
- `demo/views/` is reference output — write your output to `project/views/`
- Commit as you go, not one giant commit at the end

---

## What Happens Next

When you finish and write the handoff, you have completed one turn of the Conductor Loop:

```
intent defined → slice executed → handoff written → Next Slice Proposal → operator approves → repeat
```

The "Next Slice Proposal" in your handoff is the scheduling mechanism. You are proposing
what comes next. The operator reviews it and decides whether to run it.

See [`demo/LOOP.md`](./demo/LOOP.md) for the full explanation.
