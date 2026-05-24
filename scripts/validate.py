#!/usr/bin/env python3
"""
Conductor spine validator — domain-agnostic, stdlib only.

Checks:
  - project/ spine structure and required files
  - handoff format (Commit:, Exact Next Steps)
  - active slice acceptance criteria checkboxes
  - CI workflow stub presence
  - git branch state

For domain-specific checks (LookML, dbt, etc.) see demo/scripts/.

Usage:
  python3 scripts/validate.py
"""

import re
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROJECT = REPO_ROOT / "project"

results = []


def check(name, fn):
    try:
        status, message, detail = fn()
        results.append({"name": name, "status": status, "message": message, "detail": detail})
    except Exception as e:
        results.append({"name": name, "status": "fail", "message": str(e), "detail": None})


# ── Spine structure ───────────────────────────────────────────────────────────

check("project/ directory", lambda: (
    ("pass", "", None) if PROJECT.exists()
    else ("fail", "not found — scaffold project/ first", None)
))

for rel in ["AGENTS.md", "intent.md", "conductor/index.md", "conductor/handoff-log.md"]:
    path = rel
    check(f"project/{rel}", lambda p=path: (
        ("pass", "", None) if (PROJECT / p).exists()
        else ("fail", "missing — scaffold incomplete", None)
    ))


# ── Handoff format ────────────────────────────────────────────────────────────

def check_handoff():
    f = PROJECT / "conductor" / "handoff-log.md"
    if not f.exists():
        return "fail", "missing", None
    content = re.sub(r"<!--.*?-->", "", f.read_text(), flags=re.DOTALL).strip()
    if len(content) < 50:
        return "warn", "appears empty — agent may not have written the handoff yet", None
    missing = []
    if "Commit:" not in content:
        missing.append("Commit:")
    if "Exact Next Steps" not in content:
        missing.append("Exact Next Steps")
    if missing:
        return "warn", f"required fields missing: {', '.join(missing)}", None
    return "pass", "", None

check("handoff-log.md written", check_handoff)


# ── CI workflow stub ──────────────────────────────────────────────────────────

def check_ci_stub():
    workflows = PROJECT / ".github" / "workflows"
    if not workflows.exists() or not any(workflows.iterdir()):
        return "warn", "no .github/workflows — stub recommended", None
    files = [f.name for f in workflows.iterdir()]
    return "pass", ", ".join(files), None

check("CI workflow stub", check_ci_stub)


# ── Active slice + acceptance criteria ───────────────────────────────────────

def get_active_slice_rel():
    index = PROJECT / "conductor" / "index.md"
    if not index.exists():
        return None
    m = re.search(r"Active slice:\s*(.+)", index.read_text(), re.IGNORECASE)
    return m.group(1).strip() if m else None


def parse_acceptance_criteria(content):
    m = re.search(r"##\s+Acceptance Criteria(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if not m:
        return []
    items = []
    for line in m.group(1).splitlines():
        ticked = re.match(r"[-*]\s+\[x\]\s+(.+)", line, re.IGNORECASE)
        open_  = re.match(r"[-*]\s+\[ \]\s+(.+)", line, re.IGNORECASE)
        if ticked:
            items.append((True, ticked.group(1).strip()))
        elif open_:
            items.append((False, open_.group(1).strip()))
    return items


active_slice_rel = get_active_slice_rel()


def check_active_slice():
    if not active_slice_rel:
        return "warn", "could not parse from conductor/index.md", None
    if active_slice_rel.lower().startswith("none"):
        return "pass", active_slice_rel, None
    if not (PROJECT / active_slice_rel).exists():
        return "fail", f"{active_slice_rel} not found", None
    return "pass", active_slice_rel, None

check("Active slice file", check_active_slice)

if active_slice_rel and not active_slice_rel.lower().startswith("none") and (PROJECT / active_slice_rel).exists():
    criteria = parse_acceptance_criteria((PROJECT / active_slice_rel).read_text())
    if criteria:
        done = sum(1 for ticked, _ in criteria if ticked)
        total = len(criteria)
        lines = "\n".join(f"       {'[x]' if t else '[ ]'} {text}" for t, text in criteria)
        results.append({
            "name": f"Acceptance criteria  {done}/{total} checked",
            "status": "pass" if done == total else "warn",
            "message": "",
            "detail": lines,
        })
    else:
        results.append({
            "name": "Acceptance criteria",
            "status": "warn",
            "message": "no checklist items found — add an Acceptance Criteria section",
            "detail": None,
        })


# ── Git branch ────────────────────────────────────────────────────────────────

def check_branch():
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=REPO_ROOT, text=True
        ).strip()
        if not branch:
            return "warn", "detached HEAD", None
        if branch in ("main", "dev"):
            return "fail", f"on {branch} — commits should go on a feature branch", None
        return "pass", branch, None
    except Exception:
        return "warn", "could not determine branch", None

check("Git branch is a feature branch", check_branch)


# ── Report ────────────────────────────────────────────────────────────────────

passed  = sum(1 for r in results if r["status"] == "pass")
warned  = sum(1 for r in results if r["status"] == "warn")
failed  = sum(1 for r in results if r["status"] == "fail")
skipped = sum(1 for r in results if r["status"] == "skip")

icons = {"pass": "✓", "warn": "~", "fail": "✗", "skip": "-"}
hr = "─" * 52

print(f"\nConductor Spine Validation\n{hr}")
for r in results:
    icon = icons.get(r["status"], "?")
    suffix = f"  — {r['message']}" if r["message"] else ""
    print(f"  {icon}  {r['name']}{suffix}")
    if r["detail"]:
        print(r["detail"])
print(hr)
print(f"  {passed} passed  |  {warned} warnings  |  {failed} failed  |  {skipped} skipped\n")

sys.exit(1 if failed > 0 else 0)
