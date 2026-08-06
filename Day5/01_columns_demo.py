"""
01_columns_demo.py - Layout primitive 01 of 05: st.columns

TEACHES : Splitting the page into side-by-side panels with st.columns(2),
          placing widgets inside a column using `with col1:`, and returning
          to full width after the `with` blocks end.
SLIDE   : Day 5, Slide 7 (st.columns deep-dive)
RUN     : streamlit run 01_columns_demo.py

EXPECTED OUTPUT IN THE BROWSER
    A title, then TWO panels side by side:
        left  = "Name" text box
        right = "Age" slider
    Below them, a horizontal divider and one sentence that uses BOTH values,
    e.g. "Aarav is 20 years old."
    Typing a name or dragging the slider updates that sentence immediately.
"""

import streamlit as st

st.title("Two Columns Demo")

# st.columns(2) returns a tuple of 2 column objects. We unpack them into
# two variables so each one can be used as a context manager below.
col1, col2 = st.columns(2)

# Anything indented under `with col1:` renders INSIDE the left column.
with col1:
    st.write("**Left column**")
    user_name = st.text_input("Name", key="user_name")

with col2:
    st.write("**Right column**")
    user_age = st.slider("Age", 0, 100, 20, key="user_age")

# We are outside both `with` blocks now, so this is back to FULL width.
st.divider()
st.write(f"{user_name} is {user_age} years old.")

# Uneven columns: pass a list of ratios instead of a number.
# col1, col2 = st.columns([1, 3])   # col2 would be 3x wider than col1
