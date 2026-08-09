"""
03_filtering_basic.py - Filtering with a boolean mask

TEACHES : The two-step pattern that every pandas filter is built on -
          (1) create a mask, (2) use the mask to select rows.
SLIDE   : Day 6, Slide 8 (Filtering - Boolean Masks)
RUN     : python 03_filtering_basic.py

EXPECTED OUTPUT IN THE TERMINAL
    The mask printed as a Series of True/False (one entry per row), then the
    15 students older than 20, then the identical result from the one-liner,
    then proof that the original df still has all 28 rows.
"""

import pandas as pd

df = pd.read_csv("students.csv")

# === Step 1: create a mask ===
# A mask is a Series of True/False - one value per row, same length as df.
mask = df["age"] > 20
print("=== The mask (one True/False per row) ===")
print(mask)

# === Step 2: use the mask to select rows ===
# df[mask] keeps only the rows where the mask is True.
older = df[mask]
print("\n=== df[mask] - only the True rows ===")
print(older)

# === The same thing as a one-liner (what you'll see in real code) ===
older = df[df["age"] > 20]
print(f"\nOne-liner gives the same {len(older)} rows.")

# The original df is UNCHANGED. df[mask] returns a NEW filtered DataFrame.
# Filtering never edits in place - that is why we assign the result to a name.
print(f"df still has {len(df)} rows - filtering did not remove anything.")
