"""
07_counter_broken.py - session_state preview: THE BUG

TEACHES : Why a plain Python variable cannot count clicks in Streamlit. The
          script re-runs top to bottom on every interaction, so `counter = 0`
          executes again on every click and wipes the previous value.
SLIDE   : Day 5, Slide 11 (left side - the bug)
RUN     : streamlit run 07_counter_broken.py

EXPECTED OUTPUT IN THE BROWSER
    A "Click me" button and a count. Click it once: "Count: 1". Click it
    ten more times: STILL "Count: 1". The counter never gets past 1.

PAIRS WITH : 08_counter_fixed.py - only the two counter lines differ.
"""

import streamlit as st

st.title("Counter - BROKEN")

# This line runs again on EVERY rerun, so the count is reset before we
# ever get a chance to add to it.
counter = 0

if st.button("Click me", key="increment_button"):
    # We only ever get from 0 to 1, never 1 to 2.
    counter += 1

st.write(f"Count: {counter}")
