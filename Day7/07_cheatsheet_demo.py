"""
07_cheatsheet_demo.py - every Day 7 chart type on one page

TEACHES : Nothing new. Run this to see all five commands from the Day 7
          cheatsheet next to each other, so the choice stops being about
          the API and becomes about the data - which is the real skill.
SLIDE   : Day 7, Slide 11 - Charts Cheatsheet (deck page 11/18)
RUN     : streamlit run 07_cheatsheet_demo.py

EXPECTED OUTPUT IN THE BROWSER
    One long page at localhost:8501 with five numbered sections:
      1. line_chart  - three subject lines rising across tests 1-5
      2. bar_chart   - three bars, Amritsar ~86.9 the tallest
      3. area_chart  - three stacked expense bands, Jan to Apr
      4. metric      - three KPI cards: 84.7 / 95 / 28
      5. pyplot      - the coral marks histogram
    Scroll top to bottom and the decision tree at the end will make sense.
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

CORAL = "#FF6B5B"
NAVY = "#2A3284"

st.title("Day 7 Charts Cheatsheet")
st.write("Every chart command from today, on one page.")

df = pd.read_csv("students.csv")

# 1. st.line_chart - change over time or sequence -----------------------
st.subheader("1. st.line_chart")
marks_by_test = pd.DataFrame(
    {
        "Math": [78, 82, 85, 88, 91],
        "Science": [72, 75, 80, 84, 89],
        "English": [80, 83, 85, 87, 90],
    },
    index=[1, 2, 3, 4, 5],
)
st.line_chart(marks_by_test)
st.caption(
    "USE WHEN the x-axis is time or sequence. "
    "DON'T when categories have no order - use a bar chart."
)

# 2. st.bar_chart - compare across categories ---------------------------
st.subheader("2. st.bar_chart")
avg_by_city = df.groupby("city")["marks"].mean()
st.bar_chart(avg_by_city)
st.caption(
    "USE WHEN comparing distinct categories - height makes the ranking obvious. "
    "DON'T past ~10 categories; the bars get cramped."
)

# 3. st.area_chart - volume and composition -----------------------------
st.subheader("3. st.area_chart")
expenses = pd.DataFrame(
    {
        "Food": [8000, 8500, 9200, 8800],
        "Transport": [3000, 3200, 3500, 3100],
        "Books": [1500, 2200, 1800, 2500],
    },
    index=["Jan", "Feb", "Mar", "Apr"],
)
st.area_chart(expenses)
st.caption(
    "USE WHEN cumulative totals or composition matter. "
    "DON'T if you only want the trend - exact values are harder to read."
)

# 4. st.metric - one important number -----------------------------------
st.subheader("4. st.metric")
avg_col, high_col, count_col = st.columns(3)
avg_col.metric(label="Avg Marks", value=f"{df['marks'].mean():.1f}")
high_col.metric(label="Highest", value=f"{df['marks'].max()}")
count_col.metric(label="Students", value=len(df))
st.caption(
    "USE WHEN one number is the headline. "
    "DON'T for multiple data points - that is a table or a chart."
)

# 5. Matplotlib via st.pyplot - full control ----------------------------
st.subheader("5. Matplotlib via st.pyplot()")
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df["marks"], bins=10, color=CORAL, edgecolor="white")
ax.set_title("Distribution of Marks", fontsize=14, color=NAVY)
ax.set_xlabel("Marks")
ax.set_ylabel("Number of Students")
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
st.caption(
    "USE WHEN you need titles, colours, subplots, annotations. "
    "DON'T for a quick look - the built-ins are one line."
)

# THE DECISION TREE
#   Over time?          -> line_chart
#   Across categories?  -> bar_chart
#   One number?         -> st.metric
#   Volume matters?     -> area_chart
#   Need styling?       -> Matplotlib
st.divider()
st.write(
    "**Decision tree** - Over time? line_chart. Across categories? bar_chart. "
    "One number? st.metric. Volume matters? area_chart. Need styling? Matplotlib."
)
