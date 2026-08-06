"""
02_sidebar_demo.py - Layout primitive 02 of 05: st.sidebar

TEACHES : The dashboard pattern - controls live in the left sidebar, output
          stays in the main area. Same context-manager idea as st.columns.
SLIDE   : Day 5, Slide 8 (st.sidebar deep-dive)
RUN     : streamlit run 02_sidebar_demo.py

EXPECTED OUTPUT IN THE BROWSER
    A left sidebar with THREE controls (Name, Age, Favorite color) and a
    main area with a title plus three lines of output built from those
    values. Changing a sidebar control re-renders the main area; the
    sidebar itself stays exactly where it is.
"""

import streamlit as st

st.title("Dashboard Demo")

# Everything indented under `with st.sidebar:` renders in the LEFT sidebar.
with st.sidebar:
    st.write("**Controls**")
    user_name = st.text_input("Name", key="user_name")
    user_age = st.slider("Age", 0, 100, 20, key="user_age")
    favorite_color = st.selectbox(
        "Favorite color",
        ["Red", "Green", "Blue"],
        key="favorite_color",
    )

# This code is NOT indented under the sidebar block, so it renders in the
# main area - the default target for anything outside a layout context.
st.write(f"Hello, **{user_name}**!")
st.write(f"You are **{user_age}** years old.")
st.write(f"Your favorite color is **{favorite_color}**.")

# Shorthand for a SINGLE sidebar widget - no `with` block needed:
# user_name = st.sidebar.text_input("Name", key="user_name_shorthand")
# The `with` block is cleaner once you have more than one widget.
