# Run This Demo

You are an agent. `project/` is a deployed Conductor instance ready for LookML generation.
Read the conductor spine and execute the active slice.

---

## What You're Building

A Looker data model on top of 8 pre-aggregated BigQuery fact tables covering an
e-commerce business: revenue, sales ops, customer segments, product profitability,
marketing attribution, shipping, cart abandonment, and a daily KPI dashboard.

**BQ project:** `your-gcp-project`
**Dataset:** `gold_marts`
**Schema reference:** [`demo/schema/gold_marts.md`](./demo/schema/gold_marts.md)
**Reference output:** [`demo/views/`](./demo/views/) — what a correct slice 01 produces

---

## Orientation (read in order)

1. `project/AGENTS.md` — behavioral rules for this project
2. `project/intent.md` — BQ project, dataset, entities, modeling goal
3. `project/conductor/index.md` — active slice routing
4. The active slice spec listed in the index — your complete task definition

The slice spec contains all execution steps, type mappings, and acceptance criteria.
You do not need to read DEMO.md again after this point.

---

## Rules

- Use only columns listed in `demo/schema/gold_marts.md` — do not invent fields
- No hardcoded credentials
- Commit as you go — not one giant commit at the end
- Run `python scripts/validate.py` from the **repo root** before writing the handoff
- `demo/views/` is reference output only — write your output to `project/views/`

---

## What This Demo Shows

A Conductor-governed LookML bootstrap:

```
schema discovery → view generation → model → validate → handoff → Exact Next Steps
```

The "Exact Next Steps" in your handoff is the scheduling mechanism — you are proposing
what comes next. The operator reviews it and decides whether to run the next slice.

See [`demo/LOOP.md`](./demo/LOOP.md) for the full Conductor Loop explanation.
