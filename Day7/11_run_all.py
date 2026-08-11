"""
11_run_all.py - Instructor sanity check (not a demo, not a Streamlit app)

TEACHES : Nothing - run this before class so no live demo dies on a typo,
          a missing CSV, or a package that never got installed in .venv.
SLIDE   : none
RUN     : python 11_run_all.py

WHAT IT CHECKS
    1. students.csv exists, has the five expected columns, and has rows.
    2. Every app file 01-10 parses (compile), which catches SyntaxError.
    3. Every package those files import actually resolves on this machine
       (importlib.util.find_spec), which catches the ImportError you would
       otherwise discover in front of the room.

    All ten files are Streamlit apps, so none of them are EXECUTED here -
    importing one would try to start a server and open a browser tab. A
    tick means "this file will parse and its imports exist", not "this
    file renders correctly". Check the rendering with streamlit run.

EXPECTED OUTPUT IN THE TERMINAL
    A checklist, one line per file:
        v students.csv (28 rows, 5 columns) - OK
        v 01_line_chart_demo.py - OK
        x 04_matplotlib_demo.py - SyntaxError: invalid syntax (line 22)
    (real tick and cross characters), then an "11/11 checks passed"
    summary. Exit code 0 when everything passes, 1 when anything fails.
"""

import ast
import importlib.util
import sys
from pathlib import Path

APP_FILES: list[str] = [
    "01_line_chart_demo.py",
    "02_bar_chart_demo.py",
    "03_area_chart_demo.py",
    "04_matplotlib_demo.py",
    "05_data_display_demo.py",
    "06_styled_chart_demo.py",
    "07_cheatsheet_demo.py",
    "08_full_dashboard_exercise.py",
    "09_full_dashboard_solution.py",
    "10_full_dashboard_extended.py",
]

EXPECTED_COLUMNS: list[str] = ["name", "age", "city", "branch", "marks"]


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
    """Check students.csv. Return (problem or None, the label to display)."""
    if not path.exists():
        return "FileNotFoundError: students.csv is missing", path.name

    lines = path.read_text(encoding="utf-8").strip().splitlines()
    header = lines[0].split(",")
    if header != EXPECTED_COLUMNS:
        return f"wrong columns: expected {EXPECTED_COLUMNS}, found {header}", path.name
    if len(lines) < 2:
        return "the file has a header but no student rows", path.name

    return None, f"{path.name} ({len(lines) - 1} rows, {len(header)} columns)"


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

    csv_problem, csv_label = check_csv(folder / "students.csv")
    results.append((csv_label, csv_problem))

    for filename in APP_FILES:
        results.append((filename, check_app(folder / filename)))

    print("Day 7 pre-class check\n")
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
