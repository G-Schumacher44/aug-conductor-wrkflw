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

1. Tick every satisfied acceptance-criteria checkbox in the slice doc, then run the
   validator gate (`scripts/validate.py`) and fix any failures
2. Mark completed slice `status: stable` in its slice doc
3. Update queue table (ACTIVE → STABLE). Leave the next slice `QUEUED` — don't flip it
   to `ACTIVE` until a session actually starts it
4. Update `Active slice:` line to `none — awaiting slice-NN`
5. Commit slice doc + index.md + handoff-log.md together
