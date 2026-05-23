# Slice 04: Promotions View

Date: 2026-05-23
Status: queued
Type: workflow-slice

## Objective

Add a baseline LookML view for the new `fct_promotions` table that has been
provisioned in gold_marts, and register it as a ninth explore in the model file.

## Context

The business team wants to analyze promotional campaign performance. The data team
has added `gcs-automation-project.gold_marts.fct_promotions` to the dataset.
Schema reference: `../demo/schema/gold_marts.md` — find the `fct_promotions` section.

## Required Reads

1. `intent.md`
2. `conductor/master-plan-lookml-gold-marts.md` — architecture decisions
3. `conductor/handoff-log.md` — state from slice 03
4. `../demo/schema/gold_marts.md` — fct_promotions column list

## Steps

1. Create `views/fct_promotions.view.lkml`
   - One dimension per column (use standard type mapping)
   - One measure: `count { type: count }` — only measure for this slice
   - `sql_table_name: \`gcs-automation-project.gold_marts.fct_promotions\``
   - No value formats, no descriptions, no hidden fields — baseline only
2. Add ninth explore to `models/gold_marts.model.lkml`: `explore: fct_promotions {}`
3. Run `python scripts/validate.py` — fix any failures
4. Write handoff with Exact Next Steps for enrichment

## Acceptance Criteria

- [ ] views/fct_promotions.view.lkml created
- [ ] All columns from schema represented as dimensions
- [ ] Exactly one measure: count
- [ ] No non-baseline measures (no sum, average, max, min)
- [ ] models/gold_marts.model.lkml has 9 explores
- [ ] scripts/validate.py exits 0
- [ ] Slice marked stable, conductor/index.md updated
- [ ] Handoff written with Exact Next Steps for enrichment
- [ ] No hardcoded credentials
