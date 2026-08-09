"""
12_run_all.py - Instructor sanity check (not a demo, not a Streamlit app)

TEACHES : Nothing - run this before class so no live demo dies on a typo or a
          missing CSV.
SLIDE   : none
RUN     : python 12_run_all.py

WHAT IT CHECKS
    students.csv exists and has the five expected columns, then imports each
    of the eight plain scripts (01-07 and 11) with importlib. Importing a
    module EXECUTES it, so a tick here means the file really ran end to end,
    not just that it parsed. Their print output is swallowed so the checklist
    stays readable.

    The Streamlit apps (08, 09, 10) are only parse-checked - importing them
    would try to start a server and open browser tabs.

EXPECTED OUTPUT IN THE TERMINAL
    A checklist, one line per file:
        v students.csv (28 rows, 5 columns) - OK
        v 01_loading_demo.py - OK
        x 03_filtering_basic.py - SyntaxError: invalid syntax (line 22)
    (real tick and cross characters), then a "12/12 checks passed" summary.
    Exit code 0 when everything passes, 1 when anything fails.
"""

import contextlib
import importlib.util
import io
import os
import sys
from pathlib import Path

SCRIPT_FILES: list[str] = [
    "01_loading_demo.py",
    "02_inspecting_demo.py",
    "03_filtering_basic.py",
    "04_filtering_advanced.py",
    "05_sorting_demo.py",
    "06_loc_iloc_demo.py",
    "07_columns_demo.py",
    "11_cheatsheet_demo.py",
]

# Importing these would start a Streamlit server, so we only parse-check them.
STREAMLIT_FILES: list[str] = [
    "08_dashboard_exercise.py",
    "09_dashboard_solution.py",
    "10_dashboard_extended.py",
]

EXPECTED_COLUMNS: list[str] = ["name", "age", "city", "branch", "marks"]


def check_csv(path: Path) -> tuple[str | None, str]:
    """Check students.csv. Return (problem or None, the label to display)."""
    if not path.exists():
        return "FileNotFoundError: students.csv is missing", path.name

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    header = lines[0].split(",")
    if header != EXPECTED_COLUMNS:
        return f"wrong columns: expected {EXPECTED_COLUMNS}, found {header}", path.name

    return None, f"{path.name} ({len(lines) - 1} rows, {len(header)} columns)"


def check_script(path: Path) -> str | None:
    """Import (and therefore run) a script. Return None when it succeeds."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        return "ImportError: could not build a module spec"

    module = importlib.util.module_from_spec(spec)
    try:
        # The demos print a lot; capture it so only the checklist shows.
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(module)
    except SyntaxError as error:
        return f"SyntaxError: {error.msg} (line {error.lineno})"
    except ImportError as error:
        return f"ImportError: {error}"
    except Exception as error:  # a demo that runs but crashes is just as broken
        return f"{type(error).__name__}: {error}"

    return None


def check_parses(path: Path) -> str | None:
    """Parse-check a Streamlit app without executing it."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError as error:
        return f"SyntaxError: {error.msg} (line {error.lineno})"

    return None


def main() -> int:
    """Run every check, print a checklist, return a process exit code."""
    folder = Path(__file__).parent
    # The demos load "students.csv" by relative path, so run from their folder.
    os.chdir(folder)

    # (label, problem) for every check, in the order we want them printed.
    results: list[tuple[str, str | None]] = []

    csv_problem, csv_label = check_csv(folder / "students.csv")
    results.append((csv_label, csv_problem))

    for filename in SCRIPT_FILES:
        results.append((filename, check_script(folder / filename)))

    for filename in STREAMLIT_FILES:
        results.append((filename, check_parses(folder / filename)))

    print("Day 6 pre-class check\n")
    for label, problem in results:
        if problem is None:
            print(f"✓ {label} - OK")
        else:
            print(f"✗ {label} - {problem}")

    passed = sum(1 for _, problem in results if problem is None)
    print(f"\n{passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    # Some Windows terminals use a non-UTF-8 codepage; keep the ticks safe.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
