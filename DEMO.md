# Run This Demo

You are an agent. Your job is to build a LookML data model for a BigQuery e-commerce
dataset using the schema and intent defined below. Follow the steps in order. When done,
write a handoff proposing what comes next.

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

---

## Steps

### 0 — Create your branch

Before writing any files, create a feature branch from `demo-run`:

```bash
git checkout -b feat/slice-01-lookml-bootstrap
```

All commits go on this branch. Do not commit directly to `demo-run` or `main`.

### 1 — Read the schema

Open `demo/schema/gold_marts.md`. It lists all 8 tables with every column name and type.
Do not invent columns. Only generate views for what is in that file.

### 2 — Generate view files

For each of the 8 tables, create `views/<table_name>.view.lkml`:

- One `dimension` per column, using this type mapping:
  - `STRING` → `type: string`
  - `INTEGER` / `FLOAT` → `type: number`
  - `BOOLEAN` → `type: yesno`
  - `DATE` → `type: date`
- One `measure: count { type: count }` in every view
- `sql_table_name: \`gcs-automation-project.gold_marts.<table_name>\``
- No value formats, no descriptions, no hidden fields — baseline only

Commit after each view: `feat(views): add <table_name> view`

### 3 — Generate the model file

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

Commit: `feat(model): add gold_marts model with 8 explores`

### 4 — Write the handoff

Add an entry to `conductor/handoff-log.md` (newest at top):

```
## Slice 01 — LookML Bootstrap

Date: <today>
Commit: <short hash>

### What Was Built
- <list of view files generated>
- models/gold_marts.model.lkml

### Validation
- <confirm each view has correct column count>
- <confirm model file includes all 8 explores>

### Open Questions
- Connection name is a placeholder — operator sets it when connecting to a real Looker instance
- <any schema gaps or type ambiguities you noticed>

### Next Slice Proposal
1. <what slice 02 should do>
2. <what slice 03 should do>
```

---

## Rules

- Use only columns from `demo/schema/gold_marts.md` — no invented fields
- No hardcoded credentials
- No PDTs, no derived tables, no joins — baseline views only
- The `demo/views/` folder is reference output — write your output to `views/` at the root
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
