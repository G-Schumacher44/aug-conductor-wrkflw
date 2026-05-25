# Conductor Track Registry

Status: active
Type: track-registry

## About This File

`tracks.md` records cross-repo dependencies so agents know what they're blocked on
and what they're unblocking. It is only relevant in multi-repo setups — this demo
repo is standalone, so the registry below is empty.

---

## How It Works

Each repo has its own `conductor/` directory and slice queue. When a slice in repo A
produces an artifact that repo B depends on, both repos declare the dependency here:

- **Upstream repo** lists what it produces and who it feeds
- **Downstream repo** lists what it's waiting for and which slice is blocked

An agent reads `tracks.md` before marking a slice stable. If a dependency isn't
resolved, it records the blocker in `handoff-log.md` and stops — it does not
auto-advance.

---

## Example — LookML project + dbt upstream

If this repo's LookML views were generated from dbt gold models owned by a separate
repo, tracks.md in each repo would look like this:

**dbt-gold-models/conductor/tracks.md**
```
## Downstream dependents
| Repo                  | Waiting for          | Their blocking slice |
|-----------------------|----------------------|----------------------|
| lookml-gold-marts     | gold_marts models    | slice-01             |
```

**this repo / conductor/tracks.md**
```
## Upstream dependencies
| Repo             | Artifact          | Status  | Blocking slice |
|------------------|-------------------|---------|----------------|
| dbt-gold-models  | gold_marts models | STABLE  | slice-01       |
```

Once the dbt repo marks the artifact STABLE, this repo's agent can unblock and proceed.

---

## Registry (this repo)

This repo is standalone — no cross-repo dependencies.

| Repo | Role | Tracks status |
|------|------|---------------|
| aug-conductor-wrkflw (this repo) | standalone demo | no external dependencies |
