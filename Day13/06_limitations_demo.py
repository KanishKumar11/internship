"""
06_limitations_demo.py - Four things TF-IDF simply cannot do

TEACHES : That TF-IDF counts words and nothing more. It has no idea that
          "ML" and "machine learning" are the same thing, that "developer"
          and "development" share a root, that "bank" has two meanings, or
          that word order changes who bit whom. Knowing where a tool breaks
          is the difference between using it and trusting it.
SLIDE   : Day 13, Slide 10 - TF-IDF Limitations (deck page 10/16)
RUN     : python 06_limitations_demo.py

EXPECTED OUTPUT IN THE TERMINAL
        1. SYNONYMS            0.18  should be high, is low
        2. WORD RELATIONSHIPS  0.12  should be high, is low
        3. CONTEXT             0.34  should be low,  is medium
        4. WORD ORDER          1.00  should be low,  is a perfect match
    Every one of those four numbers is WRONG in a way a human never would be.

REQUIRES
    pip install scikit-learn
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def score(text_one: str, text_two: str) -> float:
    """The 5-line pattern from file 04."""
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([text_one, text_two])
    return float(cosine_similarity(vectors[0], vectors[1])[0][0])


def demonstrate(number: int, title: str, text_one: str, text_two: str,
                expected: str, why: str) -> None:
    """Print one failure: the texts, the score, what it should be, and why."""
    print(f"{number}. {title}  ->  {score(text_one, text_two):.2f}")
    print(f"   1: {text_one}")
    print(f"   2: {text_two}")
    print(f"   a human would say: {expected}")
    print(f"   why TF-IDF fails : {why}\n")


print("TF-IDF counts words. It does not read them. Here is the bill:\n")

demonstrate(
    1, "SYNONYMS",
    "3 years of ML experience building predictive models.",
    "Machine learning engineer wanted to build predictive models.",
    "a strong match - these describe the same person",
    "'ml' is one token; 'machine' and 'learning' are two others. To the "
    "vectorizer\n                      they are three unrelated words that "
    "happen to sit in the same sentence.",
)

demonstrate(
    2, "WORD RELATIONSHIPS",
    "Senior Python developer, 3 years.",
    "Software development role, 3 years, Java team.",
    "related - both are about developing software",
    "'developer' and 'development' share a root, but string equality does "
    "not care.\n                      They differ by three characters, so "
    "they contribute nothing to the overlap.",
)

demonstrate(
    3, "CONTEXT",
    "I sat by the river bank today.",
    "I deposited money in the bank today.",
    "unrelated - one is a riverside, the other is a financial institution",
    "'bank' matched, so the score went UP. TF-IDF has exactly one entry "
    "for 'bank'\n                      and no way to ask which meaning was "
    "intended.",
)

demonstrate(
    4, "WORD ORDER",
    "The dog bites the man.",
    "The man bites the dog.",
    "opposite - these describe two very different afternoons",
    "the two sentences contain the identical bag of words. Order is thrown "
    "away the\n                      moment the text is tokenised, so the "
    "vectors are literally the same vector.",
)

print("WHY THIS MATTERS")
print("   These four gaps are why the field kept going:")
print("      TF-IDF   (1972)  counts words")
print("      Word2Vec (2013)  learns that 'king' and 'queen' live near each other")
print("      BERT     (2018)  reads the whole sentence, so 'bank' has two meanings")
print("      GPT      (2018-) generates language, not just measures it")
print("\n   These limitations are why Word2Vec, BERT, and GPT were invented -")
print("   they understand meaning, not just word counts.")
print("\n   TF-IDF is still everywhere though: it is fast, it needs no training,")
print("   it runs on a laptop with no GPU, and you can explain every number it")
print("   produces. For search filters and resume screening that is often enough.")
