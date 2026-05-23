# Slice 01: LookML Bootstrap

Date: 2026-05-01
Status: stable
Type: workflow-slice

## Objective

Read the schema reference, generate an initial LookML view for every table,
write a model file with explores, and record a handoff.

## Steps

1. Read `intent.md`
2. Read `../demo/schema/gold_marts.md` — do not invent columns
3. For each table: create `views/<table>.view.lkml`
4. Create `models/gold_marts.model.lkml` with 8 explores
5. Run `python scripts/validate.py`
6. Write handoff to `conductor/handoff-log.md`

## Acceptance Criteria

- [x] One .view.lkml per table (8 total)
- [x] Every view has exactly one measure: count
- [x] No non-baseline measures (no sum, average, max, min)
- [x] models/gold_marts.model.lkml with 8 explores
- [x] CI stub present at .github/workflows/lookml-ci.yml
- [x] scripts/validate.py exits 0
- [x] Handoff written with Exact Next Steps and validator output in Validation field
- [x] No hardcoded credentials
