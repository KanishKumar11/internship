"""
06_styled_chart_demo.py - default vs styled, the same data twice

TEACHES : The four-line styling kit. Same numbers, same chart type, four
          extra lines - and the difference between "a chart" and "a chart
          that tells you something".
SLIDE   : Day 7, Slide 10 - Chart Styling (deck page 10/18)
RUN     : streamlit run 06_styled_chart_demo.py

EXPECTED OUTPUT IN THE BROWSER
    A tab at localhost:8501 titled "Chart Styling - Before and After" with
    two charts side by side.
      LEFT  - default blue bars, no title, no axis labels. You cannot tell
              what it is about without someone standing next to it.
      RIGHT - coral bars with white edges, the navy title "Average Marks by
              City", both axes labelled, faint gridlines, and the value
              printed above each bar (86.9, 83.4, 82.8).
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Brand palette from the deck.
CORAL = "#FF6B5B"
NAVY = "#2A3284"

st.title("Chart Styling - Before and After")

df = pd.read_csv("students.csv")
avg_by_city = df.groupby("city")["marks"].mean()

before_col, after_col = st.columns(2)

# BEFORE - default, no styling ------------------------------------------
with before_col:
    st.subheader("Before - default")

    fig1, ax1 = plt.subplots()
    ax1.bar(avg_by_city.index, avg_by_city.values)
    st.pyplot(fig1)

    st.caption("It works. But what is it about? Nothing on the chart says.")

# AFTER - the four-line styling kit -------------------------------------
with after_col:
    st.subheader("After - styled")

    # figsize sets the ASPECT RATIO and how large the text looks. Streamlit
    # scales the image to the column width either way, so a wide, short
    # figure reads better here than the squarish default.
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(avg_by_city.index, avg_by_city.values, color=CORAL, edgecolor="white")

    # THE 4-LINE STYLING KIT - add these to every Matplotlib chart you
    # ever show another human. Thirty seconds of typing, double the
    # readability. A chart with no title is a puzzle, not an answer.
    ax2.set_title("Average Marks by City", fontsize=14, color=NAVY)
    ax2.set_xlabel("City")
    ax2.set_ylabel("Average Marks")
    ax2.grid(axis="y", alpha=0.3)

    # Bonus fifth line: print the value above each bar, so the reader never
    # has to measure a bar against the axis. ax2.containers[0] is the group
    # of bars the ax2.bar() call just created.
    ax2.bar_label(ax2.containers[0], fmt="%.1f")

    st.pyplot(fig2)

    st.caption("Same data. Four extra lines. Now it tells a story.")

# Gridlines go BEHIND the bars by default in recent Matplotlib. If yours
# draw on top, add ax.set_axisbelow(True) before ax.grid(...).
