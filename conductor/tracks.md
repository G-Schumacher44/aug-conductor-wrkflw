# Conductor Track Registry

Status: active
Type: track-registry

## About Tracks

Tracks let multiple repos coordinate without merging codebases. Each repo has its own
`conductor/` directory with its own slice queue. `tracks.md` records cross-repo
dependencies so agents know what they're blocked on and what they're blocking.

The pattern: upstream repos declare what they produce; downstream repos declare what
they're waiting for. Agents read both before marking a slice stable.

---

## Worked Example — Analytics Pipeline

Below is a representative three-repo cross-repo setup. Use this as a template.

```
analytics-pipeline/          ← produces: dbt gold models
  conductor/tracks.md        ← upstream of: reporting-dashboard
  conductor/index.md

reporting-dashboard/         ← consumes: gold models / produces: embed package
  conductor/tracks.md        ← downstream of: analytics-pipeline
                             ← upstream of: client-portal
  conductor/index.md

client-portal/               ← consumes: embed package
  conductor/tracks.md        ← downstream of: reporting-dashboard
  conductor/index.md
```

### analytics-pipeline/conductor/tracks.md

```markdown
## Upstream of

| Repo               | Artifact                  | Status  |
|--------------------|---------------------------|---------|
| reporting-dashboard | gold_marts dbt models     | STABLE  |
```

### reporting-dashboard/conductor/tracks.md

```markdown
## Upstream of

| Repo          | Artifact                    | Status  |
|---------------|-----------------------------|---------|
| client-portal | embed package v2            | ACTIVE  |

## Downstream of

| Repo               | Artifact               | Blocking slice |
|--------------------|------------------------|----------------|
| analytics-pipeline | gold_marts dbt models  | slice-04       |
```

### client-portal/conductor/tracks.md

```markdown
## Downstream of

| Repo                | Artifact          | Blocking slice |
|---------------------|-------------------|----------------|
| reporting-dashboard | embed package v2  | slice-07       |
```

### How an agent uses tracks.md

Before marking a slice stable, the agent reads `conductor/tracks.md` and checks:

1. Are all "Downstream of" entries STABLE? If not, the slice is blocked — record the
   blocker in `handoff-log.md` under `Blockers:` and stop.
2. After marking stable, surface this in `handoff-log.md` so downstream agents know
   they can unblock.

---

## This Repo

This repo is a standalone scaffold demo — no cross-repo dependencies. The registry
below is a scaffold stub; replace it with your own repos when adapting.

### Active Initiatives

| Repo | Role | Status |
|------|------|--------|
| aug-conductor-wrkflw (this repo) | standalone demo | active |

### Registry Rules

- One active slice at a time unless explicitly parallelized in the slice spec.
- When a slice completes: move it to `review/` or `archive/`, update this file.
- When starting the next slice: create the slice doc, update `index.md`, update this file.
- When a cross-repo dependency resolves: update the status column here and in `handoff-log.md`.
