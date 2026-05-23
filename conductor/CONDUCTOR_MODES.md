# Conductor Modes

Choose the smallest mode that fits the work. Wider modes cost more context and time.

---

## Patch Mode

**When:** Small fix, config change, doc update, or UI polish. No new architectural decisions.

**Context to load:** AGENTS.md + the specific file(s) being changed. That's it.

**No slice doc required.** Commit directly to a fix branch.

**Handoff:** Optional for patches under 30 minutes. Required if the patch touches a seam
or leaves something unfinished.

---

## Slice Mode (Default)

**When:** Planned, bounded implementation work. A slice spec exists or will be written first.

**Context to load:**
1. `AGENTS.md`
2. `conductor/index.md`
3. `conductor/tracks.md`
4. The active `conductor/slice-*.md`
5. Latest `conductor/handoff-log.md` entry
6. Direct target files for the slice

**Slice doc required** before writing code. The slice defines scope, acceptance criteria,
and what is explicitly out of scope.

**Handoff required** at the end of every slice session.

---

## Audit Mode

**When:** Read-only review. Assessing the current state before deciding what to build.

**Context to load:** Whatever is relevant to the audit question. No writes.

**Output:** A written audit report or a set of handoff notes. No code changes.

---

## Full Conductor Mode

**When:** Cross-cutting changes — root docs, authority changes, release preparation,
or work that touches multiple tracks simultaneously.

**Context to load:** Everything relevant. Start with `conductor/index.md` and expand
from there.

**Requires operator approval** before starting if the change touches `AGENTS.md`,
`conductor/index.md`, or `conductor/tracks.md`.
