"""
10_full_dashboard_extended.py - the solution plus all three extensions

TEACHES : That the dashboard pattern extends without being rewritten. A
          third filter, a second chart and a Matplotlib figure all bolt on
          to the same `filtered` DataFrame - no new structure needed.
SLIDE   : Day 7, Slide 15 - Extensions (deck page 15/18)
RUN     : streamlit run 10_full_dashboard_extended.py

WHAT IS NEW versus 09_full_dashboard_solution.py
    EXTENSION 1 - a second bar chart, average marks by branch
    EXTENSION 2 - a marks-range slider in the sidebar, stacking with the
                  existing branch and city filters
    EXTENSION 3 - a Matplotlib histogram of the marks distribution

EXPECTED OUTPUT IN THE BROWSER
    A dashboard at localhost:8501. Unfiltered: 84.7 / 95 / 28 across the
    KPI cards, all 28 students, then three charts - marks by city, marks
    by branch (BCA 87.6, BSc-IT 76.1), and the coral histogram.
    Drag the slider to 85-100 and the set drops to 15 students, average
    89.8, with every card and all three charts following along.
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

CORAL = "#FF6B5B"
NAVY = "#2A3284"


def all_option(values: pd.Series) -> list[str]:
    """Build a dropdown option list: "All" first, then each unique value."""
    return ["All"] + values.unique().tolist()


st.title("Student Dashboard - Extended")

df = pd.read_csv("students.csv")

with st.sidebar:
    st.write("**Filters**")
    branch = st.selectbox("Branch", all_option(df["branch"]), key="f_branch")
    city = st.selectbox("City", all_option(df["city"]), key="f_city")

    # === EXTENSION 2 - marks-range slider ===============================
    # Passing a TUPLE as the default value turns st.slider into a range
    # slider, and it returns a tuple back - two numbers from one widget.
    low, high = st.slider("Marks range", 0, 100, (0, 100), key="f_marks")

filtered = df
if branch != "All":
    filtered = filtered[filtered["branch"] == branch]
if city != "All":
    filtered = filtered[filtered["city"] == city]

# The slider filter stacks on top of the other two, exactly like they stack
# on each other. One mask, two conditions - wrap each side in brackets,
# because & binds tighter than >= and the code fails without them.
filtered = filtered[(filtered["marks"] >= low) & (filtered["marks"] <= high)]

# The slider makes an empty result one drag away (try 0-50). Every line
# below assumes at least one row, so stop here rather than print "nan"
# into three KPI cards.
if len(filtered) == 0:
    st.warning("No students match these filters. Widen the marks range.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Avg Marks", f"{filtered['marks'].mean():.1f}")
col2.metric("Highest", f"{filtered['marks'].max()}")
col3.metric("Students", len(filtered))

st.write(f"**Filtered Students** - {len(filtered)} of {len(df)}")
st.dataframe(filtered)

st.write("**Average Marks by City**")
avg_by_city = filtered.groupby("city")["marks"].mean()
st.bar_chart(avg_by_city)

# === EXTENSION 1 - a second chart, average marks by branch =============
# The same two lines as the city chart with one word changed. Two
# breakdowns of the same filtered set answer two different questions:
# "where are the strong students?" and "which course is doing better?".
st.write("**Average Marks by Branch**")
avg_by_branch = filtered.groupby("branch")["marks"].mean()
st.bar_chart(avg_by_branch)

# === EXTENSION 3 - Matplotlib histogram ================================
# The bar charts show averages, which hide the spread - an average of 84
# could be everyone near 84, or half at 72 and half at 95. The histogram
# shows the shape, and Matplotlib lets us style it to match the deck.
st.write("**Marks Distribution**")
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(filtered["marks"], bins=10, color=CORAL, edgecolor="white")
ax.set_title("Marks Distribution", fontsize=14, color=NAVY)
ax.set_xlabel("Marks")
ax.set_ylabel("Number of Students")
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)
