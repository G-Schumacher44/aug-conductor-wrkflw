# Handoff Log

Newest entry at the top. Current-state handoff only; older entries live in `conductor/handoff-archive.md`.

---

## Patch — Fix demo-governance defects found by playing all three demos

Date: 2026-08-21
PR: #8 (anchor here, not a pre-squash commit hash — this repo's history already shows one
prior cleanup for exactly that mistake)
Target Branch: main
Status: STABLE
Conductor Mode: patch

### Objective
An adversarial audit played DEMO.md, DEMO2.md, and DEMO3.md end to end as a stranger's agent
would and found nine governance defects (missing tick-checkbox instruction, a circular
acceptance criterion, a gate-ordering bug that fails the demo's own correct end state, a
broken commit command, an undocumented `--health` mode, a handoff template missing a
mandated field, a stale term, an undocumented README behavior, and a missing CLI-note
preamble). Fix them without touching `scripts/validate.py`'s actual behavior — the
validator's honesty is the thing being protected, not adjusted.

### Current State
- Every project slice spec (`project/conductor/slice-01/02/03-*.md`) and the root meta
  template (`conductor/slice-01-initial-bootstrap.md`) now instruct ticking satisfied
  acceptance-criteria boxes immediately before running the validator gate, and reword the
  formerly-circular "scripts/validate.py exits 0" criterion to describe the action taken
  ("ran it and resolved every failure it reported") instead of asserting an unverified
  future result.
