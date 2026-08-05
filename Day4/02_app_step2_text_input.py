"""Live Demo Step 2 of 5 — a text box that holds what you type.

Pairs with: Slide 9 (Live Demo Step 2 - st.text_input)
Teaches:    Widgets are functions that RETURN a value. Assign the return, like input().
Run it:     streamlit run 02_app_step2_text_input.py
Expected:   The heading, plus a text box labelled "What's your name?". Typing in it
            changes nothing on the page yet - we have not USED `name`. Watch the
            terminal while you type: the script re-runs on every keystroke.

Step 1 + 1 new line (the text_input).
"""

import streamlit as st

st.title("My First Streamlit App")

# NEW LINE - a text input.
# `name` is a string holding whatever the user typed ("" if the box is empty).
# We are deliberately not using it yet, so the page looks static. That is Step 3.
name = st.text_input("What's your name?")
