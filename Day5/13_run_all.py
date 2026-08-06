"""
13_run_all.py - Instructor sanity check (not a Streamlit app)

TEACHES : Nothing - this is a pre-class check that every demo file for Day 5
          exists and parses cleanly, so no live demo dies on a typo.
SLIDE   : none (run it before the session starts)
RUN     : python 13_run_all.py

EXPECTED OUTPUT IN THE TERMINAL
    One line per file, e.g.
        [OK]   01_columns_demo.py
        [FAIL] 07_counter_broken.py - SyntaxError: invalid syntax (line 22)
    followed by a "12/12 files OK" summary line. Exit code 0 when all pass,
    1 when any file is missing or broken.

WHY WE COMPILE INSTEAD OF IMPORT
    Importing a Streamlit app actually EXECUTES it - 06_empty_demo.py would
    sleep, and every file would emit bare-mode warnings. We use importlib to
    locate each file, then compile() to check that it parses. Same protection
    against typos, none of the side effects.
"""

import importlib.util
import sys
from pathlib import Path

DEMO_FILES: list[str] = [
    "01_columns_demo.py",
    "02_sidebar_demo.py",
    "03_tabs_demo.py",
    "04_expander_demo.py",
    "05_container_demo.py",
    "06_empty_demo.py",
    "07_counter_broken.py",
    "08_counter_fixed.py",
    "09_form_exercise.py",
    "10_form_solution.py",
    "11_form_extended.py",
    "12_keys_demo.py",
]


def check_file(path: Path) -> str | None:
    """Return None if the file exists and parses, otherwise an error message."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    # importlib gives us a proper module spec for the file, which is also how
    # we would import it if we wanted to run it.
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None:
        return "ImportError: could not build a module spec"

    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError as error:
        return f"SyntaxError: {error.msg} (line {error.lineno})"

    return None


def main() -> int:
    """Check every demo file, print a checklist, return a process exit code."""
    folder = Path(__file__).parent
    passed = 0

    for filename in DEMO_FILES:
        problem = check_file(folder / filename)
        if problem is None:
            passed += 1
            print(f"[OK]   {filename}")
        else:
            print(f"[FAIL] {filename} - {problem}")

    print(f"\n{passed}/{len(DEMO_FILES)} files OK")
    return 0 if passed == len(DEMO_FILES) else 1


if __name__ == "__main__":
    sys.exit(main())
