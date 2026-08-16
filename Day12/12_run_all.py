"""
12_run_all.py - Instructor sanity check for Day 12 (not a demo)

TEACHES : Nothing - run this before class so no live demo dies on a typo,
          a missing library, or a dead internet connection.
RUN     : python 12_run_all.py

WHAT IT DOES
    1. Checks requests, pandas and streamlit are importable.
    2. Checks the internet, by calling Open-Meteo with a 5-second budget.
       This runs FIRST, because if it fails every other check will fail
       too and the checklist should say why.
    3. Executes files 01-05, 07 and 08 with their output suppressed.
       They are plain scripts, so running them is the honest check.
    4. Parse-checks files 06, 09, 10 and 11. They are Streamlit apps, so
       they are compiled and their imports resolved rather than executed.

    Note this makes around 20 real API calls. That is well inside
    Open-Meteo's free allowance, but do not put it in a loop.

EXPECTED OUTPUT IN THE TERMINAL
        Day 12 pre-class check

              ✓ requests installed - OK
              ✓ internet (Open-Meteo reachable) - OK
        ran   ✓ 01_first_api_call.py - OK
        ...
        parse ✓ 11_weather_extended.py - OK

        14/14 checks passed
    Exit code 0 when everything passes, 1 when anything fails.

IF A CHECK FAILS INTERMITTENTLY
    Live APIs blink. A single timeout on one run is usually the network,
    not the code - run it again before going hunting.
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
    "01_first_api_call.py",
    "02_response_object.py",
    "03_query_params.py",
    "04_error_handling.py",
    "05_status_codes_demo.py",
    "07_free_apis_demo.py",
    "08_reading_api_docs.py",
]

# Streamlit apps - parse-check only.
APP_FILES: list[str] = [
    "06_streamlit_caching.py",
    "09_weather_exercise.py",
    "10_weather_solution.py",
    "11_weather_extended.py",
]

REQUIRED_PACKAGES: list[str] = ["requests", "pandas", "streamlit"]


def check_package(name: str) -> str | None:
    """Confirm a package is installed, without importing it."""
    try:
        if importlib.util.find_spec(name) is None:
            return f"not installed - pip install {name}"
    except (ImportError, ValueError):
        return f"not installed - pip install {name}"
    return None


def check_internet() -> str | None:
    """Confirm Open-Meteo is reachable. Every demo depends on this."""
    try:
        import requests
    except ImportError:
        return "requests is not installed, so this cannot be checked"

    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": 31.63, "longitude": 74.87, "current": "temperature_2m"},
            timeout=5,
        )
        response.raise_for_status()
        # A 200 with an empty body is possible (file 05), so confirm the
        # data is really there rather than trusting the status code.
        if "current" not in response.json():
            return "reachable, but the response had no 'current' key"
    except requests.exceptions.Timeout:
        return "timed out after 5s - is the connection slow or blocked?"
    except requests.exceptions.ConnectionError:
        return "could not connect - check the internet or a firewall"
    except Exception as error:
        return f"{type(error).__name__}: {error}"
    return None


def run_script(path: Path) -> str | None:
    """Execute one script with its output swallowed. None means it passed."""
    if not path.exists():
        return "FileNotFoundError: file is missing"

    # spec_from_file_location because "import 01_first_api_call" is a
    # SyntaxError - a module name cannot start with a digit.
    spec = importlib.util.spec_from_file_location(f"day12_check_{path.stem}", path)
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
        # Files 03 and 08 bail out with SystemExit(1) if the API is
        # unreachable. That is a real failure for a pre-class check.
        if exit_error.code:
            return f"SystemExit({exit_error.code}) - the API call failed, see the internet check"
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

    missing = [name for name in sorted(packages_in([tree])) if check_package(name)]
    if missing:
        return f"ImportError: no module named {', '.join(missing)} - is .venv active?"
    return None


def main() -> int:
    """Run every check, print a checklist, return a process exit code."""
    # (prefix, label, problem)
    results: list[tuple[str, str, str | None]] = []

    for name in REQUIRED_PACKAGES:
        results.append(("     ", f"{name} installed", check_package(name)))

    results.append(("     ", "internet (Open-Meteo reachable)", check_internet()))

    for filename in SCRIPT_FILES:
        results.append(("ran  ", filename, run_script(FOLDER / filename)))

    for filename in APP_FILES:
        results.append(("parse", filename, check_app(FOLDER / filename)))

    print("Day 12 pre-class check\n")
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
