"""
09_dashboard_solution.py - Closing exercise: INSTRUCTOR SOLUTION

TEACHES : The universal dashboard pattern - load once, build "All"-first option
          lists, then narrow a copy of the DataFrame one filter at a time.
SLIDE   : Day 6, Slide 16 - Solution Walkthrough (reveal after students have
          tried 08_dashboard_exercise; deck page 16/18)
RUN     : streamlit run 09_dashboard_solution.py

EXPECTED OUTPUT IN THE BROWSER
    A dashboard at localhost:8501 with two sidebar dropdowns. The main area
    shows all 28 students, then the filtered set below with its own count and
    the average marks to one decimal. Picking Branch=BCA and City=Amritsar
    leaves 10 students, average 88.6.
"""

import pandas as pd
import streamlit as st


def all_option(values: pd.Series) -> list[str]:
    """Build a dropdown option list: "All" first, then each unique value."""
    return ["All"] + values.unique().tolist()


st.title("Student Dashboard")

# Load the data once. Streamlit reruns this file top-to-bottom on every
# interaction, so the CSV is read again each time - fine for 28 rows.
df = pd.read_csv("students.csv")

with st.sidebar:
    st.write("**Filters**")
    branch = st.selectbox("Branch", all_option(df["branch"]), key="filter_branch")
    city = st.selectbox("City", all_option(df["city"]), key="filter_city")

st.write("**All students**")
st.dataframe(df)
st.write(f"Total: {len(df)} students")

# Start from the full table and narrow it once per active filter. Each `if`
# is skipped when the user leaves the dropdown on "All", so the filters stack
# in any combination without a single nested condition.
filtered = df
if branch != "All":
    filtered = filtered[filtered["branch"] == branch]
if city != "All":
    filtered = filtered[filtered["city"] == city]

st.write(f"**Filtered: {len(filtered)} students**")
st.dataframe(filtered)

# .mean() on an empty column returns NaN, so guard before formatting it.
if len(filtered) > 0:
    st.write(f"Average marks: {filtered['marks'].mean():.1f}")
