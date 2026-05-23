# Master Plan: [PROJECT NAME]

Date: YYYY-MM-DD
Status: active
Type: workflow-master-plan
Owner: operator

---

## Objective

[What this project is trying to achieve. What "done" looks like for the full scope.
Be specific — this is what the agent reads to understand the arc of all slices.]

---

## Phases

### Phase 1: [Name]

[Description of what this phase accomplishes.]

Slices:
- Slice 01: [Description] — `conductor/slice-01-*.md`
- Slice 02: [Description] — `conductor/slice-02-*.md`

### Phase 2: [Name]

[Description.]

Slices:
- Slice 03: [Description] — `conductor/slice-03-*.md`

---

## Architecture Decisions

[Key decisions made upfront that constrain how slices are executed.
Examples: stack choices, naming conventions, what is out of scope, known constraints.]

- Decision 1: [What and why]
- Decision 2: [What and why]

---

## Cross-Repo Dependencies

[If this project depends on or is depended on by another repo, declare it here.
Links to conductor/tracks.md entries.]

- None (standalone project)

---

## Acceptance Criteria

Full project is done when:

- [ ] [Criterion 1 — specific and verifiable]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
- [ ] All slice acceptance criteria are marked stable
- [ ] Handoff log records final state with no open blockers

---

## Slice Index

| Slice | Status | Description |
|---|---|---|
| slice-01 | queued | [Description] |
| slice-02 | queued | [Description] |
| slice-03 | queued | [Description] |

Update status column as slices complete: `queued → active → stable`
