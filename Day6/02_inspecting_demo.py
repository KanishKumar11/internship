"""
02_inspecting_demo.py - The three commands you run after every load

TEACHES : head / info / describe, plus the three one-line bonus checks
          (shape, columns, dtypes). Five seconds here saves an hour of
          debugging later.
SLIDE   : Day 6, Slide 7 (Inspecting Data)
RUN     : python 02_inspecting_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    head() -> 5 rows, head(10) -> 10 rows, info() -> 28 non-null entries in
    5 columns (2 numeric + 3 text), describe() -> count/mean/std/min/quartiles
    for age and marks only, then shape (28, 5), the column names and dtypes.

    The text columns show as `object` on pandas 2.x and as `str` on pandas
    3.x. Same data either way - only the label changed.
"""

import pandas as pd

df = pd.read_csv("students.csv")

# === df.head(n) - did the data load the way I expected? ===
print("=== head() - default 5 rows ===")
print(df.head())

print("\n=== head(10) - ask for more when 5 isn't enough ===")
print(df.head(10))

# === df.info() - the structure: dtypes, non-null counts, memory ===
# info() PRINTS its output and returns None, so never do `x = df.info()`.
print("\n=== info() - structure summary ===")
df.info()

# === df.describe() - stats for the NUMERIC columns only ===
# name/city/branch are skipped because mean() of a string is meaningless.
print("\n=== describe() - statistical summary ===")
print(df.describe())

# === The three bonus checks ===
print("\nshape   ->", df.shape)        # (rows, cols) as a plain tuple
print("columns ->", list(df.columns))  # the column names, in order
print("dtypes  ->")
print(df.dtypes)                       # object = text, int64 = whole numbers
