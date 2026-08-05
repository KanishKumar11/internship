"""Instructor's pre-session sanity check — do all the Day 4 files parse?

Pairs with: nothing on the deck. Run it before the session starts.
Teaches:    (instructor tool, not student material)
Run it:     python 10_run_all.py
Expected:   A green/red checklist, one line per file, and a final count.
            Exit code 0 if everything is fine, 1 if any file failed.

Why this compiles instead of importing: importing a Streamlit app EXECUTES it,
which fires every st.* call outside a Streamlit runtime and floods the terminal
with warnings. We only want to know the files exist and parse, so we read each
one and hand it to compile(). Paths are resolved from this file's own location,
so the check works no matter which folder you run it from.
"""

from __future__ import annotations

import pathlib
import sys

# Make the tick and cross survive a cp1252 Windows console.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

FILENAMES = [
    "01_app_step1_title.py",
    "02_app_step2_text_input.py",
    "03_app_step3_button.py",
    "04_app_step4_balloons.py",
    "05_app_step5_else.py",
    "06_converter_exercise.py",
    "07_converter_solution.py",
    "08_converter_extended.py",
    "09_cheatsheet_demo.py",
]


def check(path: pathlib.Path) -> str | None:
    """Return None if the file parses, or a one-line reason why it doesn't."""
    if not path.exists():
        return "FileNotFoundError: file is missing"
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except SyntaxError as error:
        return f"SyntaxError: line {error.lineno}: {error.msg}"
    except (OSError, UnicodeDecodeError) as error:
        return f"{type(error).__name__}: {error}"
    return None


def main() -> int:
    # Resolve from this file, not the working directory, so `python Day4/10_run_all.py`
    # works from anywhere.
    folder = pathlib.Path(__file__).resolve().parent

    failures = 0
    for filename in FILENAMES:
        problem = check(folder / filename)
        if problem is None:
            print(f"{GREEN}✓{RESET} {filename} - OK")
        else:
            failures += 1
            print(f"{RED}✗{RESET} {filename} - {problem}")

    passed = len(FILENAMES) - failures
    print(f"\n{passed}/{len(FILENAMES)} files OK")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
