# Master Plan: LookML Gold Marts — Data Model Bootstrap

Date: 2026-05-23
Status: active
Type: workflow-master-plan

## Objective

Build a production-ready LookML data model on top of 8 pre-aggregated BigQuery
fact tables for your-gcp-project.gold_marts.

Done = all 8 tables have enriched views with typed measures, a clean model with
labeled explores, and the project validates in the Looker IDE when a connection
is provisioned.

## Phases

### Phase 1: Foundation (Slices 01-03)

Establish baseline views, enrich with business measures and formats, wire the model layer.

- Slice 01: Baseline views — one dimension per column, count measure only
- Slice 02: View enrichment — typed measures, value formats, dimension_group for dates
- Slice 03: Model layer — explore labels, field grouping, joins where grain is confirmed

## Architecture Decisions

- No live BQ or Looker access — `../demo/schema/gold_marts.md` is the authoritative schema
- Connection name stays placeholder until operator provisions a real Looker connection
- No PDTs or derived tables in Phase 1
- All 8 tables are independently aggregated — no joins until operator confirms shared grain

## Acceptance Criteria

- [ ] All 8 views structurally valid (simulated CI via scripts/validate.py)
- [ ] All 8 views pass lkml syntax check (when tooling approved)
- [ ] models/gold_marts.model.lkml has 8 labeled explores
- [ ] All slice acceptance criteria marked stable
- [ ] Handoff log records final state with no open blockers

## Slice Index

| Slice | Status | Description |
|---|---|---|
| slice-01 | active | Baseline views |
| slice-02 | queued | View enrichment |
| slice-03 | queued | Model layer |
