"""
07_run_all.py - Instructor sanity check (not a demo, not a Streamlit app)

TEACHES : Nothing - run this before class so no live demo dies on a typo,
          a missing CSV, or a package that never got installed in .venv.
SLIDE   : none
RUN     : python 07_run_all.py

WHAT IT CHECKS
    1. expenses.csv exists, has the four expected columns, and has rows.
    2. Every amount parses as a number and every date is a real ISO date -
       one stray "Rs 450" in the amount column and every chart in the
       folder breaks.
    3. Every app file 01-06 parses (compile), which catches SyntaxError.
    4. Every package those files import actually resolves on this machine
       (importlib.util.find_spec), which catches the ImportError you would
       otherwise discover in front of the room.

    All six app files are Streamlit apps, so none of them are EXECUTED
    here - importing one would try to start a server and open a browser
    tab. A tick means "this file will parse and its imports exist", not
    "this file renders correctly". Check the rendering with streamlit run.

EXPECTED OUTPUT IN THE TERMINAL
    A checklist, one line per file:
        v expenses.csv (24 rows, 4 columns, total 12,450) - OK
        v 01_expense_tracker_exercise.py - OK
        x 04_layout_tabs.py - SyntaxError: invalid syntax (line 22)
    (real tick and cross characters), then a "7/7 checks passed" summary.
    Exit code 0 when everything passes, 1 when anything fails.

    A row count other than 24 is not a failure - it means someone has been
    demoing. Reset with:  git checkout expenses.csv
"""

import ast
import csv
import datetime
import importlib.util
import sys
from pathlib import Path

APP_FILES: list[str] = [
    "01_expense_tracker_exercise.py",
    "02_expense_tracker_solution.py",
    "03_layout_top_form.py",
    "04_layout_tabs.py",
    "05_layout_two_column.py",
    "06_expense_tracker_extended.py",
]

EXPECTED_COLUMNS: list[str] = ["date", "category", "amount", "note"]


def imported_packages(tree: ast.Module) -> set[str]:
    """Collect the top-level package name of every import in a parsed file."""
    packages: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # "matplotlib.pyplot" -> "matplotlib"
                packages.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            packages.add(node.module.split(".")[0])
    return packages


def missing_packages(packages: set[str]) -> list[str]:
    """Return the packages that are not installed. find_spec does not run them."""
    missing: list[str] = []
    for package in sorted(packages):
        try:
            if importlib.util.find_spec(package) is None:
                missing.append(package)
        except (ImportError, ValueError):
            missing.append(package)
    return missing


def check_csv(path: Path) -> tuple[str | None, str]:
    """Check expenses.csv. Return (problem or None, the label to display)."""
    if not path.exists():
        return "FileNotFoundError: expenses.csv is missing", path.name

    # csv.DictReader, not pandas: a note containing a comma is quoted in
    # the file, and splitting on "," by hand would report a phantom
    # column-count error for a file that is perfectly valid.
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        rows = list(reader)

    if header != EXPECTED_COLUMNS:
        return f"wrong columns: expected {EXPECTED_COLUMNS}, found {header}", path.name
    if not rows:
        return "the file has a header but no expense rows", path.name

    total = 0.0
    for number, row in enumerate(rows, start=2):  # start=2: line 1 is the header
        try:
            total += float(row["amount"])
        except (TypeError, ValueError):
            return f"line {number}: amount {row['amount']!r} is not a number", path.name
        try:
            datetime.date.fromisoformat(row["date"])
        except (TypeError, ValueError):
            return f"line {number}: date {row['date']!r} is not YYYY-MM-DD", path.name

    label = f"{path.name} ({len(rows)} rows, {len(header)} columns, total {total:,.0f})"
    return None, label


def check_app(path: Path) -> str | None:
    """Parse-check one app and confirm its imports resolve. None means OK."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as error:
        return f"SyntaxError: {error.msg} (line {error.lineno})"

    missing = missing_packages(imported_packages(tree))
    if missing:
        return f"ImportError: no module named {', '.join(missing)} - is .venv active?"

    return None


def main() -> int:
    """Run every check, print a checklist, return a process exit code."""
    folder = Path(__file__).parent

    # (label, problem) for every check, in the order we want them printed.
    results: list[tuple[str, str | None]] = []

    csv_problem, csv_label = check_csv(folder / "expenses.csv")
    results.append((csv_label, csv_problem))

    for filename in APP_FILES:
        results.append((filename, check_app(folder / filename)))

    print("Day 8 pre-class check\n")
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
