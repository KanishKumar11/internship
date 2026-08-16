"""
23_run_all_day10.py - Instructor sanity check for Day 10 (not a demo)

TEACHES : Nothing - run this before class so no live demo dies on a typo,
          a missing database, or a package that never got installed.
RUN     : python 23_run_all_day10.py

WHAT IT DOES
    Two different checks, because Day 10 has two kinds of file:

    Files 14-19 are plain scripts, so they are EXECUTED (output
    suppressed). That catches SyntaxError, a missing table, a bad column
    name and a wrong ? count - none of which a parse-only check would see.
    They are run in numeric order because 15 builds the expenses.db that
    16-19 all read.

    Files 20-22 are Streamlit apps, so they are NOT executed - importing
    one outside `streamlit run` has no script context, and calls like
    st.rerun() misbehave or raise. They are parse-checked (compile) and
    their imports are resolved with importlib.util.find_spec instead. A
    tick means "this file will parse and its imports exist", not "this
    page renders". Check the rendering with streamlit run.

    Side effect: this rebuilds expenses.db with the 3 starter rows and
    leaves a scratch playground.db behind.

EXPECTED OUTPUT IN THE TERMINAL
        Day 10 pre-class check

        ran   ✓ 14_alter_drop_demo.py - OK
        ...
        parse ✓ 20_expense_tracker_exercise.py - OK
        ...
        ✓ expenses.db (3 expenses) - OK

        10/10 checks passed
    Exit code 0 when everything passes, 1 when anything fails.
    "ImportError: no module named streamlit" on files 20-22 means the
    virtual environment is not active - activate it and re-run.
"""

import ast
import contextlib
import importlib.util
import io
import sqlite3
import sys
import traceback
from pathlib import Path

# Plain scripts - safe to execute.
SCRIPT_FILES: list[str] = [
    "14_alter_drop_demo.py",
    "15_sqlite_full_pattern.py",
    "16_crud_demo.py",
    "17_with_context_manager.py",
    "18_pandas_sqlite_bridge.py",
    "19_error_demo.py",
]

# Streamlit apps - parse-check only.
APP_FILES: list[str] = [
    "20_expense_tracker_exercise.py",
    "21_expense_tracker_solution.py",
    "22_expense_tracker_extended.py",
]


def run_script(path: Path) -> str | None:
    """Execute one script with its output swallowed. None means it passed."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    # spec_from_file_location because "import 14_alter_drop_demo" is a
    # SyntaxError - a module name cannot start with a digit.
    spec = importlib.util.spec_from_file_location(f"day10_check_{path.stem}", path)
    if spec is None or spec.loader is None:
        return "ImportError: could not build a module spec"

    module = importlib.util.module_from_spec(spec)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(module)
    except SyntaxError as error:
        return f"SyntaxError: {error.msg} (line {error.lineno})"
    except ModuleNotFoundError as error:
        return f"ImportError: no module named {error.name} - is .venv active?"
    except Exception as error:
        last_frame = traceback.extract_tb(error.__traceback__)[-1]
        return f"{type(error).__name__}: {error} (line {last_frame.lineno})"

    return None


def imported_packages(tree: ast.Module) -> set[str]:
    """Collect the top-level package name of every import in a parsed file."""
    packages: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                packages.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            packages.add(node.module.split(".")[0])
    return packages


def check_app(path: Path) -> str | None:
    """Parse-check a Streamlit app and confirm its imports resolve."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as error:
        return f"SyntaxError: {error.msg} (line {error.lineno})"

    missing: list[str] = []
    for package in sorted(imported_packages(tree)):
        try:
            # find_spec locates a package without importing it - no side
            # effects, no Streamlit server started by accident.
            if importlib.util.find_spec(package) is None:
                missing.append(package)
        except (ImportError, ValueError):
            missing.append(package)

    if missing:
        return f"ImportError: no module named {', '.join(missing)} - is .venv active?"

    return None


def check_database(path: Path) -> tuple[str | None, str]:
    """Confirm expenses.db exists and report how many rows it holds."""
    if not path.exists():
        return f"FileNotFoundError: {path.name} was not created", path.name

    conn = sqlite3.connect(path)
    try:
        count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
    except sqlite3.OperationalError as error:
        return f"OperationalError: {error}", path.name
    finally:
        conn.close()

    return None, f"{path.name} ({count} expenses)"


def main() -> int:
    """Run every check, print a checklist, return a process exit code."""
    folder = Path(__file__).parent

    # (prefix, label, problem)
    results: list[tuple[str, str, str | None]] = []

    for filename in SCRIPT_FILES:
        results.append(("ran  ", filename, run_script(folder / filename)))

    for filename in APP_FILES:
        results.append(("parse", filename, check_app(folder / filename)))

    problem, label = check_database(folder / "expenses.db")
    results.append(("     ", label, problem))

    print("Day 10 pre-class check\n")
    for prefix, label, issue in results:
        if issue is None:
            print(f"{prefix} ✓ {label} - OK")
        else:
            print(f"{prefix} ✗ {label} - {issue}")

    passed = sum(1 for _, _, issue in results if issue is None)
    print(f"\n{passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    # Some Windows terminals use a non-UTF-8 codepage; keep the ticks safe.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
