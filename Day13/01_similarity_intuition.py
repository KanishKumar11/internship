"""
01_similarity_intuition.py - What does "similar" even mean?

TEACHES : The intuition BEFORE the library. Two pieces of text are similar
          when they share words. Count the shared words, divide by the
          total, and you have a similarity score - no maths degree and no
          scikit-learn required.
SLIDE   : Day 13, Slide 5 - Text Similarity Intuition (deck page 05/16)
RUN     : python 01_similarity_intuition.py

THE 3-STEP PROCESS FROM THE SLIDE
    1. text    -> split into words
    2. numbers -> count what overlaps
    3. compare -> turn the overlap into one score between 0 and 1
    Today's whole session is that loop. This file does it by hand so the
    library in file 03 has nothing left to hide.

EXPECTED OUTPUT IN THE TERMINAL
        A vs B   0.73  ███████░░░  HIGH
        A vs C   0.07  ░░░░░░░░░░  LOW
        A vs D   0.45  ████░░░░░░  MEDIUM
    plus the shared words behind each score.

REQUIRES
    Nothing. Standard library only - not even scikit-learn.
"""

import re
import sys

# Windows terminals often default to a codepage that cannot print the bar
# characters below. Two lines up front, and the demo never dies mid-slide.
# The hasattr guard is for 12_run_all.py, which swallows stdout into a
# buffer that has no reconfigure() method.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# The four texts from slide 5. A is our reference; B, C and D are the
# things we compare it against.
TEXT_A = "Python is a programming language for data science."
TEXT_B = "Python is a programming language for data science and machine learning."
TEXT_C = "The weather in Amritsar is 28 degrees today."
TEXT_D = "Java is a programming language for web development."


def to_word_set(text: str) -> set[str]:
    """Turn a sentence into a set of lowercase words.

    A set, not a list, because we care about WHICH words appear - not how
    many times. Lowercase so "Python" and "python" count as one word, and
    findall instead of split() so the full stop in "science." does not get
    glued onto the word.
    """
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def similarity(text_one: str, text_two: str) -> float:
    """Score two texts from 0.0 (nothing in common) to 1.0 (same words).

    shared / total is the honest version of "how much overlap is there?".
    Dividing by the TOTAL unique words matters: without it, a huge text
    would score highly against everything just by having lots of words.
    """
    words_one = to_word_set(text_one)
    words_two = to_word_set(text_two)

    shared_words = words_one & words_two   # in both texts
    all_words = words_one | words_two      # in either text

    return len(shared_words) / len(all_words)


def bar(score: float, width: int = 10) -> str:
    """Draw the score as a bar, because 0.73 means more when you see it."""
    filled = round(score * width)
    return "█" * filled + "░" * (width - filled)


def label(score: float) -> str:
    """Put a word to the number, so students learn the bands not the digits."""
    if score >= 0.50:
        return "HIGH"
    if score >= 0.20:
        return "MEDIUM"
    return "LOW"


def compare(name: str, text_one: str, text_two: str) -> None:
    """Print one comparison: the two texts, the shared words, the score."""
    score = similarity(text_one, text_two)
    shared = sorted(to_word_set(text_one) & to_word_set(text_two))

    print(f"{name}")
    print(f"   1: {text_one}")
    print(f"   2: {text_two}")
    print(f"   shared words ({len(shared)}): {', '.join(shared)}")
    print(f"   score {score:.2f}  {bar(score)}  {label(score)}\n")


print("Step 1: text -> Step 2: numbers -> Step 3: compare\n")

compare("A vs B  (both about Python for data)", TEXT_A, TEXT_B)
compare("A vs C  (completely unrelated)", TEXT_A, TEXT_C)
compare("A vs D  (both about programming languages)", TEXT_A, TEXT_D)

# The catch, and the reason the next files exist. This score treats every
# word as equally important - "is" counts exactly as much as "Python".
# That is why A vs C is not 0.00: the two sentences share the word "is",
# which tells us nothing at all. TF-IDF (file 02) fixes precisely this.
print("Notice: A vs C is not 0.00 - the two share the word 'is'.")
print("Counting 'is' as heavily as 'Python' is the flaw TF-IDF fixes next.")
