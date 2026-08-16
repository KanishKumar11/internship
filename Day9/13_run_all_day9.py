"""
13_run_all_day9.py - Instructor sanity check for Day 9 (not a demo)

TEACHES : Nothing - run this before class so no live demo dies on a typo,
          a missing database, or a package that never got installed.
SLIDE   : none
RUN     : python 13_run_all_day9.py

WHAT IT DOES
    Executes files 01-12 in order, with their output suppressed, and
    reports whether each one finished without raising. Every Day 9 file is
    a plain script (no Streamlit), so actually RUNNING them is the honest
    check - it catches SyntaxError, a missing table, a bad column name and
    a wrong ? count, none of which a parse-only check would see.

    Order matters and is why the files are numbered: 02 builds students.db
    for 03-05, 06 builds expenses.db for 09-12, and 07 builds app.db for
    08. Running them in numeric order satisfies all three.

    Side effect: this rebuilds students.db and app.db and writes
    config.json. expenses.db is left alone if it already has rows.

EXPECTED OUTPUT IN THE TERMINAL
        Day 9 pre-class check

        ✓ 01_json_demo.py - OK
        ✓ 02_create_students_db.py - OK
        ...
        ✓ students.db (8 students) - OK
        ✓ expenses.db (20 expenses) - OK
        ✓ app.db (4 students, 5 expenses) - OK

        15/15 checks passed
    Exit code 0 when everything passes, 1 when anything fails.
"""

import contextlib
import importlib.util
import io
import sqlite3
import sys
import traceback
from pathlib import Path

SCRIPT_FILES: list[str] = [
    "01_json_demo.py",
    "02_create_students_db.py",
    "03_first_query.py",
    "04_cursor_explained.py",
    "05_where_patterns.py",
    "06_create_table_demo.py",
    "07_foreign_key_demo.py",
    "08_join_demo.py",
    "09_aggregates_demo.py",
    "10_dashboard_patterns.py",
    "11_day9_exercise.py",
    "12_day9_exercise_solution.py",
]


def run_script(path: Path) -> str | None:
    """Execute one script with its output swallowed. None means it passed."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    # spec_from_file_location can load a module whose filename starts with a
    # digit - "import 01_json_demo" would be a SyntaxError, since module
    # names have to be valid Python identifiers.
    spec = importlib.util.spec_from_file_location(f"day9_check_{path.stem}", path)
    if spec is None or spec.loader is None:
        return "ImportError: could not build a module spec"

    module = importlib.util.module_from_spec(spec)
    try:
        # The demos print a lot. Swallow it so the checklist stays readable -
        # we care whether they RAISE, not what they say.
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(module)
    except SyntaxError as error:
        return f"SyntaxError: {error.msg} (line {error.lineno})"
    except ModuleNotFoundError as error:
        return f"ImportError: no module named {error.name} - is .venv active?"
    except Exception as error:
        # Any other failure: the line number is the useful part, so dig the
        # last frame out of the traceback rather than just naming the class.
        last_frame = traceback.extract_tb(error.__traceback__)[-1]
        return f"{type(error).__name__}: {error} (line {last_frame.lineno})"

    return None


def check_database(path: Path, counts: dict[str, str]) -> tuple[str | None, str]:
    """Confirm a .db file exists and report a row count per table."""
    if not path.exists():
        return f"FileNotFoundError: {path.name} was not created", path.name

    conn = sqlite3.connect(path)
    try:
        parts: list[str] = []
        for table, label in counts.items():
            # Table names cannot be passed as ? - a placeholder stands for a
            # VALUE, never an identifier. These names are hard-coded above,
            # not user input, so the f-string here is safe.
            row_count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            parts.append(f"{row_count} {label}")
    except sqlite3.OperationalError as error:
        return f"OperationalError: {error}", path.name
    finally:
        conn.close()

    return None, f"{path.name} ({', '.join(parts)})"


def main() -> int:
    """Run every check, print a checklist, return a process exit code."""
    folder = Path(__file__).parent
    results: list[tuple[str, str | None]] = []

    for filename in SCRIPT_FILES:
        results.append((filename, run_script(folder / filename)))

    # The databases are checked last, because the scripts above are what
    # create them.
    for db_name, counts in [
        ("students.db", {"students": "students"}),
        ("expenses.db", {"expenses": "expenses"}),
        ("app.db", {"students": "students", "expenses": "expenses"}),
    ]:
        problem, label = check_database(folder / db_name, counts)
        results.append((label, problem))

    print("Day 9 pre-class check\n")
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
