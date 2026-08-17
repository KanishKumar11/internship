"""
05_preprocessing_demo.py - What to clean, and what not to bother cleaning

TEACHES : Three things.
          1. TfidfVectorizer already lowercases, strips punctuation and
             (with stop_words='english') drops filler words. Do not waste
             code redoing that.
          2. What it does NOT do is remove emails, phone numbers and other
             junk that is unique to one document. Those are exactly the
             Day 11 regex jobs, and skipping them costs you real score.
          3. fit vs transform - the production pattern. Learn the
             vocabulary once, score many documents against it.
SLIDE   : Day 13, Slide 9 - Text Preprocessing for TF-IDF (deck page 09/16)
RUN     : python 05_preprocessing_demo.py

EXPECTED OUTPUT IN THE TERMINAL
        PART 1 - the vectorizer already did this for you
        PART 2 - the cleaning YOU have to do   (score 0.27 -> 0.37)
        PART 3 - fit once, transform many      (resume 1: 0.74, resume 2: 0.19)

REQUIRES
    pip install scikit-learn
"""

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def score(text_one: str, text_two: str) -> float:
    """The 5-line pattern from file 04, wrapped up so we can reuse it."""
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([text_one, text_two])
    return float(cosine_similarity(vectors[0], vectors[1])[0][0])


# ----------------------------------------------------------------------
# PART 1 - what TfidfVectorizer does for free
# ----------------------------------------------------------------------
print("PART 1 - the vectorizer already did this for you\n")

MESSY = "Python, PYTHON and python!  The data is a big deal."

vectorizer = TfidfVectorizer(stop_words="english")
vectorizer.fit([MESSY])

print(f"   input : {MESSY!r}")
print(f"   vocab : {list(vectorizer.get_feature_names_out())}")
print("   - 'Python', 'PYTHON' and 'python' collapsed into ONE word (lowercase=True)")
print("   - the comma and the exclamation mark are gone (the tokenizer keeps")
print("     only word characters, so 'Python,' becomes 'python')")
print("   - 'the', 'is', 'a' and 'and' are gone (stop_words='english')")
print("   So: do NOT write your own .lower() or punctuation stripper. Done already.\n")


# ----------------------------------------------------------------------
# PART 2 - what YOU have to clean, with Day 11 regex
# ----------------------------------------------------------------------
print("PART 2 - the cleaning YOU have to do (Day 11 regex)\n")

MESSY_RESUME = """
    Kanika Sharma
    kanika.sharma@example.com   |   +91 98765 43210

    Python developer with two years of experience. I build REST APIs with
    Flask, write SQL queries, and analyse data with pandas.   BCA graduate.
"""

JOB_DESCRIPTION = (
    "Python developer wanted. Build REST APIs with Flask, write SQL queries, "
    "and analyse data with pandas. Train machine learning models with "
    "scikit-learn and deploy the machine learning services to AWS."
)


def clean_text(text: str) -> str:
    """Strip the junk that carries no meaning but eats similarity score.

    Every unique word in a document pushes the score DOWN, because cosine
    similarity divides by the length of the vector. An email address and a
    phone number contribute nothing to a job match, but they lengthen the
    vector - so removing them is worth real points.
    """
    # 1. Emails. \S+ is "one or more non-space characters" - crude, but an
    #    email is never split across a space so it is enough here.
    text = re.sub(r"\S+@\S+", " ", text)

    # 2. Phone numbers. An optional +, a digit, then 8+ digits/spaces/dashes,
    #    then a final digit. Same pattern as Day 11's resume extractor.
    text = re.sub(r"\+?\d[\d\s-]{8,}\d", " ", text)

    # 3. Everything that is not a letter, digit or space. This also splits
    #    "scikit-learn" into two words - which is what TfidfVectorizer
    #    would have done anyway, so nothing is lost.
    text = re.sub(r"[^A-Za-z0-9\s]", " ", text)

    # 4. Collapse runs of spaces, tabs and newlines into single spaces, and
    #    trim the ends. Do this LAST, once the earlier steps have left gaps.
    return re.sub(r"\s+", " ", text).strip()


cleaned_resume = clean_text(MESSY_RESUME)

print("   BEFORE:")
print(f"      {MESSY_RESUME.strip()[:90]}...")
print("   AFTER:")
print(f"      {cleaned_resume[:90]}...")

messy_score = score(MESSY_RESUME, JOB_DESCRIPTION)
clean_score = score(cleaned_resume, JOB_DESCRIPTION)

print(f"\n   messy resume   vs job: {messy_score:.2f}")
print(f"   cleaned resume vs job: {clean_score:.2f}")
print(f"   Cleaning bought {clean_score - messy_score:+.2f}. The email and phone number were")
print("   dead weight in the vector, and now they are gone.\n")


# ----------------------------------------------------------------------
# PART 3 - fit vs transform
# ----------------------------------------------------------------------
print("PART 3 - fit once, transform many (the production pattern)\n")

RESUME_ONE = clean_text(
    "Python developer. I train machine learning models with scikit-learn "
    "and deploy services to AWS."
)
RESUME_TWO = clean_text(
    "Java developer. Built Spring Boot microservices and Oracle stored procedures."
)

# fit() = learn the vocabulary and the IDF weights, and keep them.
# Here we fit on the JOB only, so the vocabulary is "the words the employer
# cares about". Anything a candidate writes that the job never mentions is
# simply ignored - which is exactly what a recruiter does too.
job_vectorizer = TfidfVectorizer(stop_words="english")
job_vectorizer.fit([JOB_DESCRIPTION])

# transform() = reuse that stored vocabulary on new text. It does NOT learn
# anything new. That is the whole point: every resume is measured with the
# same ruler, so the scores are comparable with each other.
job_vector = job_vectorizer.transform([JOB_DESCRIPTION])

for name, resume_text in [("resume 1 (Python + ML)", RESUME_ONE),
                          ("resume 2 (Java)", RESUME_TWO)]:
    resume_vector = job_vectorizer.transform([resume_text])
    match = float(cosine_similarity(resume_vector, job_vector)[0][0])
    print(f"   {name:<24} {match:.2f}")

print(f"\n   Vocabulary used for both: {len(job_vectorizer.get_feature_names_out())} words,")
print("   learned from the job description and never changed.")
print("\n   Why this matters: with fit_transform() you would rebuild the vocabulary")
print("   for every resume, and the two scores could not be compared. fit once,")
print("   transform many - that is how a real screening system works, and it is")
print("   what file 11 uses to rank a stack of resumes.")
