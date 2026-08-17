"""
12_run_all.py - Instructor sanity check for Day 13 (not a demo)

TEACHES : Nothing - run this before class so no live demo dies on a typo,
          a missing library, or a PDF that was never built.
RUN     : python 12_run_all.py

WHAT IT DOES
    1. Checks scikit-learn and its dependency numpy are installed, plus
       streamlit (file 09) and PyPDF2/pypdf (file 10). This runs FIRST,
       because if sklearn is missing every other check fails for the same
       one reason and the checklist should say so plainly.
    2. Checks sample_resume.pdf exists, here or in Day11. File 10 needs it.
    3. Executes files 01-06, 08, 10 and 11 with their output suppressed.
       They are plain scripts, so running them is the honest check.
    4. Parse-checks files 07 and 09. File 07 is the exercise scaffold - it
       is deliberately incomplete, so it is compiled rather than run.
       File 09 is a Streamlit app, which needs `streamlit run`.

    Everything here is local computation. No internet, no API keys, no
    rate limits - unlike Day 12, you can run this as often as you like.

EXPECTED OUTPUT IN THE TERMINAL
              ✓ scikit-learn installed - OK
              ✓ numpy installed - OK
              ...
        ran   ✓ 01_similarity_intuition.py - OK
        ...
        parse ✓ 09_resume_matcher_streamlit.py - OK

        16/16 checks passed
    Exit code 0 when everything passes, 1 when anything fails.
"""

import ast
import contextlib
import importlib.util
import io
import sys
import traceback
from pathlib import Path

FOLDER = Path(__file__).parent

# Plain scripts - safe to execute.
SCRIPT_FILES: list[str] = [
    "01_similarity_intuition.py",
    "02_tfidf_explained.py",
    "03_cosine_similarity_demo.py",
    "04_scikit_learn_pattern.py",
    "05_preprocessing_demo.py",
    "06_limitations_demo.py",
    "08_resume_matcher_solution.py",
    "10_resume_matcher_pdf.py",
    "11_multiple_resumes.py",
]

# 07 is the exercise scaffold (deliberately incomplete), 09 is a Streamlit
# app. Neither is meant to be executed by `python`, so parse-check them.
PARSE_ONLY_FILES: list[str] = [
    "07_resume_matcher_exercise.py",
    "09_resume_matcher_streamlit.py",
]

# The import name, not the pip name, where they differ.
REQUIRED_PACKAGES: list[tuple[str, str]] = [
    ("sklearn", "scikit-learn"),
    ("numpy", "numpy"),
    ("streamlit", "streamlit"),
]


def check_package(import_name: str, pip_name: str) -> str | None:
    """Confirm a package is installed, without importing it."""
    try:
        if importlib.util.find_spec(import_name) is None:
            return f"not installed - pip install {pip_name}"
    except (ImportError, ValueError):
        return f"not installed - pip install {pip_name}"
    return None


def check_pdf_library() -> str | None:
    """File 10 accepts either PyPDF2 or its newer name, pypdf."""
    if check_package("PyPDF2", "PyPDF2") and check_package("pypdf", "pypdf"):
        return "neither PyPDF2 nor pypdf is installed - pip install PyPDF2"
    return None


def check_sample_pdf() -> str | None:
    """File 10 reads sample_resume.pdf, built back in Day 11."""
    here = FOLDER / "sample_resume.pdf"
    day_eleven = FOLDER.parent / "Day11" / "sample_resume.pdf"
    if here.exists() or day_eleven.exists():
        return None
    return "missing - run python ../Day11/create_sample_resume.py"


def run_script(path: Path) -> str | None:
    """Execute one script with its output swallowed. None means it passed."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    # spec_from_file_location because "import 01_similarity_intuition" is a
    # SyntaxError - a module name cannot start with a digit.
    spec = importlib.util.spec_from_file_location(f"day13_check_{path.stem}", path)
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
    except SystemExit as exit_error:
        # File 10 exits with 1 when sample_resume.pdf cannot be found.
        if exit_error.code:
            return f"SystemExit({exit_error.code}) - see the sample_resume.pdf check"
    except Exception as error:
        last_frame = traceback.extract_tb(error.__traceback__)[-1]
        return f"{type(error).__name__}: {error} (line {last_frame.lineno})"

    return None


def packages_in(tree: ast.AST) -> set[str]:
    """Collect the top-level package name of every import in this file."""
    packages: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                packages.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            packages.add(node.module.split(".")[0])
    return packages


def check_parse_only(path: Path) -> str | None:
    """Compile a file and confirm its imports resolve, without running it."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as error:
        return f"SyntaxError: {error.msg} (line {error.lineno})"

    missing = [name for name in sorted(packages_in(tree)) if check_package(name, name)]
    if missing:
        return f"ImportError: no module named {', '.join(missing)} - is .venv active?"
    return None


def main() -> int:
    """Run every check, print a checklist, return a process exit code."""
    # (prefix, label, problem)
    results: list[tuple[str, str, str | None]] = []

    for import_name, pip_name in REQUIRED_PACKAGES:
        results.append(("     ", f"{pip_name} installed", check_package(import_name, pip_name)))

    results.append(("     ", "PyPDF2 (or pypdf) installed", check_pdf_library()))
    results.append(("     ", "sample_resume.pdf available", check_sample_pdf()))

    for filename in SCRIPT_FILES:
        results.append(("ran  ", filename, run_script(FOLDER / filename)))

    for filename in PARSE_ONLY_FILES:
        results.append(("parse", filename, check_parse_only(FOLDER / filename)))

    print("Day 13 pre-class check\n")
    for prefix, label, problem in results:
        if problem is None:
            print(f"{prefix} ✓ {label} - OK")
        else:
            print(f"{prefix} ✗ {label} - {problem}")

    passed = sum(1 for _, _, problem in results if problem is None)
    print(f"\n{passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    # Some Windows terminals use a non-UTF-8 codepage; keep the ticks safe.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
