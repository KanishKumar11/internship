"""
04_scikit_learn_pattern.py - The five lines you will reuse all day

TEACHES : The canonical scikit-learn pattern for text similarity. Learn
          these five lines and you can compare any two pieces of text -
          resumes, articles, support tickets, exam answers.
SLIDE   : Day 13, Slide 8 - scikit-learn, The 5-Line Pattern (deck page 08/16)
RUN     : python 04_scikit_learn_pattern.py

THE PATTERN, WITH NOTHING AROUND IT
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors    = vectorizer.fit_transform([text_one, text_two])
    score      = cosine_similarity(vectors[0], vectors[1])[0][0]

EXPECTED OUTPUT IN THE TERMINAL
        Match score: 0.65
        Match score as a percentage: 65%
        The vectorizer found 14 words: apis, build, building, data, ...

REQUIRES
    pip install scikit-learn
"""

# scikit-learn is one install, two imports. TfidfVectorizer turns text into
# numbers; cosine_similarity compares two sets of numbers. They live in
# different sub-packages because scikit-learn keeps "prepare the data" and
# "measure the data" apart.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RESUME = (
    "Python developer with 3 years experience building data pipelines "
    "and REST APIs using pandas and SQL."
)
JOB_DESCRIPTION = (
    "Hiring a Python developer to build data pipelines and REST APIs "
    "using pandas and SQL."
)


def compare_texts(text_one: str, text_two: str) -> tuple[float, list[str]]:
    """Return the similarity score and the vocabulary the vectorizer built."""
    # STEP 1 - create the vectorizer.
    #   stop_words='english' is not optional in practice. Leave it out and
    #   "the", "is", "a", "and" carry as much weight as "Python", so every
    #   pair of English sentences looks similar and the score means nothing.
    vectorizer = TfidfVectorizer(stop_words="english")

    # STEP 2 - fit AND transform, in one call, on a LIST of texts.
    #   fit    = look at both texts and build the vocabulary + IDF weights
    #   transform = turn each text into a row of TF-IDF numbers
    #   The brackets matter. Passing a bare string makes scikit-learn treat
    #   each CHARACTER as a document, and you get nonsense instead of an error.
    vectors = vectorizer.fit_transform([text_one, text_two])

    # STEP 3 - measure the angle between the two rows.
    #   vectors[0] is text_one, vectors[1] is text_two. cosine_similarity
    #   compares every row with every row and returns a 2D array, so [0][0]
    #   digs out the one float we care about.
    score = float(cosine_similarity(vectors[0], vectors[1])[0][0])

    # STEP 5 (bonus) - ask the vectorizer what words it decided to keep.
    #   Invaluable when a score surprises you: nine times out of ten the
    #   answer is visible right here in the vocabulary.
    vocabulary = list(vectorizer.get_feature_names_out())

    return score, vocabulary


match_score, words_found = compare_texts(RESUME, JOB_DESCRIPTION)

# STEP 4 - print it. Two decimals; the third one is never meaningful.
print(f"Match score: {match_score:.2f}")
print(f"Match score as a percentage: {match_score:.0%}")

print(f"\nThe vectorizer found {len(words_found)} words:")
print("   " + ", ".join(words_found))
print("\nNotice what is NOT in that list: 'a', 'to', 'and', 'with', 'is'.")
print("stop_words='english' removed them before any maths happened.")
print("\nNotice what IS in it twice: 'build' and 'building'. To TF-IDF those are")
print("two unrelated words. Hold that thought - it is limitation 2 in file 06.")
