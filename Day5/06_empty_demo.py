"""
06_empty_demo.py - Layout primitive 05b of 05: st.empty

TEACHES : A single-slot placeholder that UPDATES IN PLACE. Writing to it a
          second time replaces the first content instead of adding below it.
          This is how loading states, progress bars and streaming text work.
SLIDE   : Day 5, Slide 10 (right side - st.empty)
RUN     : streamlit run 06_empty_demo.py

EXPECTED OUTPUT IN THE BROWSER
    The word "Loading..." appears for about one second, then is REPLACED
    (not followed) by "Done!". Reload the page to watch it again.
"""

import time

import streamlit as st

st.title("Empty Demo")

# Reserve exactly one slot on the page.
status = st.empty()

status.write("Loading...")

# Pretend we are doing slow work - fetching data, calling an API, etc.
time.sleep(1)

# Writing again REPLACES the slot's contents rather than appending.
status.write("Done!")

# The same idea powers progress bars:
# bar = st.progress(0)
# for step in range(100):
#     bar.progress(step + 1)

# You will meet st.empty again on Day 12 (AI text streaming) and Day 13
# (chatbots), where each new token replaces the previous partial answer.
