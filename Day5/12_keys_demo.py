"""
12_keys_demo.py - The widget-keys habit

TEACHES : What a `key` actually buys you. Two identical text inputs sit side
          by side; only the keyed one can be read from st.session_state,
          reset, or updated by code.
SLIDE   : Day 5, Slide 5 (Widget Keys concept)
RUN     : streamlit run 12_keys_demo.py

EXPECTED OUTPUT IN THE BROWSER
    Two text boxes side by side. Type something different into each, then
    click "Read the keyed widget from session_state": the right-hand value
    is printed back. There is no equivalent way to reach the left-hand one.
"""

import streamlit as st

st.title("Widget Keys Demo")

col_without_key, col_with_key = st.columns(2)

with col_without_key:
    st.write("**Without a key**")
    # Streamlit invents an internal key for us, something like "text_input_0".
    # That name depends on widget ORDER, so it changes the moment we move
    # this widget - which is why we cannot rely on it in code.
    anonymous_name = st.text_input("Your name (no key)")
    st.caption("Only reachable through the returned value.")

with col_with_key:
    st.write("**With a key**")
    # We name it ourselves, so the name is stable and readable from anywhere
    # as st.session_state.user_name
    keyed_name = st.text_input("Your name (keyed)", key="user_name")
    st.caption("Also reachable as st.session_state.user_name")

st.divider()

# Programmatic access: this works ONLY because the widget above has a key.
if st.button("Read the keyed widget from session_state", key="read_button"):
    st.write(f"st.session_state.user_name = {st.session_state.user_name!r}")
    st.write(f"The unkeyed box returned: {anonymous_name!r} (variable only)")
