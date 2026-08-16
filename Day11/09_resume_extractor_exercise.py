"""
09_resume_extractor_exercise.py - Day 11 exercise: STUDENT SCAFFOLD

TEACHES : Everything from today in one script - PyPDF2 pulls the text out,
          regex finds the contact details in it. The first half of Day
          13's resume matcher.
SLIDE   : Day 11, Slide 17 - Exercise Brief (deck page 17/20)
RUN     : python 09_resume_extractor_exercise.py

EXPECTED OUTPUT IN THE TERMINAL
    Right now: the extracted text prints, then three lines saying the
    patterns are not written yet.
    Once you finish the TODOs:
        Email: aarav.sharma@example.com
        Phone: +91 98765 43210
        Name : Aarav Sharma

REQUIRES
    sample_resume.pdf - run create_sample_resume.py first.

--------------------------------------------------------------------------
THE BRIEF
    Read the sample resume PDF, extract its text, and use regex to find
    the email address, the phone number and (bonus) the person's name.

REQUIREMENTS
    [ ] Use PyPDF2 to extract the text from sample_resume.pdf
    [ ] Use re.findall to find the email address
    [ ] Use re.findall to find the phone number
    [ ] Print the results clearly: "Email: ...", "Phone: ..."
    [ ] Bonus: extract the name - it is the first line of the resume

HOW TO WORK
    Uncomment one TODO block at a time, run the file, look at the output.
    The print statements are written for you; you write the patterns.

IF A PATTERN FINDS NOTHING
    Do not guess. The extracted text is printed at the top of the output
    for exactly this reason - read it, find the line you are trying to
    match, and adjust. Regex is iterative; the first attempt rarely wins.
--------------------------------------------------------------------------
"""

import re
from pathlib import Path

try:
    from PyPDF2 import PdfReader
except ImportError:
    # PyPDF2 3.x is also published as pypdf. Identical API.
    from pypdf import PdfReader

PDF_FILE = Path(__file__).with_name("sample_resume.pdf")

# --- 1. Read the PDF - this part is done for you ------------------------
if not PDF_FILE.exists():
    print(f"{PDF_FILE.name} is missing. Run: python create_sample_resume.py")
    raise SystemExit(1)

reader = PdfReader(str(PDF_FILE))
full_text = ""
for page in reader.pages:
    # `or ""` because extract_text() returns None on a page with no text.
    full_text += (page.extract_text() or "") + "\n"

print("=== EXTRACTED TEXT (first 300 chars) ===")
print(full_text[:300])
print("=" * 40)

# --- 2. Find the email --------------------------------------------------
# Hint: the cheatsheet pattern is  [\w.+-]+@[\w-]+\.[\w.]+
#   [\w.+-]+  the username, allowing dots, plus signs and dashes
#   @         a literal @
#   [\w-]+    the domain
#   \.        an escaped dot
#   [\w.]+    the ending - the dot inside the class is what makes .co.in work
# TODO 1: write the pattern and run it.
# email_pattern = r"..."
# emails = re.findall(email_pattern, full_text)
# print(f"Email: {emails[0] if emails else 'Not found'}")
print("Email: (pattern not written yet)")

# --- 3. Find the phone number -------------------------------------------
# Hint: the Indian phone pattern is  \+?\d[\d\s-]{8,}\d
#   \+?          an optional + for +91
#   \d           starts on a digit
#   [\d\s-]{8,}  8 or more digits, spaces or dashes
#   \d           ends on a digit
# Careful: this also matches the dates further down the resume. Taking
# [0] works because the phone is on the contact line at the top.
# TODO 2: write the pattern and run it.
# phone_pattern = r"..."
# phones = re.findall(phone_pattern, full_text)
# print(f"Phone: {phones[0] if phones else 'Not found'}")
print("Phone: (pattern not written yet)")

# --- 4. BONUS: find the name --------------------------------------------
# No regex needed for this one. The name is the first line of a resume -
# so split the text on newlines, drop the blank lines, and take the first
# thing left.
# TODO 3: build the list of non-empty lines and take the first.
# lines = [line.strip() for line in full_text.split("\n") if line.strip()]
# name = lines[0] if lines else "Unknown"
# print(f"Name : {name}")
print("Name : (not written yet)")

# WHEN IT WORKS
#   Email: aarav.sharma@example.com
#   Phone: +91 98765 43210
#   Name : Aarav Sharma
#
# FINISHED EARLY? See file 11 for the three extensions: pull out the
# skills, handle .docx as well as .pdf, and wrap the whole thing in a
# Streamlit upload form.
