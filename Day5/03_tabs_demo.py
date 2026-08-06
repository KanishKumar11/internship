"""
03_tabs_demo.py - Layout primitive 03 of 05: st.tabs

TEACHES : Splitting a page into tabbed sections so only one view is visible
          at a time. Widget values persist when you switch tabs, because
          each keyed widget keeps its value in session_state.
SLIDE   : Day 5, Slide 9 (left side - st.tabs)
RUN     : streamlit run 03_tabs_demo.py

EXPECTED OUTPUT IN THE BROWSER
    Three tab headers at the top: Input | Chart | Raw Data.
    "Input" holds a name box and an age slider, the other two hold
    placeholder text. Type a name, switch to "Chart", switch back - the
    name is still there.
"""

import streamlit as st

st.title("Tabs Demo")

# st.tabs takes a list of labels and returns one tab object per label,
# in the same order.
tab_input, tab_chart, tab_raw = st.tabs(["Input", "Chart", "Raw Data"])

with tab_input:
    st.write("**Enter your details**")
    user_name = st.text_input("Name", key="user_name")
    user_age = st.slider("Age", 0, 100, 20, key="user_age")
    st.write(f"{user_name} is {user_age} years old.")

with tab_chart:
    st.write("Chart goes here")
    st.caption("Real charts arrive on Day 7 - Charts & Dashboards.")

with tab_raw:
    st.write("Raw data goes here")
    st.caption("Real dataframes arrive on Day 6 - Working With Data.")
