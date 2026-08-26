"""
smart_notes_app.py - Smart Notes Summarizer

READ THIS BEFORE YOU READ THE CODE.

This file is deliberately written back-to-front: the plan first, the code
second. That is the order we build in, and it is the order this file is
meant to be taught in. The full plan is in smart_notes_plan.md; what
follows is the short version, so the file can be read on its own.


STEP 1 - THE ONE SENTENCE
    Paste long lecture notes, get back the 5 most important sentences,
    the key terms, and how long the notes take to read.

    If you cannot write this sentence, you are not ready to open the
    editor. Everything below is an argument about how to make this one
    sentence true.


STEP 2 - THE CONTRACT (in, out)
    IN    one blob of text - pasted, or read from a .txt file
          one number - how many sentences the summary should be

    OUT   a summary  - N sentences, in the order they were written
          key terms  - the 10 words the notes lean on hardest
          stats      - word count, reading time, sentence count
          a chart    - those 10 words, drawn by weight

    Fixing the contract first is what lets us build the middle in any
    order we like, and what makes it obvious when a section is finished.


STEP 3 - THE PIPELINE (and the shape of the data at every arrow)
    text (str)
        -> split_into_sentences()   -> list[str]        Day 11, regex
        -> score_sentences()        -> array of floats  Day 13, TF-IDF
        -> pick_summary()           -> list[str]        Day 2, sort + slice
        -> extract_key_terms()      -> DataFrame        Day 13 + Day 6
        -> compute_stats()          -> three ints       Day 2
        -> Streamlit renders it     -> pixels           Days 4-5, Day 7

    Five arrows, five functions, one per arrow. That is not a
    coincidence - the pipeline was drawn first and the functions were
    named after the arrows.


STEP 4 - THE DECISIONS WE ARGUED ABOUT (and lost time to, so you do not)
    Score = SUM of a sentence's word weights, not the average.
        Sum rewards long sentences. Average rewards short ones. Sum reads
        better on lecture notes, where the loaded sentences genuinely are
        the longer ones. One line to change if you disagree - see
        score_sentences().

    The summary keeps ORIGINAL order, not ranked order.
        Ranked order reads like five unrelated facts. Original order still
        reads like an argument, because the author put them in that order
        for a reason.

    No "Summarize" button, even though the mockup on slide 3 has one.
        The whole computation is milliseconds. A button would only add a
        click and a session_state variable to keep the results alive
        across reruns. Decide this at plan time - reversing it later means
        touching every section.

    No caching (Day 12), on purpose.
        st.cache_data earns its place when the slow thing is a network
        call or a big file. TF-IDF over 20 sentences is not slow. Adding
        cache decorators here would be cargo cult.


STEP 5 - WHAT WILL GO WRONG (written before it went wrong, not after)
    Empty input                 -> st.info, and compute nothing
    One sentence pasted         -> nothing to summarise, say so
    "the and a is of"           -> TF-IDF raises "empty vocabulary", catch it
    Notes about Dr. Ambedkar    -> naive regex splits on "Dr." - see
                                   split_into_sentences(), which is
                                   longer than slide 5 for exactly this
                                   reason
    A .txt file saved on Windows-> not UTF-8, decode would crash


STEP 6 - THE BUILD ORDER
    Section 1  text in, sentences out          runs on its own
    Section 2  sentences in, summary out       runs on its own
    Section 3  key terms, stats, chart         runs on its own
    Section 4  polish - sidebar, empty state, footer

    Each section runs before the next one is written. If you cannot run
    it, it is too big - cut it in half.


STEP 7 - WHAT WE ARE NOT BUILDING TODAY
    PDF upload (Day 11 can do it - it is just not today's point).
    Sentences rewritten in the model's own words. TF-IDF selects
    sentences; it cannot write one. That is a different kind of model.
    Saving summaries to a database (Day 10 can do it - out of scope).

    A plan that does not say what is out of scope is a wish, not a plan.


WHICH DAYS THIS COMBINES
    Day 2      loops, conditionals, sorting
    Days 4-5   Streamlit widgets, layout, sidebar
    Day 6      pandas DataFrames
    Day 7      charts (st.bar_chart)
    Day 11     regex sentence splitting
    Day 13     TF-IDF vectorization with scikit-learn

    Nothing here is new. Today is about wiring it together.


HOW TO RUN IT
    pip install streamlit scikit-learn pandas
    streamlit run smart_notes_app.py

    Then open http://localhost:8501. Streamlit usually opens it for you.


HOW THIS FILE IS ORGANISED
    IMPORTS
    CONFIGURATION      every number you might want to tune, in one place
    HELPER FUNCTIONS   one per arrow in the pipeline above
    SECTION 1          title, sidebar, text input
    SECTION 2          sentence splitting
    SECTION 3          TF-IDF scoring and the summary
    SECTION 4          key terms, stats, chart
    SECTION 5          footer

    The helper functions come BEFORE the UI, because Streamlit runs this
    file top to bottom on every keystroke, and a function has to exist
    before the line that calls it.
"""

