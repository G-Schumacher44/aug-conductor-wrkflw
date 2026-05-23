# Run Demo 3 — Automated Maintenance

You are an automated maintenance agent. A cron job fired you — no human is present.
You have no session context from prior conversations. Orient yourself entirely from
the Conductor spine.

This simulates what runs nightly in production via Codex app scheduled tasks.

---

## What You're Doing

Running a routine Conductor health check on `project/`:

1. Validate the conductor spine and LookML structure
2. Verify all planned work is complete (no stuck or failed slices)
3. Surface any open blockers for the operator
4. Write a brief maintenance status entry to the handoff log
5. Commit and exit

This is read-and-report work. You do not write code, add features, or fix failures.
If you find problems, you document them — the operator decides what to do.

---

## Steps

### 1 — Orient from the spine (no session context)

Read these files in order:

1. `project/intent.md` — what this project is
2. `project/conductor/index.md` — queue state, which slices exist and their status
3. `project/conductor/handoff-log.md` — last known state and any open blockers
4. `project/conductor/slice-05-maintenance.md` — your task spec

### 2 — Create your branch

```bash
git checkout -b chore/maintenance-<YYYY-MM-DD>
```

Branch from `demo-3-start`. All commits go on this branch.

### 3 — Run the spine validator

```bash
python scripts/validate.py
```

Capture the full output. Note the pass/warn/fail counts and any specific failures.

### 4 — Check queue completeness

Read `project/conductor/index.md`. Verify:
- All slices in the queue show `STABLE`
- No slice is stuck in `ACTIVE` or `IN-PROGRESS` without a corresponding handoff entry

If any slice is not STABLE, note it as a blocker — do not attempt to fix it.

### 5 — Check for open blockers

Read `project/conductor/handoff-log.md`. Look at the **Blockers** section of the most
recent entry. Count and list any unresolved blockers.

### 6 — Write the maintenance entry

Write a new entry at the top of `project/conductor/handoff-log.md`:

```
## Maintenance Check — <YYYY-MM-DD>

Date: <today>
Commit: <7-char hash>
Type: automated-maintenance

### Status
<clean | degraded>

### Validation
- scripts/validate.py: <X passed | Y warnings | Z failed>
<list any specific failures verbatim>

### Queue State
- Slices: <N> total — <N> STABLE, <N> ACTIVE, <N> QUEUED
<list any non-STABLE slices>

### Open Blockers
- <count> open blockers from last handoff
<list each verbatim, or "None">

### Next Run
Cron-driven — operator sets schedule. No action required.
```

**Status definition:**
- `clean` — validate.py 0 failures, all slices STABLE, 0 open blockers
- `degraded` — any failures, any non-STABLE slices, or any open blockers

Move the previous handoff entry to `project/conductor/handoff-archive.md`.

### 7 — Commit

```bash
git commit -m "chore(maintenance): conductor health check <YYYY-MM-DD>"
```

---

## Rules

- Read-only investigation. Do not modify view files, model files, or slice specs.
- Do not auto-fix failures. Document them verbatim and exit.
- Do not invent context. If you don't know something, say "unknown" in the status entry.
- If validate.py exits non-zero, that is a `degraded` status — still write the entry and commit.
- No hardcoded credentials.

---

## Codex App Cron Setup (Reference)

To run this as a true automated task via the Codex desktop app:

1. Open Codex app → Settings → Scheduled Tasks
2. Create a new task:
   - **Name:** Conductor Health Check
   - **Schedule:** `0 6 * * 1` (Monday 6am) or your preferred cadence
   - **Prompt:** `Read DEMO3.md in the aug-conductor-wrkflw repo and execute it.`
   - **Repo:** point to this repo root
3. Codex fires the agent on schedule with no human intervention

The CI equivalent is `.github/workflows/conductor-maintenance.yml` — see that file for
a GitHub Actions version that runs the same validator on a schedule.

---

## What Happens Next

The maintenance entry is the artifact. The operator reviews it on their next check-in.
If status is `clean`, no action needed. If `degraded`, the operator triages the blockers
and decides whether to queue a new slice or fix the issue directly.

This is the Conductor loop in fully automated mode: the agent proposes, the operator decides.
