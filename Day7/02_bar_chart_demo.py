"""
02_bar_chart_demo.py - st.bar_chart: compare values across categories

TEACHES : The groupby + chart pattern. Day 6's pandas produces the summary,
          Day 7's chart draws it. The chart never sees the raw 28 rows -
          "one bar per city" only exists after the aggregation.
SLIDE   : Day 7, Slide 6 - st.bar_chart deep-dive (deck page 06/18)
RUN     : streamlit run 02_bar_chart_demo.py

EXPECTED OUTPUT IN THE BROWSER
    A tab at localhost:8501 titled "Average Marks by City". First the
    aggregated 3-row Series, then a bar chart with exactly three bars:
    Amritsar ~86.9, Jalandhar ~83.4, Ludhiana ~82.8. Hover a bar for its
    value. Amritsar is visibly the tallest - that is the whole point of
    the chart, and it takes two seconds to see.
"""

import pandas as pd
import streamlit as st

st.title("Average Marks by City")

df = pd.read_csv("students.csv")

# groupby FIRST, chart second. This is the pattern behind almost every
# dashboard chart you will ever write: pandas reduces 28 rows to 3 numbers,
# and the chart just draws whatever it is handed.
avg_by_city = df.groupby("city")["marks"].mean()

st.write("**The aggregated data** - a Series, one value per city")
st.dataframe(avg_by_city)

# ONE LINE - the bar chart.
#   - Pass a Series and you get one bar per index entry (what we do here).
#   - Pass a DataFrame and you get a group of bars per row, one colour per
#     column - useful for comparing city AND branch at the same time.
#   - Same interactivity as line_chart: hover, drag to zoom, double-click.
st.bar_chart(avg_by_city)

# USE WHEN you are comparing quantities across distinct categories. Height
# makes the ranking obvious. Past ~10 categories the bars get cramped -
# group them or sort and show the top few.
