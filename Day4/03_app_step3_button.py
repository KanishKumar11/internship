"""Live Demo Step 3 of 5 — a button, and finally we use `name`.

Pairs with: Slide 10 (Live Demo Step 3 - st.button)
Teaches:    st.button returns a boolean, not an event. You use it in an `if`.
Run it:     streamlit run 03_app_step3_button.py
Expected:   Heading, text box, and a "Greet me" button. Type a name, click the
            button, and "Hello, <name>! Welcome to Streamlit." appears below it.
            Click with an empty box and nothing happens - `and name` guards that.

Step 2 + 2 new lines (the button and the if block).
"""

import streamlit as st

st.title("My First Streamlit App")

name = st.text_input("What's your name?")

# NEW LINE - a button.
# `clicked` is True only on the run triggered by the click, False on every other
# run. There is no event handler to register; it is just a boolean.
clicked = st.button("Greet me")

# We check the name too, otherwise an empty box would greet nobody.
if clicked and name:
    st.write(f"Hello, {name}! Welcome to Streamlit.")
