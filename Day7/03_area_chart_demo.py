"""
03_area_chart_demo.py - st.area_chart: a line chart with filled volume

TEACHES : area_chart takes exactly the same DataFrame as line_chart - only
          the function name changes. What changes is the emphasis: filled,
          stacked areas show how much, not just which direction.
SLIDE   : Day 7, Slide 7 - st.area_chart concept (deck page 07/18)
RUN     : streamlit run 03_area_chart_demo.py

EXPECTED OUTPUT IN THE BROWSER
    A tab at localhost:8501 titled "Monthly Expenses by Category" showing
    the 4-row expenses table, then a stacked area chart of three bands -
    Food, Transport, Books - across Jan to Apr. The stack tops out around
    14,500 in March. The same data is drawn again as a line chart at the
    bottom so the trade-off is visible side by side.
"""

import pandas as pd
import streamlit as st

st.title("Monthly Expenses by Category")

# One column per spending category, one row per month. The index holds the
# month names, so it becomes the x-axis - identical shape to the DataFrame
# we passed to line_chart in demo 01.
expenses = pd.DataFrame(
    {
        "Food": [8000, 8500, 9200, 8800],
        "Transport": [3000, 3200, 3500, 3100],
        "Books": [1500, 2200, 1800, 2500],
    },
    index=["Jan", "Feb", "Mar", "Apr"],
)

st.write("**The data we are charting** - rupees per month")
st.dataframe(expenses)

# Same API as line_chart, just a different visual emphasis. The area under
# each line is filled, and Streamlit STACKS the bands by default - so the
# top edge is the monthly total, not the Books figure on its own.
st.area_chart(expenses)

# The trade-off, drawn: stacking makes the total easy and the individual
# values hard. Compare the two charts - reading "Transport in March" off
# the area chart means measuring a band, but the line chart just says 3500.
st.write("**The same data as a line chart** - easier to read exact values")
st.line_chart(expenses)

# USE WHEN volume matters as much as direction: cumulative totals, or the
# composition of a whole over time. If you only want the trend, the line
# chart is the honest choice.
