"""
03_cosine_similarity_demo.py - The score, from 0 to 1

TEACHES : Cosine similarity. TF-IDF turned each text into a list of
          numbers (a "vector"); cosine similarity measures the ANGLE
          between two of those lists. Same direction = 1.0, nothing in
          common = 0.0. It is the angle and not the distance, which is why
          a short text and a long text can still score 1.0.
SLIDE   : Day 13, Slide 7 - Cosine Similarity (deck page 07/16)
RUN     : python 03_cosine_similarity_demo.py

EXPECTED OUTPUT IN THE TERMINAL
        A vs A   1.00  ██████████  IDENTICAL
        A vs B   0.75  ████████░░  HIGH
        A vs D   0.25  ███░░░░░░░  MEDIUM
        A vs C   0.00  ░░░░░░░░░░  LOW
    The same four texts as file 01, now scored by the real thing.

COMPARE THIS WITH FILE 01
    File 01 gave A vs C = 0.07, because the two sentences share "is".
    Here it is 0.00 - stop_words='english' threw "is" away before scoring.
    That drop from 0.07 to 0.00 is TF-IDF earning its keep.

REQUIRES
    pip install scikit-learn
"""

import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Windows terminals often default to a codepage that cannot print bars. The
# hasattr guard is for 12_run_all.py, which swallows stdout into a buffer
# that has no reconfigure() method.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TEXT_A = "Python is a programming language for data science."
TEXT_B = "Python is a programming language for data science and machine learning."
TEXT_C = "The weather in Amritsar is 28 degrees today."
TEXT_D = "Java is a programming language for web development."


def match_score(text_one: str, text_two: str) -> float:
    """Score two texts from 0.0 to 1.0. This is the 5-line pattern."""
    # stop_words='english' drops "is", "a", "for", "the" and friends. Without
    # it those words are in nearly every sentence and drown out the real
    # signal - every pair would look vaguely similar.
    vectorizer = TfidfVectorizer(stop_words="english")

    # fit_transform takes a LIST of texts, not one string. It learns the
    # vocabulary from both texts and returns one row of numbers per text.
    vectors = vectorizer.fit_transform([text_one, text_two])

    # vectors[0] and vectors[1] are the two rows. cosine_similarity hands
    # back a 2D array (every row against every row), so [0][0] pulls out
    # the single number we actually want.
    return float(cosine_similarity(vectors[0], vectors[1])[0][0])


def bar(score: float, width: int = 10) -> str:
    """Draw the score, because a picture beats a decimal on a projector."""
    filled = round(score * width)
    return "█" * filled + "░" * (width - filled)


def label(score: float) -> str:
    """Name the band. Students should remember the bands, not the digits."""
    if score >= 0.99:
        return "IDENTICAL"
    if score >= 0.50:
        return "HIGH"
    if score >= 0.20:
        return "MEDIUM"
    return "LOW"


def show(name: str, text_one: str, text_two: str) -> None:
    """Print one pair and its score."""
    score = match_score(text_one, text_two)
    print(f"{name}")
    print(f"   1: {text_one}")
    print(f"   2: {text_two}")
    print(f"   {score:.2f}  {bar(score)}  {label(score)}\n")


print("Cosine similarity - the angle between two TF-IDF vectors\n")

# Start with the sanity check. A text against itself MUST be 1.0; if it is
# not, something is wrong with the code, not with the texts.
show("A vs A  (the same text twice)", TEXT_A, TEXT_A)
show("A vs B  (both about Python for data)", TEXT_A, TEXT_B)
show("A vs D  (both programming, different world)", TEXT_A, TEXT_D)
show("A vs C  (nothing whatsoever in common)", TEXT_A, TEXT_C)

print("THE SCALE")
print("   1.00        identical - the same words in the same proportions")
print("   0.50 - 0.99 high      - clearly about the same thing")
print("   0.20 - 0.49 medium    - some shared vocabulary, different topic")
print("   0.00 - 0.19 low       - unrelated")
print("\nA vs D is only 0.25: 'programming language' is shared, but 'Python',")
print("'data science', 'Java' and 'web' are not. The score is doing its job.")