# === IMPORTS ===

import re  # Day 11: regex, for finding sentence boundaries

import numpy as np  # Day 13: the TF-IDF matrix comes back as numpy arrays
import pandas as pd  # Day 6: DataFrames, for the key terms table and the chart
import streamlit as st  # Days 4-5: the whole user interface

# Day 13: the one scikit-learn piece we need. TfidfVectorizer turns text
# into numbers that say how important each word is. There is no
# cosine_similarity import today - we are not comparing two documents,
# we are ranking the sentences inside one.
from sklearn.feature_extraction.text import TfidfVectorizer


# === CONFIGURATION ===
# Step 4 of the plan produced these numbers. They live up here, named,
# instead of buried in the code, so Phase 3 ("customise it") is a matter
# of editing one line and pressing save.

# The slider's range and starting point. Below 3 a summary is not a
# summary; above 10 it is just the notes again with gaps in them.
MIN_SUMMARY_SENTENCES = 3
MAX_SUMMARY_SENTENCES = 10
DEFAULT_SUMMARY_SENTENCES = 5

# How many key terms to show, and how many columns to lay them out in.
# 10 and 5 give two tidy rows of five metric cards.
TOP_KEY_TERMS = 10
KEY_TERM_COLUMNS = 5

# Average adult reading speed for study material. 200 is the number
# every "5 min read" badge on the internet uses.
WORDS_PER_MINUTE = 200

# A "sentence" shorter than this is a heading, a page number, a stray
# bullet, or the "3." left behind by a numbered list. Ten characters is
# short enough to keep "It rained." and long enough to drop "Unit 2."
MIN_SENTENCE_LENGTH = 10

# Abbreviations that end in a full stop WITHOUT ending a sentence. This
# list is the whole reason split_into_sentences() is more than one line.
# Add to it when your own notes break - that is a two-second fix, and a
# good exercise.
ABBREVIATIONS = (
    "Mr", "Mrs", "Ms", "Dr", "Prof", "Sr", "Jr", "St",
    "vs", "etc", "e.g", "i.e", "approx", "Fig", "Eq", "No", "al",
)

# The stand-in we put where a protected full stop used to be. It has to
# be something a human could not possibly type into a browser text box,
# because anything they CAN type, they eventually will. "\x00" is the NUL
# character: no keyboard produces it and no paste survives with it.
DOT_PLACEHOLDER = "\x00"

# Built once, at import time, instead of on every keystroke. \b is a word
# boundary, so "St." matches but the "st." at the end of "artist." does
# not. The group captures the abbreviation so the substitution can put it
# back untouched.
ABBREVIATION_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(word) for word in ABBREVIATIONS) + r")\."
)


# === HELPER FUNCTIONS ===
# One function per arrow in the pipeline. Each takes plain data and
# returns plain data - no Streamlit inside, so you can test them in a
# normal Python file, and so the UI sections below read as four lines
# instead of forty.


def read_uploaded_text(uploaded_file) -> str:
    """
    Read an uploaded .txt file into a string.

    PLAN NOTE - this is failure mode 5 from step 5 of the plan. A .txt
    file written by Notepad on a Windows laptop is usually cp1252, not
    UTF-8, and .decode("utf-8") raises on the first curly quote. We try
    UTF-8 first because it is right almost always, and fall back to
    latin-1, which is the one encoding that physically cannot fail: every
    byte from 0 to 255 maps to some character. The odd character may come
    out wrong; the app does not crash in front of the class.

    Args:
        uploaded_file: The object returned by st.file_uploader.

    Returns:
        The file's contents as a string.
    """
    raw_bytes = uploaded_file.getvalue()

    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return raw_bytes.decode("latin-1")


