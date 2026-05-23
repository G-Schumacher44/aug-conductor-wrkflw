# Slice 02: View Enrichment

Date: 2026-05-02
Status: stable
Type: workflow-slice

## Objective

Enrich all 8 baseline views with typed measures, value formats, and
dimension_group definitions for date fields. No structural changes to existing
dimensions — additive only.

## Steps

1. For each view, add typed measures for numeric facts
2. Add `value_format_name` to financial measures
3. Replace DATE dimensions with `dimension_group` + timeframes
4. Run `scripts/validate.py` — fix any failures
5. Write handoff with Exact Next Steps

## Acceptance Criteria

- [x] Every numeric fact field has a typed measure (sum or average)
- [x] All financial measures have value_format_name applied
- [x] All DATE columns converted to dimension_group
- [x] No dimensions removed or renamed from slice 01
- [x] scripts/validate.py exits 0
- [x] Slice marked stable, conductor/index.md queue advanced to slice-03
- [x] Handoff written with Exact Next Steps
