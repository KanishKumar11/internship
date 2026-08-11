"""
08_full_dashboard_exercise.py - Closing exercise: STUDENT SCAFFOLD

TEACHES : The Phase-2 capstone shape - Day 5's sidebar, Day 6's pandas
          filter, Day 7's metrics and charts, in one file. This is the
          pattern every group will reuse in their project.
SLIDE   : Day 7, Slide 13 - Exercise Brief (deck page 13/18)
RUN     : streamlit run 08_full_dashboard_exercise.py

EXPECTED OUTPUT IN THE BROWSER
    Right now: the title, an empty sidebar, three empty columns and the
    full 28-row table. It runs - it is just mostly blank.
    Once you finish the TODOs: two sidebar dropdowns, three KPI cards that
    recalculate as you filter, the shrinking table, and a bar chart of
    average marks by city underneath.

--------------------------------------------------------------------------
THE BRIEF
    Build a Streamlit app that loads students.csv and shows KPI metrics,
    a filtered table, and a bar chart of average marks by city - with
    sidebar filters for branch and city.

REQUIREMENTS
    [ ] Load the CSV with pd.read_csv
    [ ] Sidebar: a branch selectbox ("All" + the unique branches), keyed
    [ ] Sidebar: a city selectbox ("All" + the unique cities), keyed
    [ ] Filter the DataFrame based on both selections (the Day 6 pattern)
    [ ] Three st.metric cards in columns: Average Marks, Highest, Count
    [ ] Show the filtered DataFrame with st.dataframe
    [ ] Show a st.bar_chart of average marks by city (use groupby)

    Every widget gets a unique key - the habit from Day 5.

HOW TO WORK
    Uncomment one TODO at a time, save, and watch the browser reload.
    Fix each error before uncommenting the next one.
--------------------------------------------------------------------------
"""

import pandas as pd
import streamlit as st

st.title("Student Dashboard - Full")

# 1. Load the data -------------------------------------------------------
df = pd.read_csv("students.csv")

# 2. Sidebar filters (from Day 6) ----------------------------------------
with st.sidebar:
    st.write("**Filters**")

    # TODO 1: build the branch dropdown.
    #   "All" goes first so the default state applies no filter at all.
    #   .unique() returns a numpy array, so .tolist() makes it a real list
    #   we can add to ["All"].
    # branches = ["All"] + df["branch"].unique().tolist()
    # branch = st.selectbox("Branch", branches, key="f_branch")

    # TODO 2: build the city dropdown the same way.
    #   Careful - its own options list, and its OWN key.
    # cities = ["All"] + df["city"].unique().tolist()
    # city = st.selectbox("City", cities, key="f_city")

# 3. Filter (from Day 6) -------------------------------------------------
# Start from the full table, then narrow it once per active filter. Each
# `if` is skipped while the dropdown still says "All", so the two filters
# stack in any combination without a single nested condition.
filtered = df

# TODO 3: apply each filter only when it is not "All".
# if branch != "All":
#     filtered = filtered[filtered["branch"] == branch]
# if city != "All":
#     filtered = filtered[filtered["city"] == city]

# 4. KPI metrics (Day 7) -------------------------------------------------
# st.columns(3) gives three side-by-side slots. Call .metric() on each one
# instead of st.metric(), and the card lands inside that column.
col1, col2, col3 = st.columns(3)

# TODO 4: fill the three cards.
#   Format the average to one decimal - .mean() returns 84.71428... and
#   nobody needs seven decimal places on a dashboard.
# col1.metric("Avg Marks", f"{filtered['marks'].mean():.1f}")
# col2.metric("Highest", f"{filtered['marks'].max()}")
# col3.metric("Students", len(filtered))

# 5. Filtered table ------------------------------------------------------
st.write("**Filtered Students**")
st.dataframe(filtered)

# 6. Chart (Day 6 groupby + Day 7 chart) ---------------------------------
# TODO 5: aggregate, then chart. groupby reduces the filtered rows to one
#   average per city; bar_chart draws whatever it is handed.
# st.write("**Average Marks by City**")
# avg_by_city = filtered.groupby("city")["marks"].mean()
# st.bar_chart(avg_by_city)

# Bonus for the extend phase (5 min): add a second chart of marks by
# branch, or a sidebar marks-range slider:
#   st.slider("Marks range", 0, 100, (0, 100), key="f_marks")
