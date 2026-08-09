"""
07_columns_demo.py - Adding and modifying columns

TEACHES : Six ways to fill df["new"] = ... - a constant, column arithmetic,
          .apply() with your own function, overwriting an existing column,
          np.where() for conditional values, and .drop() to remove one.
SLIDE   : Day 6, Slide 12 (Adding + Modifying Columns)
RUN     : python 07_columns_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    Six labelled tables, each showing the first 5 rows after one change:
    a school column, a percentage column, a grade column (A/B/C), the city
    column upper-cased, a passed column of "Yes", and finally the table with
    the school column dropped.

    We print .head() rather than the whole 28-row table so the change stays
    visible on one screen during the live demo.
"""

import numpy as np
import pandas as pd

df = pd.read_csv("students.csv")

# === 1. Add a constant column ===
# One value on the right, and pandas repeats it down every row.
df["school"] = "Hindu College Amritsar"
print("=== 1. Constant column ===")
print(df.head())

# === 2. Column arithmetic ===
# The maths happens element-wise: row 0 with row 0, row 1 with row 1, ...
# No loop needed, and it stays fast on millions of rows.
df["percentage"] = df["marks"] / 100 * 100
print("\n=== 2. Column arithmetic ===")
print(df[["name", "marks", "percentage"]].head())


# === 3. Apply a function row by row ===
def to_grade(marks: int) -> str:
    """Turn a mark out of 100 into a letter grade."""
    if marks >= 90:
        return "A"
    if marks >= 80:
        return "B"
    if marks >= 70:
        return "C"
    return "F"


# .apply() hands each value in the column to the function, one at a time,
# and collects the return values into a new Series.
df["grade"] = df["marks"].apply(to_grade)
print("\n=== 3. .apply(to_grade) ===")
print(df[["name", "marks", "grade"]].head())

# === 4. Modify an existing column ===
# Same syntax as creating one - assigning to a name that already exists
# overwrites it. "Amritsar" becomes "AMRITSAR".
df["city"] = df["city"].str.upper()
print("\n=== 4. Overwrite a column ===")
print(df[["name", "city"]].head())

# === 5. Conditional column with np.where ===
# np.where(condition, value_if_true, value_if_false) - a vectorised if/else.
df["passed"] = np.where(df["marks"] >= 40, "Yes", "No")
print("\n=== 5. np.where ===")
print(df[["name", "marks", "passed"]].head())

# === 6. Drop a column ===
# drop() returns a NEW DataFrame, so we reassign df to keep the result.
df = df.drop(columns=["school"])
print("\n=== 6. After dropping 'school' ===")
print(df.head())
print("\nColumns now:", list(df.columns))
