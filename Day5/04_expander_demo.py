"""
04_expander_demo.py - Layout primitive 04 of 05: st.expander

TEACHES : Hiding rare or advanced controls behind a collapsible section so
          the main page stays clean. Widgets inside an expander behave
          exactly like any other widget - they just start out hidden.
SLIDE   : Day 5, Slide 9 (right side - st.expander)
RUN     : streamlit run 04_expander_demo.py

EXPECTED OUTPUT IN THE BROWSER
    A title, a "Your name" text box, and a collapsed grey bar labelled
    "Advanced options". Clicking the bar reveals a Threshold slider and a
    "Use cache" checkbox. The line underneath always shows both values.
"""

import streamlit as st

st.title("Expander Demo")

user_name = st.text_input("Your name", key="user_name")

# expanded=False is the default: the section starts collapsed.
with st.expander("Advanced options", expanded=False):
    threshold = st.slider("Threshold", 0.0, 1.0, 0.5, key="threshold")
    use_cache = st.checkbox("Use cache", value=True, key="use_cache")

# The widgets above still return values even while the expander is closed.
st.write(f"Threshold: {threshold}, Cache: {use_cache}")

# Open the section by default - useful for help text you want people to read:
# st.expander("Help", expanded=True)