def split_into_sentences(text: str) -> list:
    """
    Split a blob of text into a list of sentences.
    Day 11 skill: re.split with a lookbehind, and re.sub for protection.

    PLAN NOTE - slide 5 gives this as one line:

        re.split(r'(?<=[.!?])\\s+', text)

    and the checkpoint on the same slide asks you to confirm it does NOT
    split on "Mr." or "Dr.". It does. Both cannot be true, and the
    checkpoint is the one worth keeping, so the function grew.

    The trick is protect, split, restore:
      1. Hide the full stops that do not end sentences.
      2. Split on the ones that are left - now they are all real.
      3. Put the hidden ones back.

    Args:
        text: The raw text the user pasted or uploaded.

    Returns:
        A list of sentences, whitespace trimmed, with anything shorter
        than MIN_SENTENCE_LENGTH dropped.
    """
    # STEP 1 - protect abbreviations. "Dr. Ambedkar" becomes
    # "Dr<NUL> Ambedkar", which has no full stop for step 2 to split on.
    #
    # THE LAMBDA - a function written inline, with no def and no name.
    # These two are the same function:
    #
    #     def protect(match):
    #         return match.group(1) + DOT_PLACEHOLDER
    #
    #     lambda match: match.group(1) + DOT_PLACEHOLDER
    #
    # Left of the colon is the parameter list; right of the colon is one
    # expression, and that expression's value is what comes back. There
    # is no "return" keyword and no room for a second line. That limit
    # is the point, not a wart: a lambda is for the throwaway one-liner
    # that is not worth naming, and anything needing two lines has
    # earned a def. It is called like any other function - the name is
    # the only thing it is missing.
    #
    # Why one is wanted here: .sub() accepts either a replacement STRING
    # or a replacement FUNCTION. Handed a function, it calls it once per
    # match and passes in the match object, so `match` is one hit of the
    # pattern and match.group(1) is what the parentheses in
    # ABBREVIATION_PATTERN captured - "Dr", without its full stop. We
    # return "Dr" + NUL, and the real full stop is gone. Naming that
    # two-token function would put its definition six lines away from
    # its only use, which is exactly the trade the lambda avoids.
    #
    # The same shape turns up all over Python wherever a function is an
    # argument: sorted(rows, key=lambda row: row[1]) to sort on the
    # second column, df.apply(lambda value: value * 2), and so on.
    protected = ABBREVIATION_PATTERN.sub(
        lambda match: match.group(1) + DOT_PLACEHOLDER, text
    )

    # STEP 1b - protect decimal numbers the same way. "Accuracy rose to
    # 98.6 percent" must not become two sentences. The pattern is
    # digit-dot-digit, and the two capture groups put the digits back
    # around the placeholder.
    #
    # Note this one takes the OTHER option and passes a replacement
    # string: \1 and \2 are regex shorthand for the same groups
    # match.group(1) and match.group(2) would hand you in a lambda. Both
    # forms are here on purpose. The string is shorter when the
    # replacement only shuffles captured text around; the lambda is the
    # one you need the moment building the replacement takes real Python
    # - a dict lookup, an if, a .upper(), anything at all.
    protected = re.sub(r"(\d)\.(\d)", r"\1" + DOT_PLACEHOLDER + r"\2", protected)

    # STEP 2 - the split from slide 5, now that every remaining full stop
    # really does end a sentence. (?<=[.!?]) is a lookbehind: "there must
    # be a . or ! or ? just before this point". \s+ is the whitespace we
    # actually cut at. The lookbehind is what keeps the punctuation
    # attached to the sentence instead of being eaten by the split.
    raw_sentences = re.split(r"(?<=[.!?])\s+", protected.strip())

    # STEP 3 - restore, trim, and drop the fragments.
    sentences = []
    for raw_sentence in raw_sentences:
        sentence = raw_sentence.replace(DOT_PLACEHOLDER, ".").strip()

        # Day 2: a plain guard. Headings, page numbers and list markers
        # all survive step 2 and all pollute the TF-IDF vocabulary.
        if len(sentence) >= MIN_SENTENCE_LENGTH:
            sentences.append(sentence)

    return sentences


