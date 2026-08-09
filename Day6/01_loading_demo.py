"""
01_loading_demo.py - Loading a CSV into a DataFrame

TEACHES : pd.read_csv() - the one loader that covers 90% of the work, plus the
          five arguments you will actually reach for on real files.
SLIDE   : Day 6, Slide 6 (Loading Data)
RUN     : python 01_loading_demo.py

EXPECTED OUTPUT IN THE TERMINAL
    Shape: (28, 5)
    followed by the first 5 rows (Aarav ... Sanjana), then the same file
    re-loaded with index_col=0 so `name` becomes the row index instead of a
    column.
"""

import pandas as pd

# === Load a CSV ===
# The path is relative to where you RUN python from, not where the file lives.
df = pd.read_csv("students.csv")

# === Quick check that it loaded ===
print("Shape (rows, cols):", df.shape)
print(df.head())

# === The same load, with the arguments worth knowing ===
df_with_options = pd.read_csv(
    "students.csv",
    sep=",",            # the delimiter; use sep="\t" for tab-separated files
    header=0,           # row 0 holds the column names (use header=None if there are none)
    index_col=0,        # use column 0 ("name") as the row index instead of a data column
    nrows=100,          # read at most 100 rows - a lifesaver on million-row files
    encoding="utf-8",   # fixes most "UnicodeDecodeError" crashes on exported files
)

print("\nWith index_col=0 - 'name' is now the index, so only 4 columns remain:")
print(df_with_options.head())

# === Loading straight from a URL (Day 11 preview) ===
# read_csv accepts a URL anywhere it accepts a path - no download step needed.
# url = "https://example.com/data.csv"
# df = pd.read_csv(url)
