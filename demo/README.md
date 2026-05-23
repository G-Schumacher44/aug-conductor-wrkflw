# Demo: Building a LookML Project with Conductor

This folder shows a complete worked example of the Conductor workflow in action.

**The setup:** A BigQuery gold mart (`gcs-automation-project.gold_marts`) with 8 fact tables
covering an e-commerce business — revenue, sales operations, customer segments, product
profitability, marketing attribution, shipping, cart abandonment, and a daily dashboard.

**The task:** Use Conductor to guide an agent through building a LookML data model on top
of those tables.

---

## What Happened (Step by Step)

### 1. Operator filled in `intent.md`

The operator opened `intent.md` and described the project: BQ project ID, dataset name,
key entities, relationships, and what a "done" first slice looks like.

See the filled-in version: [`demo/intent-example.md`](./intent-example.md)

### 2. Agent read the Conductor spine

The agent opened the repo and read:
- `AGENTS.md` — behavioral rules and handoff requirements
- `conductor/index.md` — active slice routing
- `conductor/slice-01-initial-bootstrap.md` — the current unit of work

### 3. Agent executed the slice

Following the slice spec, the agent:
1. Validated `intent.md` — confirmed BQ project, dataset, and entities were declared
2. Read `demo/schema/gold_marts.md` — the authoritative schema reference (no BQ access required)
3. Generated one `.view.lkml` file per table
4. Created `models/gold_marts.model.lkml` with explores for each primary entity
5. Wrote a handoff log entry before stopping

### 4. Output produced

The views and model the agent generated are in:
- [`demo/views/`](./views/) — one file per BQ table
- [`demo/models/gold_marts.model.lkml`](./models/gold_marts.model.lkml)

The handoff the agent wrote is in:
- [`demo/handoff-example.md`](./handoff-example.md)

---

## What You're Actually Seeing — The Conductor Loop

Open [`demo/handoff-example.md`](./handoff-example.md) and scroll to **Next Slice Proposal**.

That section was written by the agent — not the operator. The agent built slice 01, then
proposed slices 02–04 in the handoff. The operator's only job after slice 01 was to read
that proposal and decide whether to promote it to the next slice spec.

**This is the Conductor Loop:**

```
operator sets intent → agent reads slice → agent executes → agent writes handoff
       ↑                                                              ↓
operator approves ←←←←← Next Slice Proposal ←←←←←←←←←←←←←←←←←←←←←←
```

The agent is scheduling its own next unit of work. The operator approves or redirects.
No scope is generated from scratch after the first slice — the agent proposes it.

→ See [`demo/LOOP.md`](./LOOP.md) for a full walkthrough of the loop mechanics.

---

## Try It Yourself

1. Copy `demo/intent-example.md` content into the root `intent.md` — or write your own
2. Point an agent (Claude Code, Gemini CLI, Codex) at the repo root
3. The agent will execute `conductor/slice-01-initial-bootstrap.md`
4. Watch it build, then read the handoff it writes

To use your own BQ data: update `intent.md` with your GCP project ID, dataset, and entities.
The agent will discover your schema and generate your views.