def score_sentences(sentences: list) -> tuple:
    """
    Score every sentence by how much important vocabulary it carries.
    Day 13 skill: TfidfVectorizer + fit_transform.

    This is the same five-line pattern from Day 13. The only difference
    is what a "document" means: on Day 13 each document was a whole
    resume, and today each document is one sentence.

    Args:
        sentences: The list from split_into_sentences.

    Returns:
        A tuple of (scores, vectorizer, matrix):
        - scores: one float per sentence, same order as the input
        - vectorizer: the fitted TfidfVectorizer, for the key terms
        - matrix: the TF-IDF matrix, also for the key terms

    Raises:
        ValueError: if nothing survives stop-word removal. The caller
            handles it - see Section 3.

    The vectorizer and matrix come back too so Section 4 can reuse them.
    Refitting there would repeat the work and, worse, could produce a key
    terms list that disagreed with the summary above it.
    """
    # stop_words="english" removes "the", "is", "a" and about 300 others.
    # This is not optional. Leave it out and the highest-scoring sentence
    # is simply the one with the most "the" in it.
    vectorizer = TfidfVectorizer(stop_words="english")

    # fit_transform takes a LIST of strings - which is exactly what we
    # have. Row i of the matrix is sentence i; each column is a word in
    # the vocabulary; each cell is how important that word is here.
    matrix = vectorizer.fit_transform(sentences)

    # A sentence's score is the sum of its word weights: axis=1 means
    # "add up each row". The result is a numpy matrix of shape (n, 1), so
    # .flatten() turns it into a plain list of n numbers we can sort.
    #
    # PLAN NOTE - sum, not mean, and this is the decision from step 4.
    # Summing rewards sentences that carry more loaded words, which on
    # lecture notes tends to be the longer ones. To try the other way,
    # change .sum(axis=1) to .mean(axis=1) and reload - the summary will
    # fill up with short definition sentences. Neither is wrong; pick the
    # one that reads better on YOUR notes.
    scores = np.asarray(matrix.sum(axis=1)).flatten()

    return scores, vectorizer, matrix


def pick_summary(sentences: list, scores, count: int) -> list:
    """
    Pick the highest scoring sentences, then put them back in order.
    Day 2 skill: sorting, slicing, and a loop.

    PLAN NOTE - the two-sort dance is the decision from step 4 and it is
    the whole idea of the app, so it gets three lines and a comment each.

    Args:
        sentences: The list of sentences.
        scores: One score per sentence, from score_sentences.
        count: How many sentences the user asked for (the slider).

    Returns:
        The chosen sentences, in the order the author wrote them.
    """
    # np.argsort returns the INDEXES that would sort the array, smallest
    # first. [::-1] reverses it, so ranked_indexes[0] is now the index of
    # the best sentence.
    ranked_indexes = np.argsort(scores)[::-1]

    # Take the best `count` of them. Slicing past the end is not an error
    # in Python, so asking for 10 sentences from a 4-sentence note gives
    # 4 - no guard needed.
    best_indexes = ranked_indexes[:count]

    # Then sort those indexes back into ascending order. This is the line
    # that turns "five facts in a random order" into something that still
    # reads like an argument.
    best_indexes = sorted(best_indexes)

    return [sentences[index] for index in best_indexes]


def extract_key_terms(vectorizer, matrix, count: int) -> pd.DataFrame:
    """
    Find the words the whole document leans on hardest.
    Day 13 skill: get_feature_names_out. Day 6 skill: DataFrame.

    Sentence scores added up each ROW. Key terms add up each COLUMN: how
    much does this one word matter across every sentence at once. Same
    matrix, turned ninety degrees.

    Args:
        vectorizer: The fitted TfidfVectorizer.
        matrix: The TF-IDF matrix from fit_transform.
        count: How many terms to return.

    Returns:
        A DataFrame with columns "term" and "weight", heaviest first.
    """
    # The vocabulary: every word the vectorizer kept, alphabetically. The
    # matrix columns line up with this list position by position, which
    # is the only reason indexes work as a lookup below.
    terms = vectorizer.get_feature_names_out()

    # axis=0 is "add up each column" - the one character that separates
    # this function from score_sentences.
    weights = np.asarray(matrix.sum(axis=0)).flatten()

    ranked_indexes = np.argsort(weights)[::-1]

    # Day 2: walk the ranking and take the first `count` terms that are
    # actually words.
    #
    # PLAN NOTE - this loop is here because of something the plan did not
    # predict and the first test run did. TF-IDF's tokenizer splits "98.6"
    # into "98", so a page of notes with any numbers in it puts "98" and
    # "2024" on the key term cards, above real words. Stop words were
    # planned for; digits were not. Add it to step 5 of your own plan next
    # time - "the vocabulary contains things that are not words".
    chosen_indexes = []
    for index in ranked_indexes:
        term = terms[index]

        # any() with a generator: True if at least one character is a
        # letter. Keeps "gpt4" and "covid19", drops "98" and "2024".
        if not any(character.isalpha() for character in term):
            continue

        chosen_indexes.append(index)

        if len(chosen_indexes) == count:
            break

    # Day 6: build the DataFrame from two aligned lists. float() on the
    # way in, because numpy's float32 renders as "0.8200000524521" in a
    # Streamlit metric and nobody wants to explain why.
    return pd.DataFrame(
        {
            "term": [terms[index] for index in chosen_indexes],
            "weight": [float(weights[index]) for index in chosen_indexes],
        }
    )


