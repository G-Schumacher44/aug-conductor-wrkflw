# Tool Evaluation Brief — lkml

**For:** Engineering / Platform team review before production use
**Decision required:** Approve for local dev use, CI/CD pipelines, or defer to Looker IDE validation only

---

## What It Is

`lkml` is an open-source LookML parser and syntax validator implemented in pure Python.
It parses `.view.lkml` and `.model.lkml` files and validates their syntax without
requiring a Looker instance, database connection, or network access.

It does **not** validate SQL correctness or field references against a live database.
That validation requires the Looker IDE connected to BigQuery.

---

## Provenance

| Field | Detail |
|---|---|
| Author | Josh Temple ([@joshtemple](https://github.com/joshtemple)) |
| Repository | https://github.com/joshtemple/lkml |
| License | MIT |
| Language | Python 3.7+ |
| External dependencies | None |
| Latest release | v1.3.7 (January 31, 2025) |
| Total releases | 20 |
| GitHub stars | 185 |
| Total commits | 468 |

---

## Adoption Signal

| Metric | Value (as of May 2026) |
|---|---|
| PyPI downloads — last day | ~36,500 |
| PyPI downloads — last week | ~249,600 |
| PyPI downloads — last month | ~1,107,000 |

Monthly download volume in the 1M+ range indicates broad adoption across the Looker
developer ecosystem. The package is widely used in CI/CD pipelines at Looker shops.

---

## What It Does and Does Not Do

| Capability | Supported |
|---|---|
| LookML syntax validation | ✅ |
| Parse view, model, explore blocks | ✅ |
| Offline / no network required | ✅ |
| No Looker license required | ✅ |
| SQL correctness validation | ❌ requires live connection |
| Field reference validation | ❌ requires live connection |
| PDT / derived table execution | ❌ requires live connection |

---

## Installation

```bash
pip install lkml
```

No system dependencies. Works in virtualenvs, Docker containers, and CI runners.

## Usage

```bash
# Validate a single file
lkml views/fct_finance_revenue.view.lkml

# Validate all views
lkml views/*.view.lkml

# Validate model file
lkml models/gold_marts.model.lkml
```

Exit code 0 = valid syntax. Non-zero = parse error with file and line number.

---

## Security Considerations

- MIT license — permissive, no copyleft restrictions
- No network calls — runs entirely locally
- No data access — reads only the `.lkml` files you point it at
- No telemetry or usage reporting
- Source code is fully auditable at https://github.com/joshtemple/lkml

---

## Alternatives

| Option | Requires |
|---|---|
| `lkml` (this tool) | Python, pip |
| Looker IDE linter | Active Looker instance + connection |
| `lookml-tools` (Wil Gieseler) | Python, broader feature set, heavier |
| Manual review | No tooling — error-prone at scale |

---

## Recommendation For This Demo

`lkml` is optional in this workflow. If your environment does not approve it:

1. Skip the validation step in the agent's slice execution
2. Note it as a blocker in the handoff
3. Use Looker IDE validation as the gate when a connection is provisioned

The demo is designed to run without it — it is a quality-of-life check, not a hard dependency.
