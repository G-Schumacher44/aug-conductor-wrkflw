# Conductor Index

Status: active
Type: conductor-index

## Active Slice

Active slice: conductor/slice-01-lookml-bootstrap.md

## Queue

| Status | Slice |
|---|---|
| ACTIVE | conductor/slice-01-lookml-bootstrap.md |
| QUEUED | conductor/slice-02-view-enrichment.md |
| QUEUED | conductor/slice-03-model-layer.md |

## Master Plan

[LookML Gold Marts Master Plan](./master-plan-lookml-gold-marts.md)

## Agent — end-of-slice responsibilities

1. Mark completed slice `status: stable` in its slice doc
2. Update queue table (ACTIVE → STABLE, next QUEUED → ACTIVE)
3. Update `Active slice:` line to point to next slice
4. Commit slice doc + index.md + handoff-log.md together
