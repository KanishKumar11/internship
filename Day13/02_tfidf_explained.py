"""
02_tfidf_explained.py - TF-IDF, done by hand and then by scikit-learn

TEACHES : That TF-IDF is two small ideas multiplied together, and that
          scikit-learn is doing exactly the arithmetic you just did.
          TF  = how OFTEN a word appears in this document
          IDF = how RARE that word is across all documents
          TF-IDF = TF x IDF -> "common here, rare everywhere else"
SLIDE   : Day 13, Slide 6 - TF-IDF Explained Simply (deck page 06/16)
RUN     : python 02_tfidf_explained.py

EXPECTED OUTPUT IN THE TERMINAL
        PART 1 - term frequency, doc 1        python 0.250 ...
        PART 2 - inverse document frequency   python 0.000, sqlite 1.099 ...
        PART 3 - TF x IDF by hand             sqlite 0.275 is the top word
        PART 4 - scikit-learn on the same 3 docs
    Part 4's numbers are NOT identical to Part 3's, and the file explains
    why at the end - that difference is the lesson, not a bug.

REQUIRES
    pip install scikit-learn
"""

import math
import re

from sklearn.feature_extraction.text import TfidfVectorizer

# A tiny corpus. "Corpus" is just the ML word for "the pile of documents
# we are working with". Three is enough to see IDF do its job: "python"
# is in all three, "sqlite" is in only one.
CORPUS: list[str] = [
    "python sqlite sqlite dashboard",
    "python pandas dashboard",
    "python pandas charts",
]


def tokenize(text: str) -> list[str]:
    """Split a document into lowercase words - a list, so repeats survive."""
    # TF is about counting repeats, so unlike file 01 we must NOT use a set.
    return re.findall(r"[a-z0-9]+", text.lower())


def term_frequency(document: str) -> dict[str, float]:
    """TF = how many times a word appears / how many words there are."""
    words = tokenize(document)
    # Dividing by the length is what makes a 20-word document comparable
    # to a 2000-word one. Without it, long documents win every time.
    return {word: words.count(word) / len(words) for word in set(words)}


def inverse_document_frequency(corpus: list[str]) -> dict[str, float]:
    """IDF = log(total documents / documents containing the word)."""
    total_documents = len(corpus)
    document_word_sets = [set(tokenize(document)) for document in corpus]

    scores: dict[str, float] = {}
    for word in sorted(set().union(*document_word_sets)):
        # df = "document frequency" - in how many documents does it appear?
        document_frequency = sum(1 for words in document_word_sets if word in words)
        # log() is what squashes the scale. A word in every document gets
        # log(3/3) = 0.0, so multiplying by it deletes the word entirely.
        # That is IDF automatically ignoring boring words.
        scores[word] = math.log(total_documents / document_frequency)
    return scores


def tf_idf(document: str, idf_scores: dict[str, float]) -> dict[str, float]:
    """TF-IDF = TF x IDF, one number per word in this document."""
    return {word: tf * idf_scores[word] for word, tf in term_frequency(document).items()}


print("The corpus (3 documents):")
for index, document in enumerate(CORPUS, start=1):
    print(f"   doc {index}: {document}")

print("\nPART 1 - TERM FREQUENCY of document 1 (how often, in THIS doc)")
for word, score in sorted(term_frequency(CORPUS[0]).items(), key=lambda pair: -pair[1]):
    print(f"   {word:<10} {score:.3f}")
print("   'sqlite' scores highest - it appears twice out of four words.")
print("   Note TF alone has no opinion about whether that word is interesting.")

print("\nPART 2 - INVERSE DOCUMENT FREQUENCY (how rare, across ALL docs)")
idf_scores = inverse_document_frequency(CORPUS)
for word, score in sorted(idf_scores.items(), key=lambda pair: -pair[1]):
    print(f"   {word:<10} {score:.3f}")
print("   'python' is 0.000 - it is in every document, so it distinguishes nothing.")

print("\nPART 3 - TF x IDF for document 1, computed by hand")
manual_scores = tf_idf(CORPUS[0], idf_scores)
for word, score in sorted(manual_scores.items(), key=lambda pair: -pair[1]):
    print(f"   {word:<10} {score:.3f}")
print("   'sqlite' wins: frequent here AND found nowhere else. That is the whole idea.")

print("\nPART 4 - the same corpus through scikit-learn")
# One object does tokenizing, TF, IDF and the multiplication. Note we pass
# the whole LIST at once - the vectorizer needs every document to work out
# IDF, so feeding it one string at a time would be meaningless.
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(CORPUS)

vocabulary = vectorizer.get_feature_names_out()
document_one_row = tfidf_matrix[0].toarray()[0]
for word, score in sorted(zip(vocabulary, document_one_row), key=lambda pair: -pair[1]):
    print(f"   {word:<10} {score:.3f}")

print("\nSAME ORDER, DIFFERENT DIGITS - sqlite > dashboard > python in both parts.")
print("The digits differ for two reasons, and neither changes the idea:")
print("   1. scikit-learn uses log((1+N)/(1+df)) + 1, a 'smoothed' IDF. The +1 on")
print("      the end means a word in every document keeps a small score instead")
print("      of being multiplied down to exactly zero and disappearing.")
print("   2. It then scales each document's vector to length 1, which is what")
print("      makes the cosine similarity in file 03 work.")
print("\nSo: you now know what TfidfVectorizer does. From here on, we let it do it.")
