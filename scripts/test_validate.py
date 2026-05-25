#!/usr/bin/env python3
"""
Tests for scripts/validate.py — runs the validator as a subprocess against
fixture directories so the tests don't depend on the repo's own project/ state.

Usage:
  python3 scripts/test_validate.py
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent / "validate.py"
PASS = 0
FAIL_COUNT = [0]


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(project_root: Path, extra_env: dict | None = None) -> tuple[int, str]:
    env = {**os.environ, "CONDUCTOR_PROJECT_ROOT": str(project_root), "CI": "1"}
    if extra_env:
        env.update(extra_env)
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, env=env
    )
    return result.returncode, result.stdout + result.stderr


def ok(name: str, condition: bool, output: str = "") -> None:
    if condition:
        print(f"  ✓  {name}")
    else:
        print(f"  ✗  {name}")
        if output:
            for line in output.strip().splitlines():
                print(f"       {line}")
        FAIL_COUNT[0] += 1


def make_good_project(tmp: Path) -> Path:
    p = tmp / "project"
    (p / "conductor").mkdir(parents=True)
    (p / ".github" / "workflows").mkdir(parents=True)

    (p / "AGENTS.md").write_text("# Agents\n")
    (p / "intent.md").write_text("# Intent\nWhat we are building.\n")
    (p / "conductor" / "index.md").write_text(
        "# Index\nActive slice: conductor/slice-01.md\n"
    )
    (p / "conductor" / "slice-01.md").write_text(
        "# Slice 01\n## Acceptance Criteria\n- [x] Thing done\n"
    )
    (p / "conductor" / "handoff-log.md").write_text(
        "# Handoff\nCommit: abc1234\nExact Next Steps: do the next thing\n"
    )
    (p / ".github" / "workflows" / "ci.yml").write_text(
        "name: CI\non: push\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps: []\n"
    )
    return p


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_good_project():
    with tempfile.TemporaryDirectory() as tmp:
        p = make_good_project(Path(tmp))
        rc, out = run(p)
        ok("good project exits 0", rc == 0, out)
        ok("good project shows passed", "passed" in out, out)
        ok("no failures on good project", "0 failed" in out, out)


def test_missing_project_dir():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "nonexistent"
        rc, out = run(p)
        ok("missing project/ exits 0 (warn not fail)", rc == 0, out)
        ok("reports warn for missing project/", "not found" in out, out)


def test_missing_required_file():
    with tempfile.TemporaryDirectory() as tmp:
        p = make_good_project(Path(tmp))
        (p / "intent.md").unlink()
        rc, out = run(p)
        ok("missing intent.md exits 1", rc == 1, out)
        ok("reports fail for missing intent.md", "project/intent.md" in out and "✗" in out, out)


def test_empty_handoff():
    with tempfile.TemporaryDirectory() as tmp:
        p = make_good_project(Path(tmp))
        (p / "conductor" / "handoff-log.md").write_text("<!-- placeholder -->")
        rc, out = run(p)
        ok("empty handoff exits 0 (warn only)", rc == 0, out)
        ok("warns about empty handoff", "empty" in out, out)


def test_handoff_missing_fields():
    with tempfile.TemporaryDirectory() as tmp:
        p = make_good_project(Path(tmp))
        (p / "conductor" / "handoff-log.md").write_text(
            "Worked on the thing and it was great. Spent time on all the work. "
            "Made many changes to many files.\n"
        )
        rc, out = run(p)
        ok("handoff missing required fields exits 0 (warn)", rc == 0, out)
        ok("warns about missing Commit: field", "Commit:" in out, out)


def test_active_slice_missing():
    with tempfile.TemporaryDirectory() as tmp:
        p = make_good_project(Path(tmp))
        (p / "conductor" / "slice-01.md").unlink()
        rc, out = run(p)
        ok("missing active slice file exits 1", rc == 1, out)
        ok("reports fail for missing slice file", "not found" in out, out)


def test_acceptance_criteria_partial():
    with tempfile.TemporaryDirectory() as tmp:
        p = make_good_project(Path(tmp))
        (p / "conductor" / "slice-01.md").write_text(
            "# Slice 01\n## Acceptance Criteria\n- [x] Done\n- [ ] Not done yet\n"
        )
        rc, out = run(p)
        ok("partial criteria exits 0 (warn)", rc == 0, out)
        ok("reports 1/2 criteria checked", "1/2" in out, out)


def test_acceptance_criteria_all_checked():
    with tempfile.TemporaryDirectory() as tmp:
        p = make_good_project(Path(tmp))
        (p / "conductor" / "slice-01.md").write_text(
            "# Slice 01\n## Acceptance Criteria\n- [x] Done\n- [x] Also done\n"
        )
        rc, out = run(p)
        ok("all criteria checked exits 0", rc == 0, out)
        ok("reports 2/2 checked", "2/2" in out, out)


def test_active_slice_none():
    with tempfile.TemporaryDirectory() as tmp:
        p = make_good_project(Path(tmp))
        (p / "conductor" / "index.md").write_text(
            "# Index\nActive slice: none — queue exhausted\n"
        )
        rc, out = run(p)
        ok("active slice 'none' exits 0", rc == 0, out)


def test_no_ci_stub():
    with tempfile.TemporaryDirectory() as tmp:
        p = make_good_project(Path(tmp))
        import shutil
        shutil.rmtree(p / ".github")
        rc, out = run(p)
        ok("missing CI stub exits 0 (warn)", rc == 0, out)
        ok("warns about missing CI stub", "stub recommended" in out, out)


# ── Runner ────────────────────────────────────────────────────────────────────

tests = [
    test_good_project,
    test_missing_project_dir,
    test_missing_required_file,
    test_empty_handoff,
    test_handoff_missing_fields,
    test_active_slice_missing,
    test_acceptance_criteria_partial,
    test_acceptance_criteria_all_checked,
    test_active_slice_none,
    test_no_ci_stub,
]

hr = "─" * 52
print(f"\nvalidate.py test suite\n{hr}")
for t in tests:
    print(f"\n{t.__name__}")
    t()

print(f"\n{hr}")
total = sum(1 for t in tests for _ in [None])  # count tests run
if FAIL_COUNT[0]:
    print(f"  {FAIL_COUNT[0]} assertion(s) failed\n")
    sys.exit(1)
else:
    print(f"  all assertions passed\n")
