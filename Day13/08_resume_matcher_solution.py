"""
08_resume_matcher_solution.py - The resume matcher, finished

TEACHES : The complete exercise. Score two texts, then use the TF-IDF
          weights a second time to work out WHICH words the resume is
          missing - the same trick every applicant-tracking system uses.
SLIDE   : Day 13, Slide 12 - Sample Solution (deck page 12/16)
RUN     : python 08_resume_matcher_solution.py

EXPECTED OUTPUT IN THE TERMINAL
        Match score: 0.41  (41%)

        Missing keywords, most important first:
           learning    0.43
           machine     0.43
           aws         0.21
           deploy      0.21
           ...
        'machine' and 'learning' score double the rest because the job
        description says "machine learning" twice - that is TF doing its job.

REQUIRES
    pip install scikit-learn
"""

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RESUME = (
    "Python developer with two years of experience. I build REST APIs with "
    "Flask, write SQL queries, and analyse data with pandas. BCA graduate."
)

JOB_DESCRIPTION = (
    "Python developer wanted. Build REST APIs with Flask, write SQL queries, "
    "and analyse data with pandas. Train machine learning models with "
    "scikit-learn and deploy the machine learning services to AWS."
)

# Words scoring below this in the job description are not worth telling the
# candidate about. Tune it by eye: too low and you list filler, too high and
# you miss real requirements.
IMPORTANCE_THRESHOLD = 0.1


def match_resume(resume: str, job_description: str) -> tuple[float, list[tuple[str, float]]]:
    """Score a resume against a job, and list the keywords it is missing.

    Returns (match_score, missing_keywords) where missing_keywords is a list
    of (word, weight) pairs sorted with the most important first.
    """
    # One vectorizer, fitted on both texts, so they share a vocabulary and
    # their vectors are directly comparable.
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume, job_description])

    # Row 0 is the resume, row 1 is the job - the order we passed them in.
    match_score = float(cosine_similarity(vectors[0], vectors[1])[0][0])

    vocabulary = vectorizer.get_feature_names_out()

    # The job's row of TF-IDF weights. The matrix is sparse (mostly zeros,
    # stored compactly), so .toarray()[0] flattens it into a plain array we
    # can index alongside the vocabulary.
    job_weights = vectors[1].toarray()[0]

    # Tokenise the resume the same way the vectorizer did - lowercase, word
    # characters only. Using .split() instead would leave "pandas." with its
    # full stop attached, and "pandas" would look missing when it is not.
    resume_words = set(re.findall(r"[a-z0-9]+", resume.lower()))

    missing_keywords = [
        (word, float(weight))
        for word, weight in zip(vocabulary, job_weights)
        # Two conditions: the job leans on this word, AND the resume never
        # says it. A word the job barely mentions is not worth flagging.
        if weight > IMPORTANCE_THRESHOLD and word not in resume_words
    ]

    # Sort by weight descending, so the candidate reads the biggest gap first.
    missing_keywords.sort(key=lambda pair: pair[1], reverse=True)

    return match_score, missing_keywords


score, missing = match_resume(RESUME, JOB_DESCRIPTION)

print(f"Match score: {score:.2f}  ({score:.0%})\n")

print("Missing keywords, most important first:")
for word, weight in missing:
    print(f"   {word:<12} {weight:.2f}")

print(f"\n{len(missing)} keywords from the job description are absent from the resume.")
print("Add the real ones - the skills the candidate genuinely has - and the")
print("score climbs. Add the rest and you have lied to a computer, which is")
print("still lying.")
print("\nWorth noticing: 'wanted' is in that list too. TF-IDF cannot tell a skill")
print("from a job-ad verb, so a human still reads the output. That is the honest")
print("limit of a word-counting model, and it is the point of file 06.")
