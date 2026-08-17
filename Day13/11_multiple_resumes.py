"""
11_multiple_resumes.py - One job, a stack of resumes: the ATS pattern

TEACHES : fit once, transform many. An applicant-tracking system learns the
          vocabulary from the JOB (that is the fixed thing) and then scores
          every resume against it. Because all the resumes are measured
          with the same ruler, their scores can honestly be compared - and
          therefore sorted.
SLIDE   : Day 13, Slide 13 - Extension 3, Multiple Resumes (deck page 13/16)
RUN     : python 11_multiple_resumes.py

EXPECTED OUTPUT IN THE TERMINAL
        1. Priya  (Python + ML)   0.87  █████████░
        2. Rohit  (Python, no ML) 0.57  ██████░░░░
        3. Simran (Java)          0.19  ██░░░░░░░░
    Plus, for each, the job's keywords that resume never mentions.

THE WARNING THAT COMES WITH IT
    This is roughly how the real thing works, and it is why "tailor your
    resume to the job ad" is genuine advice rather than folklore. It is
    also why a good candidate who used different words gets filtered out -
    see file 06.

REQUIRES
    pip install scikit-learn
"""

import re
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Windows terminals often default to a codepage that cannot print bars. The
# hasattr guard is for 12_run_all.py, which swallows stdout into a buffer
# that has no reconfigure() method.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

JOB_DESCRIPTION = (
    "Python developer wanted. Build REST APIs with Flask, write SQL queries, "
    "and analyse data with pandas. Train machine learning models with "
    "scikit-learn and deploy the machine learning services to AWS."
)

# Three candidates, deliberately chosen to land in three different bands.
RESUMES: dict[str, str] = {
    "Priya  (Python + ML)": (
        "Python developer with three years of experience. I train machine "
        "learning models with scikit-learn, build REST APIs, analyse data "
        "with pandas, and deploy services to AWS."
    ),
    "Rohit  (Python, no ML)": (
        "Python developer. I build REST APIs with Flask and write SQL queries. "
        "Comfortable with Git, Linux and writing unit tests."
    ),
    "Simran (Java)": (
        "Java developer with five years of enterprise experience. Built Spring "
        "Boot microservices, wrote Oracle stored procedures, and led a team of "
        "four engineers on a banking platform."
    ),
}


def bar(score: float, width: int = 10) -> str:
    """Draw the score, so the ranking is obvious at a glance."""
    filled = round(score * width)
    return "█" * filled + "░" * (width - filled)


def score_resumes(job_description: str, resumes: dict[str, str]) -> list[tuple[str, float, list[str]]]:
    """Rank resumes against one job. Returns (name, score, missing) best first."""
    vectorizer = TfidfVectorizer(stop_words="english")

    # fit() on the JOB ALONE. This is the whole trick. The vocabulary is now
    # "the words this employer used", frozen, and every resume is scored in
    # that space. Words a candidate uses that the job never mentions are
    # invisible - which is harsh, but it is also what makes the scores
    # comparable with each other.
    vectorizer.fit([job_description])
    job_vocabulary = set(vectorizer.get_feature_names_out())

    # transform(), not fit_transform(). transform reuses the stored
    # vocabulary and IDF weights; fit_transform would throw them away and
    # relearn from this one resume, and the scores would mean nothing.
    job_vector = vectorizer.transform([job_description])

    results: list[tuple[str, float, list[str]]] = []
    for name, resume_text in resumes.items():
        resume_vector = vectorizer.transform([resume_text])
        score = float(cosine_similarity(resume_vector, job_vector)[0][0])

        resume_words = set(re.findall(r"[a-z0-9]+", resume_text.lower()))
        missing = sorted(job_vocabulary - resume_words)

        results.append((name, score, missing))

    # Best match first - the only order a recruiter would ever want.
    results.sort(key=lambda row: row[1], reverse=True)
    return results


print("THE JOB")
print(f"   {JOB_DESCRIPTION}\n")
print(f"Scoring {len(RESUMES)} resumes against it, best first:\n")

for rank, (name, match_score, missing_words) in enumerate(score_resumes(JOB_DESCRIPTION, RESUMES), start=1):
    print(f"{rank}. {name:<24} {match_score:.2f}  {bar(match_score)}")
    print(f"   missing from the job's vocabulary ({len(missing_words)}): "
          f"{', '.join(missing_words)}\n")

print("WHAT THE RANKING IS ACTUALLY MEASURING")
print("   Priya used the employer's own words - 'machine learning',")
print("   'scikit-learn', 'AWS' - so she scores highest.")
print("   Rohit is a real Python developer, but the ML half of the job is")
print("   absent from his resume, so he lands in the middle.")
print("   Simran shares almost no vocabulary with the ad and is filtered out.")
print("\n   None of this measures whether they can do the job. It measures")
print("   word overlap. Keep the difference straight - and remember Simran")
print("   might have been the best hire.")
