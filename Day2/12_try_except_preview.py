"""
12_try_except_preview.py — try/except preview (pairs with Slide 13).

Teaches: a missing file is not a reason for the whole program to die. try/except
lets you handle the predictable failures by name, and `finally` runs either way —
including when the try block has already returned.

Expected output: the failure case, then the success case, with a [finally] line
under both.
"""

import os

SAMPLE_FILE = "exists.txt"


def safe_read(filepath: str) -> str:
    """Read a text file, returning an empty string if it cannot be read.

    Args:
        filepath: Path to the file to read.

    Returns:
        The file's contents, or "" if the file is missing or unreadable.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file_handle:
            return file_handle.read()
    except FileNotFoundError:
        print(f"  [handled] No file named {filepath} -- returning empty text.")
        return ""
    except PermissionError:
        print(f"  [handled] Not allowed to read {filepath} -- returning empty text.")
        return ""
    finally:
        # Runs on success, on error, and even after the `return` above.
        print(f"  [finally] Finished trying to read {filepath}.")


print("--- Case 1: the file does not exist ---")
missing_content = safe_read("missing.txt")
print(f"  Got {len(missing_content)} characters back. Program still running.\n")

with open(SAMPLE_FILE, "w", encoding="utf-8") as sample_file:
    sample_file.write("Day 2 -- Python, Properly\nThis file exists.\n")

print("--- Case 2: the file exists ---")
found_content = safe_read(SAMPLE_FILE)
print(f"  Got {len(found_content)} characters back:")
print(f"  {found_content.strip()!r}")

os.remove(SAMPLE_FILE)
print(f"\nDeleted {SAMPLE_FILE}")
