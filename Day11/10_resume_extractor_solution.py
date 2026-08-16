"""
10_resume_extractor_solution.py - Day 11 exercise: INSTRUCTOR SOLUTION

TEACHES : The full pipeline end to end - extract (PyPDF2), find (regex),
          store (SQLite). The same three steps Day 13's resume matcher
          runs before it does any AI.
SLIDE   : Day 11, Slide 18 - Exercise, Solution Walkthrough
          (deck page 18/20). Reveal after students have tried file 09.
RUN     : python 10_resume_extractor_solution.py

EXPECTED OUTPUT IN THE TERMINAL
        === EXTRACTED TEXT (first 300 chars) ===
        Aarav Sharma
        Software Engineer
        ...
        Email: aarav.sharma@example.com
        Phone: +91 98765 43210
        Name : Aarav Sharma

        Stored in contacts.db (1 row in contacts)
    Run it twice and the row count goes to 2 - the INSERT has no
    duplicate check, which is a fine thing to point out.

REQUIRES
    sample_resume.pdf - run create_sample_resume.py first.
    Creates contacts.db in this folder.
"""

import re
import sqlite3
from pathlib import Path

try:
    from PyPDF2 import PdfReader
except ImportError:
    from pypdf import PdfReader

PDF_FILE = Path(__file__).with_name("sample_resume.pdf")
DB_FILE = Path(__file__).with_name("contacts.db")

# The two cheatsheet patterns from slide 15, as named constants - so the
# pattern is written once and the code below reads like English.
EMAIL_PATTERN = r"[\w.+-]+@[\w-]+\.[\w.]+"
PHONE_PATTERN = r"\+?\d[\d\s-]{8,}\d"


def extract_pdf_text(path: Path) -> str:
    """Step 1 - read every page of the PDF into one string."""
    reader = PdfReader(str(path))
    full_text = ""
    for page in reader.pages:
        full_text += (page.extract_text() or "") + "\n"
    return full_text


def find_email(text: str) -> str:
    """Step 2 - the first email address, or a message saying there is none."""
    matches = re.findall(EMAIL_PATTERN, text)
    # findall returns [] when nothing matched, so check before indexing -
    # matches[0] on an empty list is an IndexError.
    return matches[0] if matches else "Not found"


def find_phone(text: str) -> str:
    """Step 3 - the first phone number."""
    matches = re.findall(PHONE_PATTERN, text)
    # [0] is deliberate. This pattern also matches the ISO dates further
    # down the resume, but the contact line is at the top of the page, so
    # the first match is the phone number.
    return matches[0] if matches else "Not found"


def find_name(text: str) -> str:
    """Step 4 - the name is the first non-empty line of a resume."""
    # No regex here. A name has no shape a pattern could describe - it is
    # position that identifies it, not format.
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return lines[0] if lines else "Unknown"


def store_contact(name: str, email: str, phone: str) -> int:
    """Step 5 - save the contact to SQLite. Returns the new row count."""
    # Day 10's helper-function pattern: open, work, commit, close.
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            name TEXT,
            email TEXT,
            phone TEXT
        )
        """
    )
    # ? placeholders, exactly as on Day 10 - and it matters more here than
    # it did there, because this data came out of a file somebody else
    # wrote. Never build SQL out of text you did not type yourself.
    conn.execute(
        "INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)",
        (name, email, phone),
    )
    conn.commit()
    row_count = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    conn.close()
    return row_count


if not PDF_FILE.exists():
    print(f"{PDF_FILE.name} is missing. Run: python create_sample_resume.py")
    raise SystemExit(1)

full_text = extract_pdf_text(PDF_FILE)

print("=== EXTRACTED TEXT (first 300 chars) ===")
print(full_text[:300])
print("=" * 40)

email = find_email(full_text)
phone = find_phone(full_text)
name = find_name(full_text)

print(f"Email: {email}")
print(f"Phone: {phone}")
print(f"Name : {name}")

total_rows = store_contact(name, email, phone)
print(f"\nStored in {DB_FILE.name} ({total_rows} row(s) in contacts)")

# THE PIPELINE
#   extract (PyPDF2) -> find (regex) -> store (SQLite).
#   Day 13 adds one step on the end: compare the extracted text to a job
#   description with TF-IDF. Everything before that step is this file.
