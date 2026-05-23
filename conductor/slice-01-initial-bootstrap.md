# Slice 01: Initial Project Bootstrap

Status: active
Type: workflow-slice
Owner: agent

```yaml
conductor_mode: slice
context_budget: medium
handoff_required: true
```

## Objective

Read `intent.md`, set up the foundational project structure for the declared stack,
and leave the repository in a buildable, runnable state. Write a handoff when done.

## Required Reads

1. `intent.md` — stack, entities, definition of done
2. `AGENTS.md` — execution and handoff rules
3. `conductor/index.md`
4. This slice

## Execution Steps

### Step 1 — Validate Intent

Read `intent.md`. Confirm the stack is declared and the definition of done is filled in.
If placeholders remain, stop and ask the operator to complete `intent.md` before proceeding.

### Step 2 — Bootstrap Project Structure

Based on the declared stack in `intent.md`, create the foundational project files:

- Package manifest or dependency file (`package.json`, `requirements.txt`, `go.mod`, etc.)
- Entry point file (`index.ts`, `main.py`, `main.go`, etc.)
- Config files appropriate to the stack (`.gitignore`, `tsconfig.json`, `Makefile`, etc.)
- Any directory structure needed (`src/`, `tests/`, etc.)

Do not install packages yet — just write the manifests.

### Step 3 — Verify

Confirm the project is in a valid starting state:
- No syntax errors in generated files
- Build or lint passes if applicable
- Git status is clean after committing bootstrap files

### Step 4 — Write Handoff

Write a `conductor/handoff-log.md` entry at the top of the file recording:
- What was bootstrapped (files created)
- Validation result
- What is next (recommended Slice 02 objective)
- Any open questions for the operator

## Acceptance Criteria

- [ ] `intent.md` has no unfilled placeholders
- [ ] Project has a functional, stack-appropriate baseline structure
- [ ] Handoff log entry written with next steps
- [ ] No sensitive values (API keys, passwords) committed

## Out of Scope

- Installing dependencies (that's Slice 02)
- Writing application logic (that's Slice 03+)
- Database migrations or schema setup
