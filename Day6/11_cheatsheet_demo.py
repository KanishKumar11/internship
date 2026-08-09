"""
11_cheatsheet_demo.py - All 10 cheatsheet commands in one place

TEACHES : Nothing new. Run this to see every command from the Day 6 cheatsheet
          in one place, in the order you would actually use them on a fresh
          dataset: load -> inspect -> select -> filter -> sort -> transform.
SLIDE   : Day 6, Slide 13 (pandas Cheatsheet)
RUN     : python 11_cheatsheet_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    Ten numbered sections separated by rules, ending with the per-city average
    marks from groupby - the pivot table, as one line.
"""

import pandas as pd


def section(number: int, title: str) -> None:
    """Print a numbered separator so each command's output is easy to find."""
    print("\n" + "-" * 60)
    print(f"{number:02d}. {title}")
    print("-" * 60)


# 01. pd.read_csv(path) - read a CSV file into a DataFrame.
section(1, 'pd.read_csv("students.csv")')
df = pd.read_csv("students.csv")
print(f"Loaded a DataFrame with {df.shape[0]} rows and {df.shape[1]} columns.")

# 02. df.head(n) - the first n rows. Returns a DataFrame.
section(2, "df.head(3)")
print(df.head(3))

# 03. df.info() - structure: columns, dtypes, non-null counts. Prints, returns None.
section(3, "df.info()")
df.info()

# 04. df.describe() - count/mean/std/min/quartiles/max for numeric columns.
section(4, "df.describe()")
print(df.describe())

# 05. df["col"] - select ONE column. Returns a Series (1D), not a DataFrame.
section(5, 'df["name"]')
names = df["name"]
print(names.head())
print("type:", type(names).__name__)

# 06. df[mask] - filter rows with a boolean mask. Returns a new DataFrame.
section(6, 'df[df["age"] > 20]')
older = df[df["age"] > 20]
print(f"{len(older)} students are older than 20:")
print(older.head())

# 07. df.sort_values("col") - reorder rows. ascending=True by default.
section(7, 'df.sort_values("marks", ascending=False)')
print(df.sort_values("marks", ascending=False).head())

# 08. df.loc[row, col] - label-based selection: row labels + column names.
section(8, 'df.loc[0:3, ["name", "marks"]]')
print(df.loc[0:3, ["name", "marks"]])


# 09. df["new"] = ... - add or overwrite a column.
def to_grade(marks: int) -> str:
    """Turn a mark out of 100 into a letter grade."""
    if marks >= 90:
        return "A"
    if marks >= 80:
        return "B"
    if marks >= 70:
        return "C"
    return "F"


section(9, 'df["grade"] = df["marks"].apply(to_grade)')
df["grade"] = df["marks"].apply(to_grade)
print(df[["name", "marks", "grade"]].head())

# 10. df.groupby("col") - group rows, then aggregate. The pivot table, in code.
section(10, 'df.groupby("city")["marks"].mean()')
print(df.groupby("city")["marks"].mean().round(1))
