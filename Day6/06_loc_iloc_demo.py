"""
06_loc_iloc_demo.py - loc uses labels, iloc uses positions

TEACHES : The label-vs-position distinction, and the slicing difference that
          catches every beginner: loc is inclusive on both ends, iloc is not.
SLIDE   : Day 6, Slide 11 (loc vs iloc)
RUN     : python 06_loc_iloc_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    Four loc examples, four iloc examples, then a side-by-side count proving
    loc[0:3] returns 4 rows while iloc[0:3] returns 3.
"""

import pandas as pd

df = pd.read_csv("students.csv")

# ============================================================
# loc - by LABEL: row index labels and column names
# ============================================================

print("=== df.loc[2] - the row whose index LABEL is 2 ===")
print(df.loc[2])

print("\n=== df.loc[0:3] - labels 0 through 3, INCLUSIVE -> 4 rows ===")
print(df.loc[0:3])

# Pass two lists: which rows, then which columns.
print("\n=== df.loc[[0, 2, 4], ['name', 'marks']] - picked rows + picked columns ===")
print(df.loc[[0, 2, 4], ["name", "marks"]])

# A boolean mask works as the row selector too - filter and pick columns at once.
print("\n=== df.loc[df['age'] > 20, ['name', 'marks']] - mask + columns ===")
print(df.loc[df["age"] > 20, ["name", "marks"]])

# ============================================================
# iloc - by POSITION: row number and column number, like a Python list
# ============================================================

print("\n=== df.iloc[2] - the row at POSITION 2 (the third row) ===")
print(df.iloc[2])

print("\n=== df.iloc[0:3] - positions 0 through 2, EXCLUSIVE -> 3 rows ===")
print(df.iloc[0:3])

print("\n=== df.iloc[0:3, 0:2] - first 3 rows, first 2 columns ===")
print(df.iloc[0:3, 0:2])

# Negative positions work exactly like list indexing. loc cannot do this.
print("\n=== df.iloc[-1] - the last row ===")
print(df.iloc[-1])

# THE KEY DIFFERENCE, in one line:
# loc[0:3] returns 4 rows (inclusive), iloc[0:3] returns 3 rows (exclusive).
print(f"\nloc[0:3] -> {len(df.loc[0:3])} rows | iloc[0:3] -> {len(df.iloc[0:3])} rows")
