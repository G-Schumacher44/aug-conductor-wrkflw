# LookML Tooling Reference

**For:** Engineering / Platform team — tool evaluation and CI/CD pipeline planning
**Context:** This demo runs without a live Looker or BigQuery connection. Tools are grouped
by whether they require one.

---

## Summary Matrix

| Tool | Provider | Offline? | Purpose | License | Stars | Monthly Downloads |
|---|---|---|---|---|---|---|
| VS Code Extension | Google / Looker (official) | Partial | IDE syntax + validation | Proprietary | N/A | N/A |
| LAMS | looker-open-source (Looker OSS org) | ✅ Yes | Style guide linter | MIT | 138 | N/A |
| `lkml` | Josh Temple (community) | ✅ Yes | Syntax parser / validator | MIT | 185 | ~1.1M |
| Spectacles | spectacles-ci (community) | ❌ No | CI test suite | MIT | 225 | ~60K |

---

## 1. Official VS Code Extension

**Publisher:** Looker (Google)
**Extension ID:** `Looker.lkml`
**Install from:** VS Code Marketplace → search "LookML"

The official editor integration maintained by Looker/Google. Most authoritative option for
developer environments.

### What it does
- LookML syntax highlighting
- Field and view auto-completion
- Inline validation and error highlighting (requires active Looker connection for full validation)
- Jump-to-definition for views and explores
- Offline: syntax highlighting and basic structural checks only

### Requirements
- VS Code
- Full validation requires a configured Looker connection (Looker API credentials)
- Offline mode provides syntax highlighting without a connection

### Notes for this demo
Useful for developers writing LookML in VS Code. For automated/headless validation without
a connection, use `lkml` or LAMS instead.

---

## 2. LAMS — Look At Me Sideways

**Repo:** https://github.com/looker-open-source/look-at-me-sideways
**Publisher:** `looker-open-source` GitHub organization (Looker's open-source org)
**Explicitly NOT officially supported by Looker** — issues go to GitHub, not Looker support
**License:** MIT
**Stars:** 138
**Offline:** ✅ Yes — reads LookML files locally, no Looker instance required

### What it does

Style guide enforcement and linting. 20+ built-in rules covering:
- Primary key naming conventions
- Field organization and grouping
- Join relationship hygiene
- Hidden field conventions
- Measure/dimension type discipline

Output formats: CLI table, markdown, GitHub Actions job summary.
Designed to run in CI/CD pipelines on every PR.

### Installation

```bash
npm install -g @looker/look-at-me-sideways
lams --source="path/to/lookml/project"
```

### When to use

Enforcing team LookML standards in CI before code reaches a Looker instance.
Catches style and convention violations that `lkml` (syntax-only) would miss.

### Notes for this demo

LAMS is the most appropriate offline linter for enforcing LookML conventions at scale.
Because it comes from Looker's own open-source GitHub org, it carries more organizational
weight than community tools when seeking internal approval — despite not being "officially
supported" by Looker engineering.

---

## 3. `lkml` — LookML Parser

**Repo:** https://github.com/joshtemple/lkml
**Publisher:** Josh Temple (community)
**License:** MIT | **Stars:** 185 | **Monthly downloads:** ~1.1M
**Offline:** ✅ Yes

Covered in detail in [`lkml-validator.md`](./lkml-validator.md).

**One-line summary:** Pure Python syntax validator. No connection. Parses one file at a time.
Exit 0 = valid syntax. The highest-adoption LookML tool by download volume.

---

## 4. Spectacles

**Repo:** https://github.com/spectacles-ci/spectacles
**Publisher:** spectacles-ci (community organization)
**License:** MIT | **Stars:** 225 | **Monthly downloads:** ~60K
**Latest:** v2.4.17 (November 19, 2025)
**Offline:** ❌ No — requires Looker API access

### What it does

The community-standard CI test suite for Looker. Runs four validator types against a
live Looker instance:

| Validator | What it checks |
|---|---|
| LookML | Looker's native LookML parser (errors Looker itself would catch) |
| SQL | Every dimension and measure generates valid SQL against the database |
| Assert | Looker data tests defined in your project |
| Content | Looks and dashboards reference valid fields |

### Installation

```bash
pip install spectacles
spectacles connect --base-url https://your.looker.com --client-id ... --client-secret ...
spectacles lookml --project your_project
spectacles sql --project your_project --explore fct_finance_revenue
```

### When to use

Post-deployment validation in CI/CD. Runs after LookML is pushed to Looker and a
connection is active. The SQL validator is particularly valuable — it catches broken
field references and type mismatches that no offline tool can detect.

### Notes for this demo

Not applicable for the offline demo. The correct production pipeline is:
1. `lkml` — syntax check (offline, every commit)
2. LAMS — style/convention check (offline, every PR)
3. Spectacles LookML validator — Looker-native parse check (requires connection)
4. Spectacles SQL validator — end-to-end SQL validation (requires connection + BQ)

---

## Recommended Pipeline (When Connection Is Available)

```
commit → lkml (syntax) → LAMS (style) → PR merge
                                              ↓
                                    Spectacles lookml (Looker parse)
                                    Spectacles sql (BQ validation)
                                              ↓
                                         production
```

## For This Demo (No Connection)

```
commit → lkml (optional, if approved) → LAMS (optional, if approved) → handoff
```

Validation is deferred to the Looker IDE when a connection is provisioned.
