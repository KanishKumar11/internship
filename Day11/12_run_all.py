"""
12_run_all.py - Instructor sanity check for Day 11 (not a demo)

TEACHES : Nothing - run this before class so no live demo dies on a typo,
          a missing sample file, or a library that never got installed.
RUN     : python 12_run_all.py

WHAT IT DOES
    1. Checks the two sample files exist, and builds them if they do not -
       every demo from file 06 onwards reads one of them.
    2. Executes files 01-10 with their output suppressed. They are all
       plain scripts, so actually RUNNING them is the honest check: it
       catches a SyntaxError, a missing library, a pattern that crashes
       and a file path that is wrong.
    3. Parse-checks file 11. It is a Streamlit app, so it is compiled and
       its imports resolved rather than executed - a tick means "this will
       parse and its imports exist", not "the page renders".
    4. Re-reads sample_resume.pdf and confirms the three values the
       exercise depends on are actually in it.

EXPECTED OUTPUT IN THE TERMINAL
        Day 11 pre-class check

        ✓ sample_resume.pdf - OK
        ✓ sample_report.docx - OK
        ran   ✓ 01_regex_intro.py - OK
        ...
        parse ✓ 11_resume_extractor_extended.py - OK
        ✓ resume content (name, email, phone) - OK

        14/14 checks passed
    Exit code 0 when everything passes, 1 when anything fails.
"""

import ast
import contextlib
import importlib.util
import io
import subprocess
import sys
import traceback
from pathlib import Path

FOLDER = Path(__file__).parent

# Plain scripts - safe to execute.
SCRIPT_FILES: list[str] = [
    "01_regex_intro.py",
    "02_re_module_basics.py",
    "03_regex_syntax.py",
    "04_regex_examples.py",
    "05_re_sub_demo.py",
    "06_pdf_extraction.py",
    "07_docx_extraction.py",
    "08_regex_cheatsheet.py",
    "09_resume_extractor_exercise.py",
    "10_resume_extractor_solution.py",
]

# Streamlit app - parse-check only.
APP_FILES: list[str] = ["11_resume_extractor_extended.py"]

# (sample file, the script that builds it)
SAMPLE_FILES: list[tuple[str, str]] = [
    ("sample_resume.pdf", "create_sample_resume.py"),
    ("sample_report.docx", "create_sample_docx.py"),
]


def ensure_sample(filename: str, builder: str) -> str | None:
    """Make sure a sample file exists, building it if needed."""
    path = FOLDER / filename
    if path.exists():
        return None

    # Run the builder in a separate process so its own top-level code runs
    # exactly as it would for a student typing the command.
    result = subprocess.run(
        [sys.executable, str(FOLDER / builder)],
        capture_output=True,
        text=True,
        cwd=str(FOLDER),
    )
    if not path.exists():
        first_error_line = (result.stderr or result.stdout).strip().splitlines()
        detail = first_error_line[-1] if first_error_line else "no output"
        return f"missing, and {builder} did not create it - {detail}"
    return None


def run_script(path: Path) -> str | None:
    """Execute one script with its output swallowed. None means it passed."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    # spec_from_file_location because "import 01_regex_intro" is a
    # SyntaxError - a module name cannot start with a digit.
    spec = importlib.util.spec_from_file_location(f"day11_check_{path.stem}", path)
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
        # The demos call raise SystemExit(1) when a sample file is missing.
        # That is a real failure here, not a clean finish.
        if exit_error.code:
            return f"SystemExit({exit_error.code}) - a required file was missing"
    except Exception as error:
        last_frame = traceback.extract_tb(error.__traceback__)[-1]
        return f"{type(error).__name__}: {error} (line {last_frame.lineno})"

    return None


def packages_in(nodes: list[ast.AST]) -> set[str]:
    """Collect the top-level package name of every import under these nodes."""
    packages: set[str] = set()
    for root in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # "matplotlib.pyplot" -> "matplotlib"
                    packages.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                packages.add(node.module.split(".")[0])
    return packages


def optional_packages(tree: ast.Module) -> set[str]:
    """Find imports wrapped in try/except ImportError - they have a fallback."""
    # File 11 imports PyPDF2 with a pypdf fallback, and streamlit with a
    # terminal fallback. Reporting those as missing would be wrong: the
    # file runs perfectly well without either. So an import inside a try
    # that catches ImportError does not count as a hard requirement.
    optional: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Try):
            continue
        for handler in node.handlers:
            names: list[str] = []
            if handler.type is None:
                names = ["ImportError"]  # a bare except catches it too
            elif isinstance(handler.type, ast.Name):
                names = [handler.type.id]
            elif isinstance(handler.type, ast.Tuple):
                names = [e.id for e in handler.type.elts if isinstance(e, ast.Name)]

            if {"ImportError", "ModuleNotFoundError"} & set(names):
                optional |= packages_in(node.body)
    return optional


def check_app(path: Path) -> str | None:
    """Parse-check a Streamlit app and confirm its imports resolve."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as error:
        return f"SyntaxError: {error.msg} (line {error.lineno})"

    # Only the imports with no fallback have to be installed.
    required = packages_in([tree]) - optional_packages(tree)

    missing: list[str] = []
    for package in sorted(required):
        try:
            # find_spec locates a package without importing it - no side
            # effects, and no Streamlit server started by accident.
            if importlib.util.find_spec(package) is None:
                missing.append(package)
        except (ImportError, ValueError):
            missing.append(package)

    if missing:
        return f"ImportError: no module named {', '.join(missing)} - is .venv active?"
    return None


def check_resume_content() -> str | None:
    """Confirm the PDF still contains what the exercise expects to find."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        try:
            from pypdf import PdfReader
        except ImportError:
            return "ImportError: neither PyPDF2 nor pypdf is installed"

    reader = PdfReader(str(FOLDER / "sample_resume.pdf"))
    text = "".join((page.extract_text() or "") for page in reader.pages)
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if not lines or lines[0] != "Aarav Sharma":
        return f"first line is {lines[0] if lines else '(nothing)'!r}, expected 'Aarav Sharma'"
    if "aarav.sharma@example.com" not in text:
        return "the email is not in the extracted text"
    if "+91 98765 43210" not in text:
        return "the phone number is not in the extracted text"
    return None


def main() -> int:
    """Run every check, print a checklist, return a process exit code."""
    # (prefix, label, problem)
    results: list[tuple[str, str, str | None]] = []

    for filename, builder in SAMPLE_FILES:
        results.append(("     ", filename, ensure_sample(filename, builder)))

    for filename in SCRIPT_FILES:
        results.append(("ran  ", filename, run_script(FOLDER / filename)))

    for filename in APP_FILES:
        results.append(("parse", filename, check_app(FOLDER / filename)))

    results.append(("     ", "resume content (name, email, phone)", check_resume_content()))

    print("Day 11 pre-class check\n")
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