- slice-01 → slice-02 and slice-02 → slice-03 transitions (plus the meta template and
  `DEMO2.md`'s slice-04 → slice-05 note) now set `Active slice: none — awaiting slice-NN`
  instead of flagging an unstarted next slice `ACTIVE` — proven with a scratch copy of
  `project/` that the old pattern reproduces the reported gate failure and the new pattern
  clears it (see Validation).
- `DEMO3.md`: added the CLI-note preamble (matches DEMO2.md), pointed the gate step at
  `--health` with a one-line rationale, fixed the commit command (`git add` was missing),
  and added an `Exact Next Steps` field to the maintenance handoff template.
- Root `AGENTS.md`: fixed "Next Slice Proposal" → "Exact Next Steps" (matches `validate.py`
  and the other AGENTS.md files), and added the tick-checkbox + none-awaiting instructions
  to the Handoff Rules' end-of-slice bullets.
- `README.md`'s Validator section now documents both modes and states plainly that a fresh
  clone of `main` exits 1 by design.
- Both `conductor/index.md` files' (root meta + `project/`) end-of-slice responsibility
  lists updated to match the same tick-then-gate, none-awaiting pattern.

### Files Changed
- `AGENTS.md`
- `DEMO.md`
- `DEMO2.md`
- `DEMO3.md`
- `README.md`
- `conductor/index.md`
- `conductor/slice-01-initial-bootstrap.md`
- `project/conductor/index.md`
- `project/conductor/slice-01-lookml-bootstrap.md`
- `project/conductor/slice-02-view-enrichment.md`
- `project/conductor/slice-03-model-layer.md`
- `conductor/handoff-log.md` (this entry)

### Validation
- `python3 scripts/validate.py` (real repo, this branch, unchanged demo-start state):
  8 passed | 2 warnings | 1 failed, exit 1 (expected — slice-01 hasn't actually been run
  in this session; the one failure is the pre-existing unchecked-criteria state)
- `python3 scripts/validate.py --health` (same state): 8 passed | 3 warnings | 0 failed, exit 0
- Gate-ordering fix, proven via `CONDUCTOR_PROJECT_ROOT` pointed at a scratch copy of
  `project/` (no real repo files touched) simulating slice-01 finished, all 8 boxes ticked:
  - old buggy pattern (`Active slice:` → slice-02 directly): 8 passed | 2 warnings | 1 failed,
    exit 1 — reproduces the reported bug exactly
  - fixed pattern (`Active slice: none — awaiting slice-02`, real commit hash `f8a1fb3`):
    10 passed | 0 warnings | 0 failed, exit 0
- `cd scripts && python3 -m pytest test_validate.py -q`: 13 passed in 0.89s (unchanged from
  baseline — `scripts/validate.py` itself was not touched)
- Pre-PR `koa review --branch` ritual: blocked by the sandbox's network allowlist
  (`api.anthropic.com` / `github.com` both denied); disclosed in PR #8 under "Pre-gate:
  unresolved findings" rather than silently skipped. Report saved at
  `/tmp/claude-501/koa-locks/koa-review-branch-_Volumes_t9_dev_git_repos_aug-conductor-wrkflw-8e57f239.json`.

### Exact Next Steps
1. Operator: review and merge PR #8 (CI's own `review-gate.yml` will run with real network
   access, unlike this session's sandboxed local attempt).
2. Operator: decide whether to also fix the demo-branch-only defects noted in the PR body
   (`demo-2-start:project/conductor/slice-04-promotions-view.md` has the identical circular
   "scripts/validate.py exits 0" criterion, with no tick-checkbox instruction anywhere on
   that branch) — that's a separate operator-decision workstream per this dispatch's hard
   rule against touching `demo-2-start`/`demo-3-start`.
3. Next time an agent actually runs Demo 1 for real, confirm the fixed slice-01 spec
   produces a clean non-simulated `validate.py` run end to end (this session only proved it
   via a scratch-copy simulation, not a live Demo 1 execution).

### Blockers
- None.

---

## Patch — Wire review-pantheon gate (Way C) + cross-repo pairing docs

Date: 2026-08-09
PR: #6 (squash-merges to main — the durable anchor; pre-squash work commits are only
reachable via the PR's own refs, so no raw intermediate hash is recorded here)
Target Branch: main
Status: STABLE
Conductor Mode: patch

### Objective
Make this repo the first public adopter of review-pantheon's PR gate, so its and
review-pantheon's mutual "pairs with" story is literally true rather than aspirational.

### Current State
- `.github/workflows/review-gate.yml` added from review-pantheon v1's
  `examples/review-gate.yml` (Way C install — fetched via
  `gh api repos/G-Schumacher44/review-pantheon/contents/examples/review-gate.yml?ref=v1`) —
  byte-verbatim except one added first line marking it as the installed copy (a gate finding
  on this very PR: the upstream header's "copy to .github/workflows/" instruction read as
  confusing in-place). `REVIEW_GATE_ENABLED` and `CLAUDE_CODE_OAUTH_TOKEN` were both
  configured on the repo before this PR merged — **this PR itself was the gate's first live
  run** (verdict posted by the review-pantheon action: artemis SHIP / apollo
  ACCEPT-WITH-NOTES, whose notes are addressed in this same PR).
- README gained a "Works with review-pantheon" section, mirroring review-pantheon's own
  "Works with Conductor" section in its README (fetched at the `v1` tag for this session).
- `conductor/AGENTS.md`'s "include validation gates" workflow rule now names a concrete,
  optional example (`pantheon gate --branch` pre-PR / the Action on the PR) — Conductor
  itself stays gate-agnostic. Root `AGENTS.md` has no matching validation-gates rule to
  update, but it WAS edited later in this PR for a different reason: its Handoff Rules'
  `Commit:` field gained the squash-merge exception (anchor on PR #N; never record a hash
  the reviewed history won't contain), after the gate + Codex both flagged this entry's
  original pre-squash hash anchor.
- `conductor/tracks.md`'s registry gained a real entry for the review-pantheon pairing —
  recorded as a non-blocking verification track (not the artifact-blocking shape the file's
  worked example describes), since no slice here blocks on review-pantheon's state.

### Files Changed
- `.github/workflows/review-gate.yml` (new)
- `README.md`
- `AGENTS.md` (Handoff Rules: squash-merge exception added to the `Commit:` field)
- `conductor/AGENTS.md`
- `conductor/tracks.md`
- `conductor/handoff-log.md` (this entry; superseded Slice-01 entries moved out per the
  current-state-only rule)
- `conductor/handoff-archive.md` (received the two moved Slice-01 entries)
- `project/AGENTS.md` (review round: the scoped Commit rule gained the same squash-merge
  exception as root, so validate.py's PROJECT checks police a rule that actually permits
  what the code accepts)
- `scripts/validate.py` (review round: accepts the PR-anchor form, field-anchored regex)
- `scripts/test_validate.py` (review round: two new tests, registered in BOTH entrypoints —
  pytest and the standalone `tests` list)

### Validation (re-run after the review-round edits, same session that wrote this entry)
- `python3 scripts/validate.py --health` — 8 passed, 3 warnings, 0 failed, exit 0 (warnings
  are the documented project/-state ones, unrelated to this change)
- `python3 scripts/validate.py` — 8 passed, 2 warnings, 1 failed, exit 1: the failure is the
  demo slice's deliberately-unchecked acceptance criteria, pre-existing on pristine `main`
  (verified in a clean worktree: main is 7 passed / 3 warnings / 1 failed — this branch
  passes one MORE check than main; the slice-01-CLOSED entry, now in
  `conductor/handoff-archive.md`, documents the by-design failure); unrelated to this change
- `cd scripts && python3 -m pytest test_validate.py -q` — 13 passed (11 at this entry's first
  writing; this PR's review rounds added two tests covering validate.py's new PR-anchor
  exception, both also registered in the file's standalone `tests` list — the gate's apollo
  caught BOTH the stale count and the unregistered tests in one blocker, which is exactly the
  job this PR wires him up to do)
- `.github/workflows/review-gate.yml` parses as YAML (`yaml.safe_load`)
- Every relative/absolute link added in this session resolves: `.github/workflows/review-gate.yml`
  exists, the README's `#works-with-review-pantheon` anchor exists, `conductor/AGENTS.md`'s
  `../.github/workflows/review-gate.yml` link resolves, and
  `gh api repos/G-Schumacher44/review-pantheon/contents/docs/SETUP.md` / `.../README.md`
  both resolve at the `main`/`v1` refs referenced

### Exact Next Steps
1. Merge PR #6. The gate is already live — it ran on this PR and posted its verdict.
2. Future PRs here get gated automatically; findings follow review-pantheon's
   fix-or-track discipline.

### Blockers
- None.

---
