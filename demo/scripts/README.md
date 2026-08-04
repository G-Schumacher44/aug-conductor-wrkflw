# Validation Extensions

`scripts/validate.py` is the Conductor governance gate — domain-agnostic, stdlib only,
ships with the scaffold. It checks the spine structure and nothing else.

Domain-specific checks live here as separate scripts. This directory is a reference
implementation. Copy the pattern for your own domain.

---

## The Pattern

Every check is three lines:

**1. Write a check function** — return a `(status, message, detail)` tuple:

```python
def check_my_thing():
    if something_is_wrong:
        return "fail", "what is wrong and how to fix it", None
    return "pass", "", None
```

Status values: `pass`, `warn` (non-blocking), `fail` (blocks exit 0), `skip`.
`detail` is an optional multi-line string printed below the result line.

**2. Register it:**

```python
check("My thing label", check_my_thing)
```

**3. The reporter handles the rest** — consistent output format, exit code, pass/warn/fail/skip counts.

---

## Files

| File | What it checks |
|---|---|
| `validate_lookml.py` | LookML structural checks — manifest, views, model, lkml/LAMS stubs |

---

## Running

```bash
# Conductor governance first, then domain checks
python3 scripts/validate.py && python3 demo/scripts/validate_lookml.py
```

Both must exit 0 before writing a handoff.

---

## Writing Your Own

Copy `validate_lookml.py` as a starting point. Replace the LookML checks with checks
for your domain — config validity, schema structure, API shape, file conventions.
Put your extension script anywhere that makes sense for your project.
The only contract: same `check()` pattern, same `(status, message, detail)` return.
