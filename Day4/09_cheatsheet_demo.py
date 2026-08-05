"""Run this to see every command from the Day 4 cheatsheet in one place.

Pairs with: Slide 14 (the 10 commands you'll use most)
Teaches:    Every st.* command is a plain Python function. It renders something
            on the page AND returns a value. Call it, assign the return, use it.
Run it:     streamlit run 09_cheatsheet_demo.py
Expected:   One scrollable page with all ten widgets, every one of them live:
            change anything and the whole script re-runs with the new values.
"""

import streamlit as st

# 01. st.title - renders an H1 heading. Returns nothing.
st.title("Day 4 Cheatsheet - All 10 Commands")

# 02. st.write - the Swiss-army knife. Renders strings, numbers, dataframes,
#     charts, figures. Returns nothing.
st.write("Every widget below is live. Change one and watch the page re-render.")

# 03. st.text_input - renders a text box. Returns the typed string ("" if empty).
name = st.text_input("Your name")

# 04. st.button - renders a button. Returns True on the click run, False on every
#     other run. That is why it belongs in an `if`, not in an event handler.
if st.button("Say hello"):
    st.write(f"Hello, {name or 'stranger'}!")

# 05. st.slider - renders a slider. Returns the current number.
#     Arguments: label, min, max, default.
age = st.slider("Age", 0, 100, 20)
st.write(f"Slider value: {age}")

# 06. st.selectbox - renders a dropdown. Returns the selected option.
#     With a non-empty list it defaults to the first item, so it is never None.
color = st.selectbox("Favourite colour", ["Red", "Green", "Blue"])

# 07. st.radio - renders radio buttons. Returns the selected option.
#     Same return shape as selectbox; pick radio when the options should all be
#     visible at once.
size = st.radio("T-shirt size", ["S", "M", "L"], horizontal=True)

# 08. st.checkbox - renders a checkbox. Returns True or False.
if st.checkbox("Show my choices"):
    st.write(f"You picked {color} in size {size}.")

# 09. st.columns - splits the page into n side-by-side columns. Returns one
#     container per column; use each as a context manager with `with`.
left_column, right_column = st.columns(2)

with left_column:
    st.write("Left column")
    st.write(f"Colour: {color}")

with right_column:
    st.write("Right column")
    st.write(f"Size: {size}")

# 10. st.sidebar - a container pinned to the left. Every st.* command works on
#     it and returns the same thing it would in the main area.
mood = st.sidebar.selectbox("How's the session going?", ["Great", "Okay", "Lost"])
st.sidebar.write(f"You said: {mood}")
