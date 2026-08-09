"""
08_dashboard_exercise.py - Closing exercise: STUDENT SCAFFOLD

TEACHES : Day 5's sidebar + Day 6's pandas, combined into the dashboard shape
          every group will reuse in Phase 4.
SLIDE   : Day 6, Slide 15 - Exercise Brief (deck page 15/18; page 14 is the
          section divider)
RUN     : streamlit run 08_dashboard_exercise.py

EXPECTED OUTPUT IN THE BROWSER
    Right now: a title and the full 28-row table, with an empty sidebar.
    Once you finish the TODOs: two sidebar dropdowns that filter the table
    live, and a second table below showing only the matching students.

--------------------------------------------------------------------------
THE BRIEF
    Build a Streamlit app that loads students.csv, displays the full table,
    and lets the user filter by branch and city using sidebar widgets.

REQUIREMENTS
    [ ] Load the CSV with pd.read_csv
    [ ] Show the full DataFrame using st.dataframe
    [ ] Sidebar: a selectbox for branch ("All" + the unique branches)
    [ ] Sidebar: a selectbox for city ("All" + the unique cities)
    [ ] Filter the DataFrame based on both selections
    [ ] Show the filtered DataFrame below the full one

    Every widget gets a unique key - the habit from Day 5.
--------------------------------------------------------------------------
"""

import pandas as pd
import streamlit as st

st.title("Student Dashboard")

# 1. Load the data -------------------------------------------------------
df = pd.read_csv("students.csv")

# 2. Sidebar controls ----------------------------------------------------
with st.sidebar:
    st.write("**Filters**")

    # TODO 1: build the branch dropdown.
    #   "All" goes first so the default state applies no filter at all.
    #   .unique() returns a numpy array, so .tolist() makes it a real list
    #   we can add to ["All"].
    # branch_options = ["All"] + df["branch"].unique().tolist()
    # branch = st.selectbox("Branch", branch_options, key="filter_branch")

    # TODO 2: build the city dropdown the same way.
    #   Careful - it needs its OWN options list and its OWN key.
    # city_options = ["All"] + df["city"].unique().tolist()
    # city = st.selectbox("City", city_options, key="filter_city")

# 3. Show the full data --------------------------------------------------
st.write("**All students**")
st.dataframe(df)
st.write(f"Total: {len(df)} students")

# 4. Filter --------------------------------------------------------------
# TODO 3: start from the full table, then narrow it once per active filter.
#   Each `if` only runs when the user picked something other than "All".
# filtered = df
# if branch != "All":
#     filtered = filtered[filtered["branch"] == branch]
# if city != "All":
#     filtered = filtered[filtered["city"] == city]

# 5. Show the filtered data ----------------------------------------------
# TODO 4: show the result with a count above it.
# st.write(f"**Filtered: {len(filtered)} students**")
# st.dataframe(filtered)

# Bonus for the extend phase: add st.metric for the average marks of the
# filtered set - st.metric(label="Average", value=f"{filtered['marks'].mean():.1f}")
