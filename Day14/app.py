"""
app.py - Resume Matcher

WHAT IT DOES
    Upload a resume PDF, paste a job description, and find out how well the
    two match. You get a percentage score, the keywords the job asks for
    that your resume never mentions, the ones it does, and a chart ranking
    all of them by importance.

    This is, roughly, what a real ATS (Applicant Tracking System) does to
    your resume before a human ever reads it.

WHICH DAYS THIS COMBINES
    Day 2      functions, conditionals, loops
    Days 4-5   Streamlit widgets, layout, sidebar, session_state
    Day 6      pandas DataFrames
    Day 7      charts (st.bar_chart)
    Day 11     regex cleaning, PDF text extraction with PyPDF2
    Day 13     TF-IDF vectorization and cosine similarity with scikit-learn

    Nothing in this file is new. Every piece is something you have already
    built. Today is about wiring them together into one working app.

HOW TO RUN IT
    pip install streamlit scikit-learn PyPDF2 pandas
    streamlit run app.py

    Then open http://localhost:8501 in a browser. Streamlit usually opens
    it for you.

HOW THIS FILE IS ORGANISED
    IMPORTS
    CONFIGURATION      the two thresholds that control the keyword lists
    HELPER FUNCTIONS   the four functions that do the actual work
    SECTION 1          title and sidebar
    SECTION 2          file upload and text extraction
    SECTION 3          job description input
    SECTION 4          compare button and match score
    SECTION 5          missing and found keywords
    SECTION 6          keyword importance chart
    SECTION 7          footer

    The helper functions are all defined BEFORE the UI, because Streamlit
    runs this file from top to bottom every single time you touch a widget.
    A function has to exist before the line that calls it.
"""

# === IMPORTS ===

import re  # Day 11: regex, for cleaning the extracted text

import pandas as pd  # Day 6: DataFrames, for the keyword tables and the chart
import streamlit as st  # Days 4-5: the whole user interface

# Day 13: the two scikit-learn pieces. TfidfVectorizer turns text into
# numbers; cosine_similarity compares two sets of numbers. They live in
# different sub-packages because scikit-learn keeps "prepare the data" and
# "measure the data" apart.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Day 11: PyPDF2 3.x was renamed to pypdf by the same author, with an
# identical API. Trying PyPDF2 first and falling back means this app runs
# on whichever one is installed, so nobody loses ten minutes to an
# ImportError on a laptop that happens to have the newer package.
try:
    from PyPDF2 import PdfReader
except ImportError:
    from pypdf import PdfReader


# === CONFIGURATION ===
# Two numbers control which words end up in the keyword tables. They are up
# here, named, instead of buried in the code, so you can tune them in one
# place and see immediately what they do.

# "This word matters in the job description." TF-IDF weights in a two
# document comparison mostly land between 0.0 and 0.5, so 0.05 keeps the
# words the employer actually leans on and drops the ones mentioned once
# in passing.
JOB_IMPORTANCE_THRESHOLD = 0.05

# "This word is essentially absent from the resume." Not 0.0 exactly,
# because a word buried in a very long resume can carry a tiny non-zero
# weight while contributing nothing meaningful.
RESUME_ABSENCE_THRESHOLD = 0.01

# How many keywords to draw in the chart. Twenty bars is readable on a
# projector; sixty is a smear.
MAX_CHART_KEYWORDS = 20


