# Slice 03: Model Layer

Date: 2026-05-03
Status: stable
Type: workflow-slice

## Objective

Polish the model file — add explore labels, field group_label organization,
and descriptions. No joins until operator confirms shared grain between tables.

## Steps

1. Add `label:` and `description:` to each explore block
2. Add `group_label:` to key dimensions and measures within each view
3. Add `hidden: yes` to primary key dimensions (ID fields)
4. Review join opportunities — document any confirmed shared grains in handoff
5. Run `scripts/validate.py` — fix any failures
6. Write handoff with Exact Next Steps

## Acceptance Criteria

- [x] Every explore has a label and description
- [x] Key dimensions have group_label applied
- [x] PK dimensions are hidden
- [x] No joins added without operator confirmation in handoff
- [x] scripts/validate.py exits 0
- [x] Slice marked stable, conductor/index.md queue shows slices 01-03 STABLE
- [x] Handoff written — records full project state, notes any open blockers for operator