def compute_stats(text: str, sentences: list) -> tuple:
    """
    Word count, reading time, sentence count.
    Day 2 skill: len, split, arithmetic.

    Args:
        text: The original text, not the cleaned version - the user asked
            how long THEIR notes are, not how long the leftovers are.
        sentences: The split sentences, for the count.

    Returns:
        A tuple of (word_count, reading_minutes, sentence_count).
    """
    # .split() with no argument splits on any run of whitespace and drops
    # the empties, so double spaces and newlines do not inflate the count.
    word_count = len(text.split())

    # max(1, ...) because round(80 / 200) is 0, and "0 min read" looks
    # like a bug even though the arithmetic is right.
    reading_minutes = max(1, round(word_count / WORDS_PER_MINUTE))

    return word_count, reading_minutes, len(sentences)


# === SECTION 1: TITLE, SIDEBAR, TEXT INPUT ===
# Days 4-5: set_page_config, title, sidebar, text_area, file_uploader, slider
#
# CHECKPOINT - after this section runs:
#   [ ] the text area appears
#   [ ] the slider appears, 3 to 10
#   [ ] pasting text shows "Found N sentences"
#   [ ] it does NOT split on "Dr." or "Mr."

# set_page_config must be the FIRST Streamlit call in the file. Any other
# st.* line above it and Streamlit raises an error.
st.set_page_config(page_title="Smart Notes Summarizer", page_icon="📝", layout="wide")

st.title("Smart Notes Summarizer")
st.write("Paste your lecture notes. Get the most important sentences instantly.")

# POLISH (build step 4, item 1) - the sidebar. Instructions belong here
# rather than in the main column, where they would push the actual app
# below the fold.
with st.sidebar:
    st.header("How it works")
    st.write(
        """
        1. Paste your notes, or upload a `.txt` file.
        2. Choose how long the summary should be.
        3. Read the summary, the key terms and the chart.
        """
    )

    st.header("Skills used")
    st.write(
        """
        - **Day 11** - regex sentence splitting
        - **Day 13** - TF-IDF scoring
        - **Days 4-5** - Streamlit widgets and layout
        - **Day 6** - pandas DataFrames
        - **Day 7** - bar charts
        """
    )

    st.caption(
        "This picks sentences the author already wrote. It does not write "
        "new ones - TF-IDF counts words, it does not understand them."
    )

st.subheader("1. Your notes")

pasted_text = st.text_area(
    "Paste your notes here",
    height=200,
    key="notes_input",
    placeholder="Paste lecture notes, an article, or any long text...",
)

uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"], key="notes_upload")

# PLAN NOTE - a file wins over the text box, and we do NOT try to push the
# file's contents into the text area. Once a widget has a key, Streamlit
# remembers what the user put there and ignores a changed `value=`
# argument on later reruns, so that trick fails in a way that looks like
# the upload did nothing. Choosing between the two sources here, in plain
# Python, always works.
if uploaded_file is not None:
    text = read_uploaded_text(uploaded_file)
    st.caption("Reading the uploaded file. Remove it with the × to use the pasted text.")
else:
    text = pasted_text

# The slider lives outside every `if` below, so it is on screen before
# there is any text to summarise. A control that appears and disappears
# is a control people never find.
num_sentences = st.slider(
    "Summary length (sentences)",
    MIN_SUMMARY_SENTENCES,
    MAX_SUMMARY_SENTENCES,
    DEFAULT_SUMMARY_SENTENCES,
    key="length_slider",
)


# === SECTION 2: SENTENCE SPLITTING ===
# Day 11: the helper above, called for real

# Splitting is cheap, so it happens on every rerun. `if text.strip()`
# guards against splitting an empty string, which would return [] anyway
# but reads as an accident rather than a decision.
sentences = split_into_sentences(text) if text.strip() else []

