"""
10_dashboard_extended.py - Closing exercise: EXTENDED VERSION

TEACHES : The three extension ideas layered onto the solution - a marks-range
          slider, a row of st.metric summary stats, and a name search box.
          Five filters, all stacking on the same `filtered` variable.
SLIDE   : Day 6, Slide 17 - Extend (deck page 17/18)
RUN     : streamlit run 10_dashboard_extended.py

EXPECTED OUTPUT IN THE BROWSER
    The Day 6 dashboard with a full sidebar: branch, city, a 0-100 marks range
    slider and a search box. Below the filtered table, three metric cards show
    the average, highest and lowest mark of whatever is currently on screen.
"""

import pandas as pd
import streamlit as st


def all_option(values: pd.Series) -> list[str]:
    """Build a dropdown option list: "All" first, then each unique value."""
    return ["All"] + values.unique().tolist()


st.title("Student Dashboard - Extended")

df = pd.read_csv("students.csv")

with st.sidebar:
    st.write("**Filters**")
    branch = st.selectbox("Branch", all_option(df["branch"]), key="filter_branch")
    city = st.selectbox("City", all_option(df["city"]), key="filter_city")

    # === EXTENSION 1 - marks-range slider =============================
    # Passing a TUPLE as the default turns st.slider into a range slider,
    # so it hands back two values instead of one.
    low, high = st.slider("Marks range", 0, 100, (0, 100), key="filter_marks")

    # === EXTENSION 3 - search box =====================================
    search = st.text_input("Search by name", key="filter_search")

st.write("**All students**")
st.dataframe(df)
st.write(f"Total: {len(df)} students")

# Every filter narrows the same `filtered` variable, in order.
filtered = df
if branch != "All":
    filtered = filtered[filtered["branch"] == branch]
if city != "All":
    filtered = filtered[filtered["city"] == city]

# === EXTENSION 1 - apply the marks range ==============================
# Both ends at once, so wrap each condition in its own parentheses.
filtered = filtered[(filtered["marks"] >= low) & (filtered["marks"] <= high)]

# === EXTENSION 3 - apply the search ===================================
# An empty text_input returns "", which is falsy - so no search, no filter.
# case=False makes "aar", "Aar" and "AAR" all match "Aarav".
if search:
    filtered = filtered[filtered["name"].str.contains(search, case=False)]

st.write(f"**Filtered: {len(filtered)} students**")
st.dataframe(filtered)

# === EXTENSION 2 - summary stats with st.metric =======================
# Three equal columns, one metric each. This is what turns a table into
# something that reads like a dashboard.
if len(filtered) > 0:
    average_col, highest_col, lowest_col = st.columns(3)
    average_col.metric(label="Average", value=f"{filtered['marks'].mean():.1f}")
    highest_col.metric(label="Highest", value=f"{filtered['marks'].max()}")
    lowest_col.metric(label="Lowest", value=f"{filtered['marks'].min()}")
else:
    st.warning("No students match these filters. Widen the range or clear the search.")
