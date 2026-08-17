"""
10_resume_matcher_pdf.py - Day 11 meets Day 13: score a real PDF resume

TEACHES : That the two halves of the internship snap together. Day 11
          pulled text out of a PDF; Day 13 scores text against a job ad.
          Bolt them end to end and you have a working screening tool.
          The pipeline: PDF -> raw text -> regex clean -> TF-IDF -> score.
SLIDE   : Day 13, Slide 13 - Extension 2, PDF Extraction (deck page 13/16)
RUN     : python 10_resume_matcher_pdf.py

EXPECTED OUTPUT IN THE TERMINAL
        Read sample_resume.pdf - 1 page(s)
        367 characters after cleaning
        Match score: 0.36  (36%)
        Missing keywords: build, dashboards, day, hiring, ...
        Without the regex clean the same resume scores 0.27
    The score is lowish on purpose: Aarav's resume is a real one-page CV
    with education and dates in it, not a paragraph written to match a job.

REQUIRES
    pip install scikit-learn PyPDF2
    sample_resume.pdf - already built in Day 11. This file looks for it in
    this folder first, then falls back to ../Day11/. If neither exists, run
    Day11/create_sample_resume.py once.
"""

import re
import sys
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# PyPDF2 3.x was renamed to pypdf by the same author, same API. Day 11 does
# the same dance, so this file runs on whichever one is installed.
try:
    from PyPDF2 import PdfReader
except ImportError:
    from pypdf import PdfReader

# Look here first, then in Day 11 where the file was originally built.
CANDIDATE_PATHS = [
    Path(__file__).with_name("sample_resume.pdf"),
    Path(__file__).parent.parent / "Day11" / "sample_resume.pdf",
]

JOB_DESCRIPTION = (
    "We are hiring a Python intern. You will build Streamlit dashboards "
    "backed by SQLite, write Python scripts to clean CSV data, and use "
    "pandas and Git every day. HTML and CSS knowledge is a plus."
)

IMPORTANCE_THRESHOLD = 0.1


def find_resume_pdf() -> Path | None:
    """Return the first sample_resume.pdf that exists, or None."""
    for path in CANDIDATE_PATHS:
        if path.exists():
            return path
    return None


def read_pdf_text(path: Path) -> str:
    """Extract every page's text as one string. Straight from Day 11."""
    reader = PdfReader(str(path))
    full_text = ""
    for page in reader.pages:
        # extract_text() returns None, not "", on a page with no text layer
        # (a scan, for instance). `or ""` stops that becoming a TypeError.
        full_text += (page.extract_text() or "") + "\n"
    print(f"Read {path.name} - {len(reader.pages)} page(s)")
    return full_text


def clean_text(text: str) -> str:
    """Strip what a job match does not care about. Day 11 regex, file 05."""
    text = re.sub(r"\S+@\S+", " ", text)                 # email addresses
    text = re.sub(r"https?://\S+", " ", text)            # URLs
    text = re.sub(r"\+?\d[\d\s-]{8,}\d", " ", text)      # phone numbers
    text = re.sub(r"[^A-Za-z0-9\s]", " ", text)          # punctuation, pipes, dashes
    return re.sub(r"\s+", " ", text).strip()             # collapse whitespace


def match_resume(resume: str, job_description: str) -> tuple[float, list[tuple[str, float]]]:
    """Score the resume and list the job's keywords it never mentions."""
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume, job_description])

    score = float(cosine_similarity(vectors[0], vectors[1])[0][0])

    vocabulary = vectorizer.get_feature_names_out()
    job_weights = vectors[1].toarray()[0]
    resume_words = set(re.findall(r"[a-z0-9]+", resume.lower()))

    missing = [
        (word, float(weight))
        for word, weight in zip(vocabulary, job_weights)
        if weight > IMPORTANCE_THRESHOLD and word not in resume_words
    ]
    missing.sort(key=lambda pair: pair[1], reverse=True)
    return score, missing


pdf_path = find_resume_pdf()
if pdf_path is None:
    print("Could not find sample_resume.pdf. Looked in:")
    for path in CANDIDATE_PATHS:
        print(f"   {path}")
    print("\nBuild it with:  python ../Day11/create_sample_resume.py")
    sys.exit(1)

raw_text = read_pdf_text(pdf_path)
resume_text = clean_text(raw_text)
print(f"{len(resume_text)} characters after cleaning\n")

print("CLEANED RESUME TEXT:")
print(f"   {resume_text[:200]}...\n")

match_score, missing_keywords = match_resume(resume_text, JOB_DESCRIPTION)

print(f"Match score: {match_score:.2f}  ({match_score:.0%})\n")
print("Missing keywords, most important first:")
for word, weight in missing_keywords:
    print(f"   {word:<12} {weight:.2f}")

# Show the cost of skipping the cleaning step, since the PDF is where the
# junk actually comes from - headers, pipes, phone numbers, dates.
raw_score, _ = match_resume(raw_text, JOB_DESCRIPTION)
print(f"\nWithout the regex clean the same resume scores {raw_score:.2f}")
print(f"instead of {match_score:.2f}. The email address, the phone number and")
print("the punctuation were all padding the vector with words the job never uses.")
