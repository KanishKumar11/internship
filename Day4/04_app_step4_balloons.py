"""Live Demo Step 4 of 5 — balloons, because a first app deserves a celebration.

Pairs with: Slide 11 (Live Demo Step 4 - st.balloons)
Teaches:    Nothing new about the model - this is the payoff for what already works.
Run it:     streamlit run 04_app_step4_balloons.py
Expected:   Type a name, click "Greet me": the greeting appears AND balloons rise
            across the page for about three seconds.

Step 3 + 1 new line (st.balloons).
"""

import streamlit as st

st.title("My First Streamlit App")

name = st.text_input("What's your name?")

clicked = st.button("Greet me")

if clicked and name:
    st.write(f"Hello, {name}! Welcome to Streamlit.")
    # NEW LINE - celebrate!
    # This is the checkpoint for today: if the balloons fly, then the run-loop,
    # widgets-return-values, and conditionals-drive-UI are all working together.
    st.balloons()
