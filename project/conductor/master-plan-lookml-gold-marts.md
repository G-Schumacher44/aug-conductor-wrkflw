# Master Plan: LookML Gold Marts — Data Model Bootstrap

Date: 2026-05-01
Status: active
Type: workflow-master-plan

## Objective

Build a production-ready LookML data model on top of pre-aggregated BigQuery
fact tables for your-gcp-project.gold_marts.

Done = all tables have enriched views with typed measures, a clean model with
labeled explores, and the project validates in the Looker IDE when a connection
is provisioned.

## Phases

### Phase 1: Foundation (Slices 01-03) — COMPLETE

Establish baseline views, enrich with business measures and formats, wire the
model layer.

- Slice 01: Baseline views — one dimension per column, count measure only ✓
- Slice 02: View enrichment — typed measures, value formats, dimension_group for dates ✓
- Slice 03: Model layer — explore labels, field grouping, hidden PKs ✓

### Phase 2: Expansion (Slices 04+) — ACTIVE

Add new tables as they are provisioned in gold_marts.

- Slice 04: fct_promotions view — baseline view for new promotions table

## Architecture Decisions

- No live BQ or Looker access — `../demo/schema/gold_marts.md` is the authoritative schema
- Connection name stays placeholder until operator provisions a real Looker connection
- No PDTs or derived tables in Phase 1
- All tables are independently aggregated — no joins until operator confirms shared grain
- New tables added via individual slices — one slice per new table

## Acceptance Criteria

- [x] All 8 foundation views structurally valid
- [x] All 8 views pass simulated CI (scripts/validate.py)
- [x] models/gold_marts.model.lkml has 8 labeled explores
- [x] All Phase 1 slice acceptance criteria marked stable
- [x] fct_promotions view added (slice 04)
- [ ] Handoff log records final state with no open blockers

## Slice Index

| Slice | Status | Description |
|---|---|---|
| slice-01 | stable | Baseline views (8 tables) |
| slice-02 | stable | View enrichment |
| slice-03 | stable | Model layer polish |
| slice-04 | stable | fct_promotions view |
