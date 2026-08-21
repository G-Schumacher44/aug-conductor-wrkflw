# Slice 01: Initial Project Bootstrap

Date: <project-start-date>
Status: stable
Type: workflow-slice
Owner: agent

## Objective

Establish the initial project state: orient from intent, do the first bounded unit of work,
validate, and write a handoff that proposes what comes next.

Replace this section with the specific objective for your project's first slice.

## Required Reads

1. `intent.md` — project goals, constraints, entities
2. `AGENTS.md` — behavioral rules for this project
3. `conductor/index.md` — routing
4. This slice

Add any project-specific schema references, design docs, or context files here.

## Mode And Context Contract

- Mode: `slice`
- Required reads: listed above
- Forbidden reads without reason: unrelated directories, external repos
- Coordination surfaces: not required for this slice
- Tag posture: no tag — bootstrap is not a stable milestone

## Execution Steps

### Step 0 — Promote this slice to ACTIVE

Before any work: in `conductor/index.md`, set this slice's queue row `QUEUED → ACTIVE` and
set the `Active slice:` line to this slice's path. The validator only checks the acceptance
criteria of the slice named there and short-circuits when it reads `none`, so skipping this
leaves the gate checking nothing.

### Step 1 — Create your branch

```bash
git checkout -b feat/slice-01-<description>
```

All commits for this slice go on this branch. Do not commit to `main` directly.

### Step 2 — Validate intent

Read `intent.md`. Confirm all required fields are filled in — no placeholders remaining.
If anything is missing, stop and ask the operator before proceeding.

### Step 3 — Do the work

Replace this step with the specific bounded task for your slice.

Rules:
- Work only within the scope defined by this slice
- Commit after each meaningful unit: `feat(<scope>): <description>`
- Do not invent requirements — only build what is specified

### Step 4 — Write the handoff

Write an entry at the top of `conductor/handoff-log.md`:

```
## Slice 01 — Initial Bootstrap

Date: <today>
Commit: <7-char hash>

### Objective
<what this slice set out to do>

### Current State
<what was actually completed>

### Files Changed
<list of created or modified files>

### Validation
- python3 scripts/validate.py: <X passed | Y warnings | 0 failed>

### Exact Next Steps
1. <first thing the next agent or operator should do>
2. <second thing>
3. <etc>

### Blockers
<anything the operator must resolve before work can continue, or "None">
```

`Commit:` is the hash of your last work commit so far, not the handoff commit itself,
which doesn't exist yet.

### Step 5 — Tick satisfied acceptance criteria, then run the spine validator (required gate)

Go to the **Acceptance Criteria** section below and tick (`- [x]`) every item that is now
true — including "Handoff written", since Step 4 just did that.

```bash
python3 scripts/validate.py
```

This is the required gate. It runs while this slice is still `Active slice:` in
`conductor/index.md`, so it genuinely checks this slice's acceptance criteria, not a
short-circuited "none". Fix any **failures** before proceeding — warnings are acceptable,
they flag recommendations, not blocking issues. Once the run is clean, paste the real
`X passed | Y warnings | 0 failed` line into the handoff's `### Validation` field.

### Step 6 — Mark stable, advance the queue, and commit

In this file: `Status: <active>` → `Status: stable`

In `conductor/index.md`:
- Update queue row: slice-01 `ACTIVE` → `STABLE`
- Leave the next slice `QUEUED` — don't flip it to `ACTIVE` until a session actually
  starts it. Its acceptance criteria are all unchecked, so an active-but-unstarted next
  slice would fail the very validator gate this one just passed.
- Update `Active slice:` line to `none — awaiting slice-02` (or whichever slice is next)

Commit the slice doc, `conductor/index.md`, and `conductor/handoff-log.md` together:
`docs(handoff): record slice 01 completion`

## Acceptance Criteria

- [ ] Branch created from main or dev — not committed directly
- [ ] Work matches the scope defined in this slice — nothing more
- [ ] Handoff written with Commit: hash and Exact Next Steps
- [ ] No hardcoded credentials or secrets
