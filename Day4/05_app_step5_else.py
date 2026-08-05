"""Live Demo Step 5 of 5 — the else branch. One file, three rendered pages.

Pairs with: Slide 12 (Live Demo Step 5 - else branch) and Slide 13 (three states)
Teaches:    There is no "current page" variable and no router. The values of
            `name` and `clicked` decide what the page shows, and the run-loop
            re-evaluates the whole file on every interaction.
Run it:     streamlit run 05_app_step5_else.py
Expected:   Three states you can cycle through by typing and clicking:
              1. empty box, no click  -> "Type your name above, then click the button."
              2. name typed, no click -> "Hi <name>. Click the button above for a surprise."
              3. name typed + click   -> "Hello, <name>! Welcome to Streamlit." + balloons

Step 4 + the else block.
"""

import streamlit as st

st.title("My First Streamlit App")

name = st.text_input("What's your name?")

clicked = st.button("Greet me")

if clicked and name:
    # State 3 - the happy path.
    st.write(f"Hello, {name}! Welcome to Streamlit.")
    st.balloons()
else:
    # NEW - what shows when the button was NOT clicked (or the box is empty).
    if name:
        # State 2 - we know who they are, they just haven't clicked yet.
        st.write(f"Hi {name}. Click the button above for a surprise.")
    else:
        # State 1 - the first thing anyone sees when the app opens.
        st.write("Type your name above, then click the button.")
