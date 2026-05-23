# Conductor Index

## Active Slice

Active slice: conductor/slice-05-maintenance.md

## Queue

| Status | Slice |
|---|---|
| STABLE | conductor/slice-01-lookml-bootstrap.md |
| STABLE | conductor/slice-02-view-enrichment.md |
| STABLE | conductor/slice-03-model-layer.md |
| STABLE | conductor/slice-04-promotions-view.md |
| ACTIVE | conductor/slice-05-maintenance.md |

## Master Plan
[LookML Gold Marts Master Plan](./master-plan-lookml-gold-marts.md)

## Agent — end-of-slice responsibilities
1. Mark completed slice `status: stable` in its slice doc
2. Update queue table (ACTIVE → STABLE, next QUEUED → ACTIVE)
3. Commit slice doc + index.md + handoff-log.md together
