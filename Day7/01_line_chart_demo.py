"""
01_line_chart_demo.py - st.line_chart: the simplest chart in Streamlit

TEACHES : One line of code turns a DataFrame of numbers into an interactive
          line chart. Each numeric column becomes a line, and the DataFrame's
          index becomes the x-axis - so the index is a design decision, not
          leftover bookkeeping.
SLIDE   : Day 7, Slide 5 - st.line_chart deep-dive (deck page 05/18)
RUN     : streamlit run 01_line_chart_demo.py

EXPECTED OUTPUT IN THE BROWSER
    A tab at localhost:8501 titled "Marks Trend by Subject". First the small
    5-row table we are charting, then one chart with three rising lines -
    Math, Science, English - across test numbers 1 to 5, with a legend.
    Hover any point for its value, drag sideways to zoom, double-click to
    reset. All of that comes free with the single st.line_chart call.
"""

import pandas as pd
import streamlit as st

st.title("Marks Trend by Subject")

# One column per subject, one row per test. We set the index to the test
# number because line_chart reads the index as the x-axis - leave it as the
# default 0,1,2,3,4 and the chart silently starts at "test 0".
marks_by_test = pd.DataFrame(
    {
        "Math": [78, 82, 85, 88, 91],
        "Science": [72, 75, 80, 84, 89],
        "English": [80, 83, 85, 87, 90],
    },
    index=[1, 2, 3, 4, 5],
)

st.write("**The data we are charting**")
st.dataframe(marks_by_test)

# THE WHOLE CHART - one line of code.
#   - Each numeric column becomes a line. The index becomes the x-axis.
#   - Colours are automatic. Streamlit also builds the legend and the axes.
#   - Interactive by default: hover for values, drag to zoom, double-click
#     to reset. You do not write a single line for any of that.
st.line_chart(marks_by_test)

# USE WHEN the x-axis is time or a sequence and you want to show change.
# For distinct categories with no natural order (cities, branches), the
# ranking matters more than the trend - use st.bar_chart instead.
