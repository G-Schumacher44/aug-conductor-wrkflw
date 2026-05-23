# Conductor Workflow

A project-agnostic agent workflow system. Point any AI agent at this repo and it will
work in a structured, documented, handoff-safe way — regardless of what you're building.

## What Is Conductor?

Conductor is a lightweight workflow system for AI agents. It gives the agent:

- **`intent.md`** — a contract describing what you want built and why
- **`conductor/tracks.md`** — what's in progress and what's next
- **`conductor/slice-*.md`** — the current bounded unit of work, with acceptance criteria
- **`conductor/handoff-log.md`** — a written record of every session

Each session the agent reads the slice spec, does the work, and writes a handoff before stopping.
No state lives in the agent's memory — it's all in the files.

## Quick Start

1. **Fill in `intent.md`** — describe your project: what you're building, what stack, what the
   first milestone looks like.

2. **Point an agent at this directory** — open Claude Code, Gemini CLI, or Codex here.
   The agent reads `AGENTS.md`, then `conductor/index.md`, then executes the active slice.

3. **Watch it work** — the agent does the slice work and writes a handoff when done.

4. **Run the next slice** — update `conductor/tracks.md` with the next slice spec,
   start a new session.

## See It In Action

The `demo/` folder shows a complete worked example: a LookML project built on BigQuery,
using this exact Conductor workflow. You can see the filled-in intent, the slice-01 output
(generated LookML views and model), and the handoff the agent wrote when it finished.

→ Start with [`demo/README.md`](./demo/README.md)

## Repo Structure

```
intent.md              ← fill this in first
AGENTS.md              ← agent behavioral rules
conductor/
  index.md             ← agent routing entry point
  tracks.md            ← active work and roadmap
  slice-01-*.md        ← active slice spec
  handoff-log.md       ← session history
demo/                  ← worked LookML example (read-only reference)
```

## Adapting For Your Project

The only files you need to change to start a new project:

1. `intent.md` — describe your actual project
2. `conductor/slice-01-initial-bootstrap.md` — update the objective and acceptance criteria
   to match your first milestone

Everything else (the conductor spine, agent rules, handoff pattern) stays the same.
