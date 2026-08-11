"""
04_matplotlib_demo.py - Matplotlib via st.pyplot(): full control

TEACHES : The fig/ax pattern, the four-line styling kit, and the price of
          control - roughly 10 lines where the built-in charts needed 1.
          Also the one chart the built-ins cannot draw: a histogram.
SLIDE   : Day 7, Slide 8 - Matplotlib via st.pyplot() deep-dive
          (deck page 08/18)
RUN     : streamlit run 04_matplotlib_demo.py

EXPECTED OUTPUT IN THE BROWSER
    A tab at localhost:8501 titled "Marks Distribution (Matplotlib)" with
    one wide histogram: coral bars with white edges, the navy title
    "Distribution of Marks", axis labels on both sides, and faint
    horizontal gridlines. Marks run 72 to 95, so the bars cluster on the
    right - most of the class scored above 80.
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Brand palette from the deck - keep charts recognisably ours.
CORAL = "#FF6B5B"
NAVY = "#2A3284"

st.title("Marks Distribution (Matplotlib)")

df = pd.read_csv("students.csv")

# 1. Create a figure and an axis.
#    fig is the whole picture (the canvas Streamlit will render).
#    ax is one plot inside it. figsize is in inches, width x height.
fig, ax = plt.subplots(figsize=(8, 4))

# 2. Plot ON THE AXIS - ax.hist(), not plt.hist().
#    The object-oriented API says exactly which plot you are drawing on, so
#    it keeps working the moment you add a second subplot. plt.hist() draws
#    on whatever figure happens to be "current", which is a guess.
#    A histogram buckets the marks into 10 bins and counts each bucket -
#    it answers "how are marks spread?", not "what did Aarav score?".
ax.hist(df["marks"], bins=10, color=CORAL, edgecolor="white")

# 3. Customise - the four-line styling kit from slide 10.
ax.set_title("Distribution of Marks", fontsize=14, color=NAVY)
ax.set_xlabel("Marks")
ax.set_ylabel("Number of Students")
ax.grid(axis="y", alpha=0.3)

# 4. Pass the FIGURE to Streamlit - the fig object, not the plt module.
#    Streamlit renders it as a static image, so there is no hover or zoom
#    here. That is the trade: styling control instead of interactivity.
st.pyplot(fig)

# USE WHEN you need titles, exact colours, subplots or annotations - a
# chart someone else will look at. For a quick look while you explore,
# st.line_chart and st.bar_chart get you there in one line.
