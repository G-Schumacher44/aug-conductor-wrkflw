#!/usr/bin/env python3
"""
Conductor spine validator — agnostic to workflow type.

Tier 1: Conductor governance checks (always runs, zero dependencies)
  - project/ spine structure
  - handoff format (Commit:, Next Slice Proposal)
  - active slice acceptance criteria checkboxes
  - git branch state

Tier 2: Simulated CI — structural LookML shape checks (no external tooling required)
  - view files: view block, sql_table_name, dimensions, count measure
  - model file: connection, explore blocks
  Runs when project/views/ and project/models/ exist.
  Records NOT RUN for any check that requires external tooling (lkml, LAMS, Spectacles).

Usage:
  python scripts/validate.py
"""

import os
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


# ── Tier 1: Conductor spine ──────────────────────────────────────────────────

check("project/ directory", lambda: (
    ("pass", "", None) if PROJECT.exists()
    else ("fail", "not found — scaffold project/ first", None)
))

for rel in ["AGENTS.md", "intent.md", "conductor/index.md", "conductor/handoff-log.md"]:
    path = rel  # capture for closure
    check(f"project/{rel}", lambda p=path: (
        ("pass", "", None) if (PROJECT / p).exists()
        else ("fail", "missing — scaffold incomplete", None)
    ))


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
    if "Next Slice Proposal" not in content:
        missing.append("Next Slice Proposal")
    if missing:
        return "warn", f"required fields missing: {', '.join(missing)}", None
    return "pass", "", None


check("handoff-log.md written", check_handoff)


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
    m = re.search(r"##\s+Acceptance Criteria(.*?)(?=\n##|$)", content, re.DOTALL | re.MULTILINE)
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
    if not (PROJECT / active_slice_rel).exists():
        return "fail", f"{active_slice_rel} not found", None
    return "pass", active_slice_rel, None


check("Active slice file", check_active_slice)

if active_slice_rel and (PROJECT / active_slice_rel).exists():
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


# ── Tier 2: Simulated CI — LookML structural checks ─────────────────────────

views_dir = PROJECT / "views"
models_dir = PROJECT / "models"

if views_dir.exists() or models_dir.exists():

    def check_views_structure():
        if not views_dir.exists():
            return "fail", "project/views/ not found", None
        view_files = list(views_dir.glob("*.view.lkml"))
        if not view_files:
            return "fail", "no .view.lkml files found", None
        issues = []
        for vf in view_files:
            content = vf.read_text()
            name = vf.name
            if not re.search(r"\bview\s*:", content):
                issues.append(f"{name}: missing view block")
            if not re.search(r"\bsql_table_name\s*:", content):
                issues.append(f"{name}: missing sql_table_name")
            if not re.search(r"\bdimension\s*:", content):
                issues.append(f"{name}: no dimensions found")
            if not re.search(r"type\s*:\s*count", content):
                issues.append(f"{name}: missing count measure")
        if issues:
            return "warn", f"{len(issues)} structural issue(s)", "\n".join(f"       {i}" for i in issues)
        return "pass", f"{len(view_files)} view(s) structurally valid (sim — lkml pending approval)", None

    check("LookML views — simulated check", check_views_structure)

    def check_model_structure():
        if not models_dir.exists():
            return "fail", "project/models/ not found", None
        model_files = list(models_dir.glob("*.model.lkml"))
        if not model_files:
            return "fail", "no .model.lkml files found", None
        content = model_files[0].read_text()
        issues = []
        if not re.search(r"\bconnection\s*:", content):
            issues.append("missing connection:")
        explores = re.findall(r"\bexplore\s*:\s*\w+", content)
        if not explores:
            issues.append("no explore blocks found")
        if issues:
            return "warn", "; ".join(issues), None
        return "pass", f"{len(explores)} explore(s) — sim (lkml pending approval)", None

    check("LookML model — simulated check", check_model_structure)

    results.append({
        "name": "lkml syntax check",
        "status": "skip",
        "message": "NOT RUN — pending tooling approval",
        "detail": None,
    })
    results.append({
        "name": "LAMS style check",
        "status": "skip",
        "message": "NOT RUN — pending tooling approval",
        "detail": None,
    })


# ── Git state ────────────────────────────────────────────────────────────────

def check_branch():
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            cwd=REPO_ROOT, text=True
        ).strip()
        if not branch:
            return "warn", "detached HEAD", None
        if branch in ("main", "demo-run", "dev"):
            return "fail", f"on {branch} — commits should go on a feature branch", None
        return "pass", branch, None
    except Exception:
        return "warn", "could not determine branch", None


check("Git branch is a feature branch", check_branch)


# ── Report ───────────────────────────────────────────────────────────────────

passed = sum(1 for r in results if r["status"] == "pass")
warned = sum(1 for r in results if r["status"] == "warn")
failed = sum(1 for r in results if r["status"] == "fail")
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
