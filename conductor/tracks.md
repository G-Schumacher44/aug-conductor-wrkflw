# Conductor Track Registry

Status: active
Type: track-registry

## About This File

`tracks.md` records cross-repo dependencies so agents know what they're blocked on
and what they're unblocking. It is only relevant in multi-repo setups.

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

This repo has no artifact-producing upstream/downstream dependency in the sense the example
above describes — no other repo's slice blocks on this one, and this repo's slices don't block
on an artifact from elsewhere. It does have one cross-repo tooling pairing, recorded below in
the same shape: a planning↔verification pairing rather than an artifact-blocking one, so
"Blocking slice" is n/a and a red status here never stops a slice from advancing.

| Repo | Role | Provides | Tracks status |
|------|------|----------|----------------|
| [review-pantheon](https://github.com/G-Schumacher44/review-pantheon) | verification pairing (non-blocking) | Artemis/Apollo PR gate on this repo's own pull requests (`.github/workflows/review-gate.yml`) | LIVE — `CLAUDE_CODE_OAUTH_TOKEN` + `REVIEW_GATE_ENABLED` are configured; first gated PR was #6 (the PR that installed it) |

This repo is also review-pantheon's own documented "Works with Conductor" example — its README
names aug-conductor-wrkflw as the repo that pairs with it: Conductor plans the work (slices,
handoffs), review-pantheon verifies the delivery and pressure-tests the plan before it's built.
See the README's [Works with review-pantheon](../README.md#works-with-review-pantheon) section
here for the mirror of that pairing.
