"""
09_full_dashboard_solution.py - Closing exercise: INSTRUCTOR SOLUTION

TEACHES : The universal dashboard layout, end to end - metrics for the
          headline, a table for the detail, a chart for the pattern, and
          one filtered DataFrame feeding all three.
SLIDE   : Day 7, Slide 14 - Solution Walkthrough (reveal after students
          have tried 08_full_dashboard_exercise; deck page 14/18)
RUN     : streamlit run 09_full_dashboard_solution.py

EXPECTED OUTPUT IN THE BROWSER
    A dashboard at localhost:8501. Unfiltered it reads 84.7 / 95 / 28
    across the three KPI cards, lists all 28 students, and draws three
    bars (Amritsar 86.9, Jalandhar 83.4, Ludhiana 82.8).
    Pick Branch=BCA and City=Amritsar and everything updates together:
    88.6 / 95 / 10, ten rows in the table, one bar left in the chart.
"""

import pandas as pd
import streamlit as st


def all_option(values: pd.Series) -> list[str]:
    """Build a dropdown option list: "All" first, then each unique value."""
    # The two lines from the slide - ["All"] + df["branch"].unique().tolist()
    # - factored out, because we need exactly the same thing twice.
    return ["All"] + values.unique().tolist()


st.title("Student Dashboard - Full")

# Load the data once. Streamlit reruns this file top-to-bottom on every
# interaction, so the CSV is read again each time - fine for 28 rows.
df = pd.read_csv("students.csv")

with st.sidebar:
    st.write("**Filters**")
    branch = st.selectbox("Branch", all_option(df["branch"]), key="f_branch")
    city = st.selectbox("City", all_option(df["city"]), key="f_city")

# Start from the full table and narrow it once per active filter. Each `if`
# is skipped when the dropdown still says "All", so the filters stack in
# any combination without a single nested condition. This is Day 6's
# pattern, unchanged - only what we do with `filtered` is new today.
filtered = df
if branch != "All":
    filtered = filtered[filtered["branch"] == branch]
if city != "All":
    filtered = filtered[filtered["city"] == city]

# KPI cards - the headline. Call .metric() on the column object, not on st,
# and the card lands inside that column. Format the average to one decimal;
# .mean() returns 84.71428571428571 and nobody needs that on a dashboard.
col1, col2, col3 = st.columns(3)
col1.metric("Avg Marks", f"{filtered['marks'].mean():.1f}")
col2.metric("Highest", f"{filtered['marks'].max()}")
col3.metric("Students", len(filtered))

# The detail.
st.write(f"**Filtered Students** - {len(filtered)} of {len(df)}")
st.dataframe(filtered)

# The pattern. Day 6's groupby produces the summary, Day 7's chart draws
# it - and because it groups `filtered`, not `df`, the chart obeys the
# sidebar like everything else on the page.
st.write("**Average Marks by City**")
avg_by_city = filtered.groupby("city")["marks"].mean()
st.bar_chart(avg_by_city)

# No empty-set guard here on purpose: every branch/city combination in
# students.csv has at least two students. Add a slider (see file 10) and
# an empty result becomes one drag away - that version guards for it.
