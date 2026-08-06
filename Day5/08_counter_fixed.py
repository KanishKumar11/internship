"""
08_counter_fixed.py - session_state preview: THE FIX

TEACHES : st.session_state is a dictionary that SURVIVES reruns. Initialise
          a key once with the `if key not in st.session_state` guard, then
          read and write it freely anywhere in the app.
SLIDE   : Day 5, Slide 11 (right side - the fix)
RUN     : streamlit run 08_counter_fixed.py

EXPECTED OUTPUT IN THE BROWSER
    A "Click me" button and a count that actually climbs: 1, 2, 3, 4, 5...
    every time you click.

PAIRS WITH : 07_counter_broken.py - only the two counter lines differ.
"""

import streamlit as st

st.title("Counter - FIXED")

# Initialise ONCE. On later reruns the key already exists, so this block is
# skipped and the stored value is kept.
if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Click me", key="increment_button"):
    # The value we add to is last run's value, not a fresh 0.
    st.session_state.counter += 1

st.write(f"Count: {st.session_state.counter}")
