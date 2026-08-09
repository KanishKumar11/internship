"""
05_sorting_demo.py - Reordering rows with sort_values

TEACHES : sort_values on one column, on many columns, in both directions, plus
          the reset_index(drop=True) habit that keeps the index readable.
SLIDE   : Day 6, Slide 10 (Sorting)
RUN     : python 05_sorting_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    Lowest marks first (Rohit, 72), then highest first (Jasleen, 95), then
    grouped by city A-Z with the top scorer of each city first, and finally
    the same top-first table with a clean 0,1,2,3... index.
"""

import pandas as pd

df = pd.read_csv("students.csv")

# === Sort by one column, ascending (the default) ===
lowest_first = df.sort_values("marks")
print("=== sort_values('marks') - lowest marks first ===")
print(lowest_first.head())

# === Sort by one column, descending ===
top_first = df.sort_values("marks", ascending=False)
print("\n=== ascending=False - highest marks first ===")
print(top_first.head())

# === Sort by multiple columns ===
# City A-Z first; inside each city, marks high-to-low.
# The ascending list lines up position-by-position with the column list.
city_then_marks = df.sort_values(["city", "marks"], ascending=[True, False])
print("\n=== city A-Z, then marks high-low within each city ===")
print(city_then_marks.head(10))

# === Reset the index after sorting ===
# Sorting keeps each row's ORIGINAL index label, so the left column comes out
# shuffled (20, 8, 25...). drop=True renumbers 0,1,2... and throws the old
# labels away instead of storing them as a new column.
ranked = df.sort_values("marks", ascending=False).reset_index(drop=True)
print("\n=== .reset_index(drop=True) - a clean 0,1,2... index ===")
print(ranked.head())

# === Sorting in place (rare - prefer the copy above) ===
# inplace=True modifies df directly and returns None, so never assign it:
#     df = df.sort_values("marks", inplace=True)   # df becomes None!
# df.sort_values("marks", inplace=True)