if not text.strip():
    # POLISH (build step 4, item 2) - the empty state. This is failure
    # mode 1 from the plan, and it is the FIRST thing every user sees, so
    # it is worth more than a blank page.
    st.info("Paste your notes above, or upload a `.txt` file, to begin.")

elif len(sentences) < 2:
    # Failure mode 2. One sentence has nothing to be more important than.
    # Note this is a warning, not an error - the user did nothing wrong,
    # there is just no work to do.
    st.warning(
        "That is only one sentence. Paste a few paragraphs so there is "
        "something to summarise."
    )

else:
    st.caption(f"Found {len(sentences)} sentences.")

    # === SECTION 3: TF-IDF SCORING + THE SUMMARY ===
    # Day 13: score_sentences and pick_summary, called for real
    #
    # CHECKPOINT - after this section runs:
    #   [ ] a summary appears
    #   [ ] it has as many sentences as the slider says
    #   [ ] they are in ORIGINAL order, not ranked order
    #   [ ] moving the slider changes the length
    #   [ ] "the", "is" and "a" never show up as key terms

    scores = None

    try:
        scores, vectorizer, tfidf_matrix = score_sentences(sentences)
    except ValueError as error:
        # Failure mode 3: after stop-word removal there was no vocabulary
        # left. Someone pasted "the and a is of", or a wall of numbers.
        # scikit-learn calls this "empty vocabulary", which means nothing
        # to a first-year student, so we say it in English and keep the
        # original message for the ones who want to look it up.
        st.error(
            f"Nothing left to score after removing common English words ({error}). "
            "Try a longer passage with more real content."
        )

    if scores is not None:
        summary = pick_summary(sentences, scores, num_sentences)

        st.subheader("Summary")
        for position, sentence in enumerate(summary, start=1):
            st.write(f"{position}. {sentence}")

        # === SECTION 4: KEY TERMS, STATS, CHART ===
        # Day 13: get_feature_names_out. Day 7: st.bar_chart. Day 6: DataFrame
        #
        # CHECKPOINT - after this section runs:
        #   [ ] ten key terms appear as metric cards
        #   [ ] the stats row shows words, reading time, sentences
        #   [ ] the bar chart draws
        #   [ ] editing the text changes all three

        key_terms = extract_key_terms(vectorizer, tfidf_matrix, TOP_KEY_TERMS)

        st.subheader("Key Terms")

        # The digit filter in extract_key_terms can empty the table, if the
        # notes really are nothing but numbers. Ten blank cards under a
        # heading looks broken; one honest line does not.
        if key_terms.empty:
            st.caption("No word-like key terms here - these notes are mostly numbers.")
        else:
            # Days 4-5: st.columns returns a list of column objects you
            # write into. `index % KEY_TERM_COLUMNS` deals them out left to
            # right and wraps to the next row - five per row, two rows.
            columns = st.columns(KEY_TERM_COLUMNS)
            for index, row in key_terms.iterrows():
                columns[index % KEY_TERM_COLUMNS].metric(row["term"], f"{row['weight']:.2f}")

            st.caption(
                "Weight is the word's total TF-IDF importance across every "
                "sentence. Higher means the notes lean on it harder."
            )

        word_count, reading_minutes, sentence_count = compute_stats(text, sentences)

        st.subheader("Stats")
        stat_column_1, stat_column_2, stat_column_3 = st.columns(3)
        stat_column_1.metric("Words", word_count)
        stat_column_2.metric("Reading time", f"{reading_minutes} min")
        stat_column_3.metric("Sentences", sentence_count)

        if not key_terms.empty:
            st.subheader("Word Importance Chart")

            # Day 7: st.bar_chart. set_index("term") tells the chart what
            # to label each bar with; the ["weight"] column gives the
            # heights. No key= here - a chart is a display element, not an
            # input widget, so it has nothing to remember between reruns
            # and Streamlit gives it no key parameter. Passing one is a
            # TypeError.
            st.bar_chart(key_terms.set_index("term")["weight"])

            st.caption(f"The top {len(key_terms)} words by TF-IDF weight.")


# === SECTION 5: FOOTER ===
# POLISH (build step 4, item 3). Outside every `if` above, so it is on
# screen even before anyone has pasted anything.

st.divider()
st.caption("Built with Python, Streamlit, scikit-learn. TF-IDF powered summarization.")
