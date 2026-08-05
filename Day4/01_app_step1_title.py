"""Live Demo Step 1 of 5 — a heading on the page.

Pairs with: Slide 8 (Live Demo Step 1 - st.title)
Teaches:    A Streamlit app is a normal Python file. One import, one function call.
Run it:     streamlit run 01_app_step1_title.py
Expected:   A browser tab opens at http://localhost:8501 showing a single big
            heading, "My First Streamlit App". Nothing else on the page.
"""

# Aliased as `st` by convention - every Streamlit command starts with st.
import streamlit as st

# st.title renders an H1 heading. It is a plain function call, not markup.
st.title("My First Streamlit App")
