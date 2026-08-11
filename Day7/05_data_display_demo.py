"""
05_data_display_demo.py - st.dataframe vs st.table vs st.metric

TEACHES : Not everything is a chart. Three ways to put data on the page,
          and the question that picks between them: does the user need to
          explore it, read it, or just see one number?
SLIDE   : Day 7, Slide 9 - data display comparison (deck page 09/18)
RUN     : streamlit run 05_data_display_demo.py

EXPECTED OUTPUT IN THE BROWSER
    A tab at localhost:8501 titled "Three Ways to Show Data" with three
    sections stacked down the page:
      1. st.dataframe  - all 28 students in a scrollable grid. Click a
         column header to sort; drag a column edge to resize.
      2. st.table      - the first 10 students, rendered flat. Clicking a
         header does nothing, and there is no scrollbar.
      3. st.metric     - one card reading "Avg Marks / 84.7" with a green
         "+2.3" underneath, next to two more cards.
"""

import pandas as pd
import streamlit as st

st.title("Three Ways to Show Data")

df = pd.read_csv("students.csv")

# 1. st.dataframe - the interactive grid -------------------------------
# Sortable, scrollable, resizable columns. This is the default for any
# real table: the user explores it without you writing a single control.
st.subheader("1. st.dataframe - interactive")
st.dataframe(df)
st.caption("Sortable, scrollable, resizable. Use for a full DataFrame.")

# 2. st.table - the static table ---------------------------------------
# Renders every row flat, with no scrollbar and no sorting. That fixed
# view is the feature - use it for a report or a small summary where
# sorting would be a distraction. Pass more than ~20 rows and the page
# just gets very long, so we slice with .head(10) first.
st.subheader("2. st.table - static")
st.table(df.head(10))
st.caption("No interactivity. Use for small, fixed views - 20 rows at most.")

# 3. st.metric - one number, big ---------------------------------------
# The KPI card. `value` is what you show, `delta` is the small change
# indicator under it - green when it starts with +, red with -. Here the
# delta is hardcoded because we have no previous term to compare against;
# in a real dashboard you would compute it.
st.subheader("3. st.metric - one big number")
avg_col, high_col, count_col = st.columns(3)
avg_col.metric(label="Avg Marks", value=f"{df['marks'].mean():.1f}", delta="+2.3")
high_col.metric(label="Highest", value=f"{df['marks'].max()}")
count_col.metric(label="Students", value=len(df))
st.caption("One important number per card. Never a whole table.")

# THE UNIVERSAL DASHBOARD LAYOUT
#   Lead with st.metric for the headline numbers, follow with st.dataframe
#   for the detail, and use charts for the patterns. Metrics answer "how
#   are we doing?", the table answers "who exactly?", the chart answers
#   "where is it coming from?". That is the shape of today's exercise.
