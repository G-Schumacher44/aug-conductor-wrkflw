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

### Review round — four unresolved PR #8 threads fixed
1. **Gate-ordering circularity survived one level down (Codex, blocker).** The first pass
   put "tick criteria, then run the gate" before the step that writes the handoff — but
   every slice's criteria list included a "Handoff written" item, which can't be honestly
   true until the handoff step, which ran *after* the gate. Reordered every slice
   spec (project slice-01/02/03 + the root meta template) to: do the work → **write the
   handoff** → tick every satisfied criterion (now including "handoff written") → **run
   the required gate** (slice still `ACTIVE`, so it's a real check, not short-circuited by
   `Active slice: none`) → mark stable + advance the queue. Also deleted the
   self-referential "ran `scripts/validate.py` ... and resolved every failure it reported"
   criterion (the passing gate is the evidence) and, in slice-02/03, the equally circular
   "slice marked stable / queue advanced" criteria (those are post-gate actions by the new
   ordering, so they can never be honestly true while the gate that checks them is still
   running). `conductor/index.md` (root + `project/`) end-of-slice lists and `AGENTS.md`'s
   Handoff Rules updated to match. `DEMO.md`'s two prose references to slice-01's order
   updated; no file anywhere references these steps by number outside each slice's own
   now-removed self-reference (grepped the full repo to confirm). `DEMO3.md` left untouched.
   **Superseded later in this same PR (Apollo, round 3):** `DEMO2.md` WAS left untouched as
   of `838f223` on the reasoning below, but Codex then showed its steps 6/7 carried the same
   gate-before-handoff circularity in their own narration — independent of which branch
   slice-04 lives on — so `15eebd1` rewrote them to the handoff-then-gate order and dropped
   the self-referential instruction. What remains genuinely out of scope is slice-04's own
   criteria list, which lives only on `demo-2-start` and belongs to the demo-branch rebuild
   workstream. The original reasoning, kept so the scope call is auditable: `DEMO2.md`
   narrates `demo-2-start`'s slice-04, out of scope per this dispatch's hard rule and the
   prior PR's own "separate operator-decision workstream" call.
2. **False credential-check guarantee (Codex, highest priority).** `README.md` claimed
   `--health` mode still fails "credential checks" for real problems. `scripts/validate.py`
   has no credential-scanning code at all — "No hardcoded credentials" is one manually-ticked
   acceptance-criteria checkbox among others, and in `--health` mode the whole
   acceptance-criteria line (including that box) is downgraded to a warning. Removed the
   false claim and added an explicit paragraph stating the validator does not scan file
   contents for secrets. Grepped the full PR diff for every other capability claim added
   (the `--health`/default-mode split, the "fresh clone of `main` exits 1" claim) and
   verified each against `scripts/validate.py`'s actual behavior by running it (see
   Validation) — both check out.
3. **Superseded handoff entry not archived (CodeRabbit, major).** The first pass's edit to
   `conductor/handoff-log.md` was purely additive — it inserted the new PR #8 entry above
   the old "Patch — Wire review-pantheon gate (Way C)..." entry instead of moving it out,
   violating the file's own current-state-only rule. Moved that entry verbatim to the top
   of `conductor/handoff-archive.md` (ahead of the existing "Slice 01 — CLOSED" entry) and
   added `conductor/handoff-archive.md` to this entry's Files Changed.
4. **"Required gate" wording not scoped to the demos that use it (CodeRabbit, minor).**
   `README.md` called the plain `scripts/validate.py` invocation "the demos' required
   gate" — but `DEMO3.md` requires `--health`. Reworded both mode-comment lines: default
   mode is Demo 1 and Demo 2's required gate; `--health` is Demo 3's.

### Files Changed
- `AGENTS.md`
- `DEMO.md`
- `DEMO2.md`
- `DEMO3.md`
- `README.md`
- `conductor/index.md`
- `conductor/slice-01-initial-bootstrap.md`
- `project/conductor/index.md`
- `scripts/validate.py` — module docstring only, no behavior change (round 3: its own
  docstring was the source of the false "handoff format ... and credentials are still
  enforced" claim the README had copied)
- `project/conductor/slice-01-lookml-bootstrap.md`
- `project/conductor/slice-02-view-enrichment.md`
- `project/conductor/slice-03-model-layer.md`
- `conductor/handoff-log.md` (this entry)
- `conductor/handoff-archive.md` (archived the superseded PR #6 entry, which this PR's
  first pass left sitting below the current-state entry in violation of the log's own
  current-state-only rule)

### Validation
- `python3 scripts/validate.py` (real repo, this branch, unchanged demo-start state, this
  session): `8 passed | 2 warnings | 1 failed`, exit 1 — expected; slice-01 is still 0/7
  unticked (Demo 1's real starting state, unchanged by this review round)
- `python3 scripts/validate.py --health` (same state, this session): `8 passed | 3 warnings
  | 0 failed`, exit 0
- **Gate-ordering fix, re-verified this session** for the reordering above, via
  `CONDUCTOR_PROJECT_ROOT` pointed at a scratch copy of `project/` (no real repo files
  touched) simulating slice-01 finished under the *new* step order — handoff written
  first (real reachable commit hash `8b22472`), then all 7 (post-deletion) criteria
  ticked, `Active slice:` left pointing at slice-01 (still `ACTIVE`, not short-circuited),
  then the gate run:
  ```
  ✓ handoff-log.md written
  ✓ Handoff commit hash is real — 8b22472
  ✓ Acceptance criteria  7/7 checked
  ✓ Git branch is a feature branch — fix/demo-governance-defects
  11 passed  |  0 warnings  |  0 failed  |  0 skipped
  ```
  exit 0 — every criterion honestly tickable, slice genuinely `ACTIVE` throughout, gate
  passes for real. Same pattern applies to slice-02/03 and the root meta template (same
  reorder, same criteria deletions); not independently re-simulated this session since the
  shape and the validator's parsing logic are identical.
- `cd scripts && python3 -m pytest test_validate.py -q`: `13 passed in 0.85s` this session
  (unchanged count from baseline — `scripts/validate.py` itself was not touched, per the
  hard rule protecting the validator's honesty)

### Exact Next Steps
1. Operator: merge PR #8 once the four review threads above are confirmed resolved.
2. Operator: decide whether to also fix the demo-branch-only defects noted below (unchanged
   from the prior round, still deferred):
   `demo-2-start:project/conductor/slice-04-promotions-view.md` has the identical circular
   "scripts/validate.py exits 0" criterion, with no tick-checkbox instruction anywhere on
   that branch — separate operator-decision workstream per this dispatch's hard rule
   against touching `demo-2-start`/`demo-3-start`.
3. Next time an agent actually runs Demo 1 for real, confirm the reordered slice-01 spec
   produces a clean non-simulated `validate.py` run end to end (this session only proved it
   via a scratch-copy simulation, not a live Demo 1 execution).

### Blockers
- None.

---
