# pamda — Developer Guide

## Project Purpose

`pamda` is a pure Python functional programming library inspired by [Ramda](https://ramdajs.com/docs/). It provides currying, thunkification, piping, and a rich set of utility functions for nested data structures. It has one runtime dependency: `type_enforced`.

---

## Directory Layout

```
pamda/
  __init__.py        # Package export (pamda) + README as module docstring
  pamda.py           # Core: pamda class with all public functions
  pamda_curry.py     # curry_obj: the currying engine (thunkify, flip, asyncRun, asyncWait, asyncKill, typeEnforce)
  pamda_fast.py      # Internal __dunder__-named fast versions of hot-path functions
  pamda_timer.py     # PamdaTimer / pamda_timer decorator for in-script benchmarking
  pamda_utils.py     # pamda_utils: file I/O (read_csv, write_csv, read_json, write_json) + getMethods, getForceDict
  pamda_wrappers.py  # Class-level decorator wrappers (typed_curry_wrap, staticmethod_wrap, classmethod_wrap)
test/
  curry_tests.py     # curry / thunkify behavior
  function_tests.py  # All core pamda functions
  other_tests.py     # Async (asyncRun, asyncWait, asyncKill) + type enforcement
  time_tests.py      # 1M-scale performance benchmarks (not pass/fail)
  type_check_tests.py # curryTyped and type annotation enforcement
  util_tests.py      # File I/O utilities and pamda_timer
  test_data/         # CSV/JSON fixtures used by util_tests
utils/
  test.sh            # Run all test/*.py files with python
  prettify.sh        # autoflake (unused imports) + black (line-length=80)
  docs.sh            # Generate pdoc HTML docs — do NOT run unless releasing
prettify.sh          # Root-level shortcut: runs utils/prettify.sh directly (no Docker)
run.sh               # Docker wrapper for all dev commands
Dockerfile           # Python 3.13 by default; comment/uncomment to test other versions
pyproject.toml       # black config: line-length=80, target py39; project version
setup.cfg            # Version mirrored here (both must be updated on release)
publish.sh           # PyPI publishing script
```

---

## Development Commands

All commands use Docker via `./run.sh`:

| Command | What it does |
|---|---|
| `./run.sh test` | Run all tests inside Docker |
| `./run.sh prettify` | Format with autoflake + black |
| `./run.sh docs` | Regenerate pdoc documentation |
| `./run.sh` | Drop into a Docker shell |

> **Note:** `./run.sh` requires a TTY. In non-interactive contexts (CI, background tasks) it will fail with "the input device is not a TTY". Ask the user to run it themselves.

**Prettify without Docker:** `./prettify.sh` runs autoflake + black directly in your local environment (requires dev dependencies installed).

**Test runner details** (`utils/test.sh`): Runs every `.py` file in `test/` with `python`. Each file prints failure messages if something goes wrong; silence = pass. Output is also tee'd to `utils/test_output.txt`.

**Docs**: **DO NOT generate docs** unless doing a release. Docs are regenerated and versioned at release time only.

---

## Core Architecture

### Class Hierarchy

```
pamda_utils   ← staticmethod-wrapped, type-enforced file I/O and helpers
    └── pamda ← classmethod-wrapped, typed-curry-wrapped, all public functions
```

**`pamda_utils`** (`pamda_utils.py`):
- Decorated with `@type_enforced.Enforcer` and `@pamda_wrappers.staticmethod_wrap`
- Provides file I/O: `read_csv`, `write_csv`, `read_json`, `write_json`
- Utility helpers: `getMethods`, `getForceDict`

**`pamda`** (`pamda.py`):
- Inherits from `pamda_utils`
- Decorated with `@pamda_wrappers.typed_curry_wrap` and `@pamda_wrappers.classmethod_wrap`
- All methods become class methods, auto-curried with type enforcement
- Usage: `from pamda import pamda` — call methods directly on the class without instantiation
- Subclassing: `class MyClass(pamda): ...` works; inherited methods auto-bind `self`

**`curry_obj`** (`pamda_curry.py`):
- The currying engine. Wraps any function/method; tracks arity; accumulates args until arity reaches 0, then executes.
- Methods: `thunkify()`, `flip()`, `typeEnforce()`, `asyncRun()`, `asyncWait()`, `asyncKill()`
- `asyncRun` / `asyncWait` / `asyncKill` use `threading.Thread` and `ctypes` for thread management

**`pamda_fast.py`**:
- Contains `__dunder__`-named internal versions of hot-path operations: `__getForceDict__`, `__assocPath__`, `__groupByHashable__`, `__mergeDeep__`, `__pathOr__`, `__getKeyValues__`
- These skip validation and curry overhead for performance; used internally by `pamda.py`

**`pamda_timer`** (`pamda_timer.py`):
- `PamdaTimer` class wraps a function and times each call. Supports `get_time_stats(...)` for multi-iteration stats (avg, min, max, std).
- `pamda_timer` is a `Partial`-wrapped factory, usable as `@pamda_timer` or `@pamda_timer(units="us", iterations=100)`

**`pamda_wrappers.py`**:
- `typed_curry_wrap`: recursively wraps all callable class members with `curry_obj(...).typeEnforce()`
- `staticmethod_wrap`: recursively wraps all callable class members as `staticmethod`
- `classmethod_wrap`: recursively wraps all callable class members as `classmethod`

---

## Docstring Convention

All public functions use this structured docstring format:

```python
def my_fn(self, a: int, b: list):
    """
    Function:

    - One-line description of what the function does
    - Additional behavioral notes if needed

    Requires:

    - `a`:
        - Type: int
        - What: Description of the parameter
        - Note: Any special behavior
    - `b`:
        - Type: list
        - What: Description of the parameter

    Optional:

    - `c`:
        - Type: str
        - What: Description of optional parameter
        - Default: "default"

    Example:

    ```
    pamda.my_fn(1, [2, 3]) #=> result
    ```
    """
```

Use `#=>` for return value annotations in examples.

---

## Test Structure

Tests live in `test/`. Each file is standalone: import what's needed, run assertions, print failure messages explicitly. No pass summary is printed — silence means everything passed.

**Test pattern:**
```python
# Passing case
out = pamda.some_fn(valid_input)
if out != expected:
    print("some_fn failed")

# Failure case (should raise)
try:
    pamda.some_fn(invalid_input)
    print("some_fn failed")  # reached means no exception was raised
except:
    pass  # expected exception
```

**Files:**
- `curry_tests.py` — curry wrapper, curry with defaults, thunkify
- `function_tests.py` — one test block per public function in `pamda.py`
- `other_tests.py` — type enforcement, asyncRun/asyncWait/asyncKill timing
- `time_tests.py` — 1M-scale benchmarks via `pamda_timer`; not pass/fail
- `type_check_tests.py` — `curryTyped` with annotated functions
- `util_tests.py` — `read_csv` return types and casting, `pamda_timer` decorator

When adding a new function, add a corresponding test block to `function_tests.py` (or a new file if testing a distinct subsystem). Tests are picked up automatically by `utils/test.sh`.

---

## Coding Conventions

- **Line length**: 80 characters (black config in `pyproject.toml`)
- **Python version**: ≥3.11 — use `str | None` union syntax, not `Optional[str]`
- **Formatting**: always run `./run.sh prettify` (or `./prettify.sh`) before committing
- **Runtime dependencies**: only `type_enforced`. Do not add others.
- **Internal fast functions**: prefix with `__` and suffix with `__` (e.g. `__assocPath__`); import into `pamda.py` from `pamda_fast`
- **No unnecessary abstractions**: don't create shared helpers unless the same logic appears 3+ times
- **DO NOT generate docs**: only regenerate at release time

---

## Release Checklist

1. Bump `version` in `pyproject.toml` and `setup.cfg` (must match)
2. Run `./run.sh prettify`
3. Run `./run.sh test` — all tests must pass
