"""
06_pdf_extraction.py - Pulling text out of a PDF with PyPDF2

TEACHES : The five-step pipeline - open, count pages, loop and extract,
          concatenate, run regex on the result. This is the exact pipeline
          the exercise uses, and the one Day 13's resume matcher starts
          from.
SLIDE   : Day 11, Slide 13 - Extraction, PDFs with PyPDF2
          (deck page 13/20)
RUN     : python 06_pdf_extraction.py

EXPECTED OUTPUT IN THE TERMINAL
        Pages: 1
        --- first 500 characters ---
        Aarav Sharma
        Software Engineer
        aarav.sharma@example.com | +91 98765 43210
        ...
        --- Page 1 on its own: 17 non-empty lines ---
        Emails found: ['aarav.sharma@example.com']
        Phones found: ['+91 98765 43210', '2024 - 2027', '2026-06-01',
                       '2026-07-31', '2026-08-04']
    Only the first of those "phones" is a phone number - the rest are
    dates that happen to fit the same pattern. That is the point of the
    note the file prints at the end.

REQUIRES
    pip install PyPDF2
    sample_resume.pdf - run create_sample_resume.py first.
"""

import re
from pathlib import Path

# PyPDF2 3.x was renamed to pypdf by the same author. The slides say
# PyPDF2, so that is what we try first; the fallback means this file also
# runs on a machine that only has the newer package. The class and its
# methods are identical either way.
try:
    from PyPDF2 import PdfReader
except ImportError:
    from pypdf import PdfReader

PDF_FILE = Path(__file__).with_name("sample_resume.pdf")

EMAIL_PATTERN = r"[\w.+-]+@[\w-]+\.[\w.]+"
PHONE_PATTERN = r"\+?\d[\d\s-]{8,}\d"


def read_pdf_text(path: Path) -> str:
    """Open a PDF and return every page's text as one string."""
    reader = PdfReader(str(path))
    print(f"Pages: {len(reader.pages)}")

    full_text = ""
    for page in reader.pages:
        # extract_text() returns None - not "" - when a page has no text
        # layer at all, which is what a scanned page looks like. Adding
        # None to a string raises TypeError, so guard it with `or ""`.
        full_text += (page.extract_text() or "") + "\n"
    return full_text


# --- The whole pipeline, wrapped so a missing file is a message ---------
try:
    full_text = read_pdf_text(PDF_FILE)
except FileNotFoundError:
    print(f"{PDF_FILE.name} is missing.")
    print("Run this first:  python create_sample_resume.py")
    raise SystemExit(1)

# --- Step 3: look at what came out --------------------------------------
# ALWAYS print the extracted text before writing regex against it. The
# text in the file is rarely laid out the way the page looks.
print("\n--- first 500 characters ---")
print(full_text[:500])

# --- Step 4: a single page -----------------------------------------------
reader = PdfReader(str(PDF_FILE))
first_page_text = reader.pages[0].extract_text() or ""
line_count = len([line for line in first_page_text.split("\n") if line.strip()])
print(f"--- Page 1 on its own: {line_count} non-empty lines ---")

# --- Step 5: regex on the extracted text --------------------------------
# This is the join between the two halves of today. Once the PDF is a
# string, it is just text - every pattern from files 01-05 applies.
emails = re.findall(EMAIL_PATTERN, full_text)
phones = re.findall(PHONE_PATTERN, full_text)

print(f"\nEmails found: {emails}")
print(f"Phones found: {phones}")
print("\nNote the phone list has more than the phone number in it - the")
print("dates in the Experience section match that pattern too (file 04")
print("explains why). phones[0] is the real one, because the contact line")
print("is at the top of the page.")

# GOTCHAS WORTH SAYING OUT LOUD
#   - A scanned PDF is a picture. extract_text() returns None or "" and no
#     regex will help; that needs OCR, which is well beyond today.
#   - PDFs have no paragraphs or tables in the data sense. You get a flat
#     string and you find the structure yourself - usually with regex.
#   - A two-column layout (academic papers) often extracts in the wrong
#     reading order, interleaving the columns. Print the text and look.
