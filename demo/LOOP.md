# The Conductor Loop — In Action

This document shows the self-scheduling loop using the LookML demo as a concrete example.

## What The Loop Looks Like

```
You fill in intent.md
       ↓
Agent reads slice-01-initial-bootstrap.md
       ↓
Agent discovers BQ schema, generates 8 view files, writes model file
       ↓
Agent writes handoff — including Next Slice Proposal
       ↓
You read the proposal, decide whether to run slice 02
       ↓
Next agent session reads the new slice spec
       ↓
repeat
```

## Slice 01 → Handoff → Slice 02 Proposal

Open [`demo/handoff-example.md`](./handoff-example.md). Scroll to **Next Slice Proposal**.

That section was written by the agent — not the operator. It reads:

> 1. **Operator**: Set the Looker connection name in `models/gold_marts.model.lkml`
> 2. **Slice 02**: Validate all views in Looker IDE — fix any type inference issues
> 3. **Slice 03**: Review `fct_daily_dashboard` and decide if it warrants its own explore
> 4. **Slice 04**: Add hidden dimensions for ID/key columns

That is the loop. The agent built slice 01, then proposed slice 02–04 in the handoff.
The operator's job is to read those proposals and decide which one to promote to the next
`conductor/slice-02-*.md` file.

## What The Agent Did In Slice 01

1. Read `intent.md` — learned the BQ project, dataset, and modeling goals
2. Read `conductor/slice-01-initial-bootstrap.md` — learned the acceptance criteria
3. Connected to BigQuery, ran schema discovery on all 8 tables in `gold_marts`
4. Generated 8 LookML view files (one per table) in `views/`
5. Generated `models/gold_marts.model.lkml` with 8 explores
6. Wrote `conductor/handoff-log.md` with current state + Next Slice Proposal
7. Committed: `feat(conductor): initial agnostic workflow deployment with LookML demo`

## What The Operator Did In Slice 01

1. Filled in `intent.md` with the BQ project and dataset names
2. Started an agent session
3. Read the handoff when done
4. Decided which next slice to run

That is it. The agent generated the scope for every subsequent slice.

## The Recursive Quality

The system that ran this workflow (the agent) also improved the system it ran on:

- The views the agent generated are inputs to the next agent's Looker validation work
- The handoff the agent wrote is the next agent's work order
- The schema gaps the agent surfaced are decisions only the operator can make — they are
  explicitly flagged in "Open Questions" rather than guessed

No state lives in the agent's memory. Everything the next agent needs is in these files.

## Starting Your Own Loop

1. Copy this repo (or deploy a fresh `lookml-bq` blueprint via Workspace Partner)
2. Fill in `intent.md` with your BQ project and dataset
3. Start an agent session — point it at this directory
4. Agent reads `AGENTS.md` → `conductor/index.md` → `conductor/slice-01-*.md` → executes
5. Read the handoff. Promote the Next Slice Proposal to `conductor/slice-02-*.md`
6. Repeat
