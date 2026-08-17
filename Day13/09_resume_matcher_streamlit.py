"""
09_resume_matcher_streamlit.py - The matcher, with a face on it

TEACHES : That the whole of today fits behind two text boxes and a button.
          Everything new here is Days 4-5 (widgets, layout, caching); the
          TF-IDF is copied straight out of file 08.
SLIDE   : Day 13, Slide 13 - Extension 1, a Streamlit UI (deck page 13/16)
RUN     : streamlit run 09_resume_matcher_streamlit.py
          NOT `python 09_...` - that prints a warning and does nothing.

WHAT YOU SEE
    Two text areas side by side, pre-filled with the sample resume and job
    description. Press Compare and you get a match-score metric and the
    missing keywords underneath.

REQUIRES
    pip install scikit-learn streamlit
"""

import re

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

IMPORTANCE_THRESHOLD = 0.1

SAMPLE_RESUME = (
    "Python developer with two years of experience. I build REST APIs with "
    "Flask, write SQL queries, and analyse data with pandas. BCA graduate."
)
SAMPLE_JOB = (
    "Python developer wanted. Build REST APIs with Flask, write SQL queries, "
    "and analyse data with pandas. Train machine learning models with "
    "scikit-learn and deploy the machine learning services to AWS."
)


# @st.cache_data remembers the answer for a given pair of texts. Streamlit
# re-runs this whole script top to bottom on every click, so without the
# cache the vectorizer would be rebuilt every time you so much as resize the
# window. The arguments are the cache key, so editing either box recomputes.
@st.cache_data
def match_resume(resume: str, job_description: str) -> tuple[float, list[tuple[str, float]]]:
    """Score a resume against a job and list the keywords it is missing."""
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume, job_description])

    match_score = float(cosine_similarity(vectors[0], vectors[1])[0][0])

    vocabulary = vectorizer.get_feature_names_out()
    job_weights = vectors[1].toarray()[0]
    resume_words = set(re.findall(r"[a-z0-9]+", resume.lower()))

    missing = [
        (word, float(weight))
        for word, weight in zip(vocabulary, job_weights)
        if weight > IMPORTANCE_THRESHOLD and word not in resume_words
    ]
    missing.sort(key=lambda pair: pair[1], reverse=True)
    return match_score, missing


st.title("Resume Matcher")
st.caption("TF-IDF + cosine similarity, running entirely on your laptop.")

left_column, right_column = st.columns(2)

with left_column:
    resume_text = st.text_area(
        "Your resume", value=SAMPLE_RESUME, height=200, key="resume_input"
    )

with right_column:
    job_text = st.text_area(
        "The job description", value=SAMPLE_JOB, height=200, key="job_input"
    )

if st.button("Compare", type="primary", key="compare_button"):
    # Guard BEFORE calling scikit-learn. Two empty strings give the
    # vectorizer no vocabulary at all, and it raises ValueError rather than
    # returning 0.0 - so a friendly message here beats a red traceback.
    if not resume_text.strip() or not job_text.strip():
        st.warning("Fill in both boxes first - there is nothing to compare.")
    else:
        score, missing_keywords = match_resume(resume_text, job_text)

        # st.metric is the right widget for one headline number.
        st.metric("Match score", f"{score:.0%}")

        if score >= 0.50:
            st.success("Strong match - the vocabulary lines up well.")
        elif score >= 0.20:
            st.info("Partial match - some of the job's language is missing.")
        else:
            st.error("Weak match - these two texts have little in common.")

        st.subheader("Missing keywords")
        if missing_keywords:
            st.write(
                "Words the job description leans on that your resume never uses, "
                "heaviest first:"
            )
            for word, weight in missing_keywords:
                st.write(f"- **{word}** (importance {weight:.2f})")
            st.caption(
                "Add the ones you can honestly claim. TF-IDF cannot tell a skill "
                "from a job-ad verb, so read the list before you act on it."
            )
        else:
            st.write("None - your resume covers every important word in the job ad.")