# === HELPER FUNCTIONS ===
# Four functions, each doing one job. Keeping them separate from the UI
# means you can reason about the logic without Streamlit in the way - and
# it is why Section 4 reads as four plain lines instead of forty.


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract all text from an uploaded PDF file.
    Day 11 skill: PyPDF2 PdfReader + page.extract_text().

    Streamlit's UploadedFile behaves like an open file, so PdfReader takes
    it directly - there is no need to save it to disk first.

    Args:
        uploaded_file: The object returned by st.file_uploader.

    Returns:
        The extracted text as a single string. Empty string if extraction
        fails, so the caller can just check `if not text:` rather than
        catching exceptions of its own. Failure is normal here - scanned
        resumes are images, and an image has no text to extract.
    """
    try:
        reader = PdfReader(uploaded_file)

        # A valid PDF with zero pages is unusual but possible, and looping
        # over it would silently return "" with no explanation.
        if len(reader.pages) == 0:
            st.error("This PDF has no pages in it.")
            return ""

        # Build the text one page at a time. Day 2: a loop and an
        # accumulator - exactly the pattern from the file I/O session.
        extracted_pages = []
        for page in reader.pages:
            # extract_text() returns None, not "", on a page with no text
            # layer - a scan, for instance. Appending None to a list of
            # strings and then joining raises TypeError, so `or ""` turns
            # that None into something harmless.
            page_text = page.extract_text() or ""
            extracted_pages.append(page_text)

        return "\n".join(extracted_pages)

    except Exception as error:
        # A broad except on purpose. PyPDF2 raises several different error
        # types for corrupt files, encrypted files and unsupported
        # compression, and to the user they all mean the same thing:
        # this file did not work.
        st.error(f"Could not read this PDF: {error}")
        return ""


def clean_text(raw_text: str) -> str:
    """
    Clean raw text for TF-IDF processing.
    Day 11 skill: regex (re.sub) for removing noise.

    Removes: emails, phone numbers, extra whitespace, special characters.
    Keeps: letters, digits, and single spaces.

    Why bother? Every unique word in a document pushes the match score
    DOWN, because cosine similarity divides by the length of the vector.
    An email address contributes nothing to a job match but still takes up
    room in the vector, so removing it is worth real points.

    Args:
        raw_text: The raw text extracted from a PDF or pasted by user.

    Returns:
        Cleaned text ready for TF-IDF vectorization.
    """
    # STEP 1 - remove email addresses.
    # \S+ means "one or more non-space characters". Crude, but an email
    # address never contains a space, so anything wrapped around an @ with
    # no spaces is one. Left in, "kanika.sharma@example.com" becomes a
    # token that appears in no job description ever written.
    text = re.sub(r"\S+@\S+", "", raw_text)

    # STEP 2 - remove phone numbers.
    # An optional +, then a digit, then at least 8 more digits, spaces or
    # dashes, then a final digit. Same pattern as the Day 11 resume
    # extractor. It catches "+91 98765 43210" and "9876543210" alike.
    text = re.sub(r"\+?\d[\d\s-]{8,}\d", "", text)

    # STEP 3 - normalise whitespace.
    # PDF extraction produces ragged text: double spaces, stray newlines,
    # tabs where a table used to be. \s+ matches any run of whitespace and
    # collapses it to a single space, so the text becomes one clean line.
    text = re.sub(r"\s+", " ", text)

    # STEP 4 - remove special characters.
    # The ^ inside [] means NOT, so this deletes anything that is not a
    # letter, a digit or a space: bullet points, pipes, brackets, the
    # decorative dashes people put in resume headers.
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # STEP 5 - trim the ends.
    # Steps 1 and 2 leave gaps where they deleted things, and step 3 turned
    # those gaps into spaces. .strip() removes the ones at the very start
    # and end.
    return text.strip()


def compute_match_score(resume_text: str, job_text: str) -> tuple:
    """
    Compute TF-IDF + cosine similarity match score.
    Day 13 skill: TfidfVectorizer + cosine_similarity.

    This is the 5-line pattern from Day 13, wrapped in a function.

    Args:
        resume_text: Cleaned resume text.
        job_text: Cleaned job description text.

    Returns:
        A tuple of (score, vectorizer, vectors) where:
        - score: float between 0 and 1
        - vectorizer: the fitted TfidfVectorizer (for keyword extraction)
        - vectors: the TF-IDF matrix (for keyword analysis)

        The vectorizer and vectors come back too so Section 5 can reuse
        them. Refitting them there would waste the work and, worse, could
        produce a keyword list that disagreed with the score above it.
    """
    # stop_words='english' removes common words like "the", "is", "a".
    # This is not optional. Leave it out and those words - which appear in
    # every English sentence ever written - carry as much weight as
    # "Python", so every resume looks like a decent match for every job
    # and the score stops meaning anything.
    vectorizer = TfidfVectorizer(stop_words="english")

    # fit_transform takes a LIST of strings, not a single string. The
    # square brackets are load-bearing: pass a bare string and scikit-learn
    # treats each CHARACTER as a document, which produces nonsense rather
    # than an error.
    # vectors[0] = resume, vectors[1] = job description - the order we
    # passed them in, and the order Section 5 relies on.
    vectors = vectorizer.fit_transform([resume_text, job_text])

    # cosine_similarity returns a 2D array (every row compared with every
    # row), so take [0][0] for the float. The 0:1 and 1:2 slice form keeps
    # each argument 2-dimensional, which works across all scikit-learn
    # versions - vectors[0] alone changed behaviour between releases.
    score = float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0])

    return score, vectorizer, vectors


def find_missing_keywords(vectorizer, vectors, resume_text: str) -> tuple:
    """
    Find keywords from the job description that are missing from the resume.
    Day 13 skill: get_feature_names_out() + TF-IDF weight analysis.

    This is the genuinely useful half of the app. A score tells someone
    they got 41%; the missing keywords tell them what to write next.

    Args:
        vectorizer: The fitted TfidfVectorizer.
        vectors: The TF-IDF matrix from fit_transform.
        resume_text: The cleaned resume text (to check which words appear).

    Returns:
        A tuple of (missing_df, found_df) where each is a pandas DataFrame
        with columns: keyword, importance. Sorted by importance descending.
    """
    # The vocabulary: every word the vectorizer decided to keep, in
    # alphabetical order. The TF-IDF rows line up with this list position
    # by position, which is what makes the loop below work.
    feature_names = vectorizer.get_feature_names_out()

    # The matrix is "sparse" - mostly zeros, stored compactly to save
    # memory. .toarray()[0] expands one row into a plain list of floats we
    # can index by number.
    resume_vector = vectors[0].toarray()[0]  # TF-IDF weights for the resume
    job_vector = vectors[1].toarray()[0]  # TF-IDF weights for the job description

    missing_keywords = []
    found_keywords = []

    # Day 2: a plain loop with an index, so we can look up the same
    # position in three lists at once. A comprehension would fit on one
    # line here and be far harder to read at a glance.
    for index in range(len(feature_names)):
        word = feature_names[index]
        job_importance = job_vector[index]
        resume_importance = resume_vector[index]

        # The 0.05 threshold means "this word matters in the job
        # description". Words below it are mentioned once in passing and
        # are not worth telling the candidate about.
        if job_importance <= JOB_IMPORTANCE_THRESHOLD:
            continue

        # The 0.01 check means "this word is essentially absent from the
        # resume". Anything above it, the candidate has already said.
        if resume_importance < RESUME_ABSENCE_THRESHOLD:
            missing_keywords.append({"keyword": word, "importance": round(float(job_importance), 3)})
        else:
            found_keywords.append({"keyword": word, "importance": round(float(job_importance), 3)})

    # Day 6: turn the lists of dicts into DataFrames. pd.DataFrame handles
    # an empty list fine, but the result has no columns at all - so name
    # them explicitly, or Section 5 crashes on a perfect-match resume.
    missing_df = pd.DataFrame(missing_keywords, columns=["keyword", "importance"])
    found_df = pd.DataFrame(found_keywords, columns=["keyword", "importance"])

    # Most important gap first - the order a candidate would want to read.
    # reset_index(drop=True) throws away the old row numbers so the tables
    # read 0, 1, 2 rather than 47, 12, 3.
    missing_df = missing_df.sort_values("importance", ascending=False).reset_index(drop=True)
    found_df = found_df.sort_values("importance", ascending=False).reset_index(drop=True)

    return missing_df, found_df


# === SECTION 1: TITLE + SIDEBAR ===
# Days 4-5: st.title, st.sidebar

# set_page_config must be the FIRST Streamlit call in the file. Put any
# other st.* line above it and Streamlit raises an error.
st.set_page_config(page_title="Resume Matcher", page_icon="📄", layout="wide")

st.title("Resume Matcher")
st.write("Upload your resume and paste a job description to see how well they match.")

# `with st.sidebar:` puts everything indented under it into the left panel.
# Instructions belong here rather than in the main column, where they would
# push the actual app below the fold.
with st.sidebar:
    st.header("How it works")
    st.write(
        """
        1. Upload your resume as a PDF.
        2. Paste the job description you are applying to.
        3. Press **Compare**.
        4. Read the missing keywords and rewrite your resume.
        """
    )

    st.header("Skills used")
    st.write(
        """
        - **Day 11** - PyPDF2 text extraction, regex cleaning
        - **Day 13** - TF-IDF, cosine similarity
        - **Days 4-5** - Streamlit widgets and layout
        - **Day 6** - pandas DataFrames
        - **Day 7** - bar charts
        """
    )

    st.caption(
        "A word-counting model. It measures vocabulary overlap, not whether "
        "you can do the job."
    )


# === SECTION 2: FILE UPLOAD + TEXT EXTRACTION ===
# Day 11: st.file_uploader, PyPDF2, regex cleaning

st.subheader("1. Your resume")

# type=["pdf"] makes the browser's file picker filter to PDFs, and
# Streamlit rejects anything else before our code ever sees it - one whole
# class of error handled by one argument.
uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"], key="resume_upload")

# resume_text starts empty. Section 4 checks it to decide whether there is
# anything to compare, and it must exist either way - Streamlit runs this
# file top to bottom, so a variable defined only inside the `if` below
# would not exist on the first run.
resume_text = ""

if uploaded is not None:
    raw_text = extract_text_from_pdf(uploaded)

    if not raw_text.strip():
        # An empty result almost always means a scanned resume: the page is
        # a photograph of text, and PyPDF2 reads text, not pictures.
        # Reading those needs OCR, which is a different tool entirely.
        st.warning("Could not extract text from this PDF. It may be a scanned document.")
    else:
        # Day 11: run the regex pipeline before anything touches TF-IDF.
        resume_text = clean_text(raw_text)

        # Show the cleaned text, not the raw text. Students should SEE what
        # the regex did - and if a score later looks wrong, this box is the
        # first place to look for why.
        st.text_area(
            "Extracted resume text", resume_text, height=200, key="resume_text_display"
        )
        st.success(f"Extracted {len(resume_text)} characters.")
else:
    st.info("Upload a resume PDF to begin.")


# === SECTION 3: JOB DESCRIPTION INPUT ===
# Day 5: st.text_area

st.subheader("2. The job description")

# Just an input. Nothing is computed here - the app stays quiet until the
# user presses Compare in Section 4. Recomputing on every keystroke would
# be both slow and confusing.
job_desc = st.text_area(
    "Paste the job description",
    height=150,
    key="job_desc_input",
    placeholder="Looking for a Python engineer with...",
)


# === SECTION 4: COMPARE BUTTON + MATCH SCORE ===
# Day 13: TfidfVectorizer, cosine_similarity, st.metric, st.progress

st.subheader("3. Compare")

# Days 4-5: session_state is Streamlit's memory between reruns. A button is
# True only on the run where it was clicked, so without this the results
# would vanish the instant the user scrolled or resized the window. Storing
# them here lets Sections 5 and 6 stay separate blocks of code that render
# whenever there is something to show.
if "results" not in st.session_state:
    st.session_state["results"] = None

if st.button("Compare", key="compare_btn", type="primary"):
    # Validate before computing. TfidfVectorizer raises ValueError on empty
    # input ("empty vocabulary"), and a red traceback is a terrible way to
    # tell someone they forgot to upload a file.
    if not resume_text:
        st.error("Upload a resume PDF first.")
        st.session_state["results"] = None
    elif not job_desc.strip():
        st.error("Paste a job description first.")
        st.session_state["results"] = None
    else:
        try:
            # Day 11: clean the pasted job description the same way as the
            # resume. Both sides must go through the same pipeline, or
            # differences in punctuation show up as differences in meaning.
            cleaned_job = clean_text(job_desc)

            # Day 13: the whole comparison, in one call.
            score, vectorizer, vectors = compute_match_score(resume_text, cleaned_job)

            missing_df, found_df = find_missing_keywords(vectorizer, vectors, resume_text)

            # Keep everything Sections 5 and 6 need in one dict.
            st.session_state["results"] = {
                "score": score,
                "keyword_count": len(vectorizer.get_feature_names_out()),
                "missing_df": missing_df,
                "found_df": found_df,
            }

        except ValueError as error:
            # The realistic failure: after stop-word removal one of the two
            # texts had no usable words left. A resume of pure punctuation,
            # or a job description reading "the and a".
            st.error(
                f"Could not compare these two texts: {error}. "
                "One of them may have no real words left after cleaning."
            )
            st.session_state["results"] = None

# Read the results back out. This runs on EVERY rerun, not just the one
# where the button was clicked, which is exactly why the output stays on
# screen while the user scrolls around.
results = st.session_state["results"]

if results is not None:
    match_score = results["score"]

    st.subheader("Results")

    # Days 4-5: three columns, so the headline numbers sit side by side
    # instead of stacked down the page.
    col1, col2, col3 = st.columns(3)

    # st.metric is the right widget for a single headline number - big
    # type, its own label, nothing else competing with it.
    col1.metric("Match Score", f"{match_score * 100:.0f}%")

    # Day 2: a chained conditional expression. Reads as "Strong if above
    # 0.5, otherwise Partial if above 0.3, otherwise Weak."
    verdict = "Strong" if match_score > 0.5 else "Partial" if match_score > 0.3 else "Weak"
    col2.metric("Verdict", verdict)

    col3.metric("Keywords Analyzed", results["keyword_count"])

    # st.progress wants a float from 0.0 to 1.0, which is exactly the range
    # cosine similarity produces - no conversion needed.
    st.progress(match_score)

    # === SECTION 5: MISSING KEYWORDS + FOUND KEYWORDS ===
    # Day 13: get_feature_names_out, TF-IDF weight analysis
    # Day 6: st.dataframe

    missing_df = results["missing_df"]
    found_df = results["found_df"]

    # Both tables empty means the job description had no usable words left
    # after stop-word removal - someone pasted "the and a is of", or a
    # single word. Without this branch the app would cheerfully announce
    # "nothing missing" directly underneath a 0% score, which is nonsense.
    if missing_df.empty and found_df.empty:
        st.warning(
            "No keywords to analyse. The job description has no meaningful words "
            "left after removing common English words - paste a longer one."
        )
    elif not missing_df.empty:
        st.subheader(f"Missing Keywords ({len(missing_df)})")
        st.write(
            "These keywords from the job description are NOT in your resume. "
            "Consider adding them."
        )
        # Day 6: st.dataframe renders a pandas DataFrame as a sortable
        # table. hide_index=True drops the 0, 1, 2 column, which carries no
        # information for the reader. width="stretch" makes the table fill
        # the page - it replaced the older use_container_width=True, which
        # still works but prints a deprecation box on top of your app.
        st.dataframe(missing_df, width="stretch", hide_index=True, key="missing_table")
        st.caption(
            "Add the ones you can honestly claim. TF-IDF cannot tell a skill "
            "from a job-ad verb, so read the list before you act on it."
        )
    else:
        st.success("Nothing missing - your resume covers every important word in the job ad.")

    if not found_df.empty:
        st.subheader(f"Keywords Found ({len(found_df)})")
        st.write(
            "These keywords from the job description ARE in your resume. Good match."
        )
        st.dataframe(found_df, width="stretch", hide_index=True, key="found_table")

    # === SECTION 6: KEYWORD IMPORTANCE CHART ===
    # Day 7: st.bar_chart
    # Day 6: pandas DataFrame for the chart data

    # Day 6: pd.concat stacks the two tables into one. .copy() first,
    # because adding the status column below would otherwise modify the
    # DataFrames still being displayed in Section 5.
    missing_for_chart = missing_df.copy()
    found_for_chart = found_df.copy()
    missing_for_chart["status"] = "Missing"
    found_for_chart["status"] = "Found"

    chart_data = pd.concat([missing_for_chart, found_for_chart], ignore_index=True)

    if not chart_data.empty:
        st.subheader("Keyword Importance Chart")

        # Keep only the most important keywords. A real job ad yields sixty
        # or more, and sixty bars on a projector is an unreadable smear.
        chart_data = chart_data.sort_values("importance", ascending=False)
        chart_data = chart_data.head(MAX_CHART_KEYWORDS)

        # Then sort ascending, so the most important keyword ends up at the
        # top of a horizontal bar chart rather than buried at the bottom.
        chart_data = chart_data.sort_values("importance", ascending=True)

        # Day 7: st.bar_chart. set_index("keyword") tells the chart what to
        # label each bar with; the ["importance"] column supplies the
        # lengths. horizontal=True keeps long words readable - vertical
        # bars would print "scikit" sideways.
        # No key= here: st.bar_chart is a display element, not an input
        # widget, so it has nothing to remember between reruns and
        # Streamlit gives it no key parameter. Passing one is a TypeError.
        st.bar_chart(
            chart_data.set_index("keyword")["importance"],
            horizontal=True,
        )

        st.caption(
            f"Showing the top {len(chart_data)} keywords by TF-IDF importance in "
            "the job description. Longer bar = the employer leaned on that word harder."
        )

        # Day 6: a filtered DataFrame, so the chart's colourless bars still
        # tell you which ones are the gaps.
        missing_in_chart = chart_data[chart_data["status"] == "Missing"]
        st.write(f"Of those, **{len(missing_in_chart)}** are missing from your resume.")


# === SECTION 7: FOOTER ===

st.divider()
st.write("Built with Python, Streamlit, scikit-learn, and PyPDF2.")
st.write("The same technique behind real ATS (Applicant Tracking) systems.")
