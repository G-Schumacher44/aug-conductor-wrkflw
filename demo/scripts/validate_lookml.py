#!/usr/bin/env python3
"""
LookML structural validator — domain extension for Conductor.

Demonstrates how to write domain-specific checks that extend the
Conductor governance gate. Run after validate.py passes:

    python3 scripts/validate.py && python3 demo/scripts/validate_lookml.py

See demo/scripts/README.md for the extension pattern.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
PROJECT = REPO_ROOT / "project"

results = []


def check(name, fn):
    try:
        status, message, detail = fn()
        results.append({"name": name, "status": status, "message": message, "detail": detail})
    except Exception as e:
        results.append({"name": name, "status": "fail", "message": str(e), "detail": None})


# ── Manifest ──────────────────────────────────────────────────────────────────

def check_manifest():
    manifest = PROJECT / "manifest.lkml"
    if not manifest.exists():
        return "warn", "manifest.lkml missing — add project_name declaration", None
    if not re.search(r"project_name\s*:", manifest.read_text()):
        return "warn", "present but missing project_name:", None
    return "pass", "", None

check("manifest.lkml", check_manifest)


# ── Views ─────────────────────────────────────────────────────────────────────

def check_views():
    views_dir = PROJECT / "views"
    if not views_dir.exists():
        return "fail", "project/views/ not found", None
    view_files = list(views_dir.glob("*.view.lkml"))
    if not view_files:
        return "fail", "no .view.lkml files — run slice-01 first", None
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
    return "pass", f"{len(view_files)} view(s) structurally valid", None

check("LookML views — structural", check_views)


# ── Model ─────────────────────────────────────────────────────────────────────

def check_model():
    models_dir = PROJECT / "models"
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
    return "pass", f"{len(explores)} explore(s)", None

check("LookML model — structural", check_model)


# ── External tooling stubs ────────────────────────────────────────────────────
# These require pip/npm install. See demo/tools/ for evaluation briefs.

results.append({
    "name": "lkml syntax check",
    "status": "skip",
    "message": "NOT RUN — pip install lkml, then: lkml project/views/*.view.lkml",
    "detail": None,
})
results.append({
    "name": "LAMS style check",
    "status": "skip",
    "message": "NOT RUN — npm i -g @looker/look-at-me-sideways, then: lams --source=project/",
    "detail": None,
})


# ── Report ────────────────────────────────────────────────────────────────────

passed  = sum(1 for r in results if r["status"] == "pass")
warned  = sum(1 for r in results if r["status"] == "warn")
failed  = sum(1 for r in results if r["status"] == "fail")
skipped = sum(1 for r in results if r["status"] == "skip")

icons = {"pass": "✓", "warn": "~", "fail": "✗", "skip": "-"}
hr = "─" * 52

print(f"\nLookML Structural Validation\n{hr}")
for r in results:
    icon = icons.get(r["status"], "?")
    suffix = f"  — {r['message']}" if r["message"] else ""
    print(f"  {icon}  {r['name']}{suffix}")
    if r["detail"]:
        print(r["detail"])
print(hr)
print(f"  {passed} passed  |  {warned} warnings  |  {failed} failed  |  {skipped} skipped\n")

sys.exit(1 if failed > 0 else 0)
