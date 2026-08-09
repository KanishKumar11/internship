"""
04_filtering_advanced.py - Combining conditions: AND, OR, contains, isin

TEACHES : The four patterns that cover almost every real filter, and the
          parentheses rule that beginners trip over every single time.
SLIDE   : Day 6, Slide 9 (Filtering - Advanced Patterns)
RUN     : python 04_filtering_advanced.py

EXPECTED OUTPUT IN THE TERMINAL
    Four filtered tables with a count above each:
      1. AND      -> 10 BCA students from Amritsar
      2. OR       -> 7 students aged under 20 or over 22
      3. contains -> 5 names containing a capital "A"
      4. isin     -> 20 students from Amritsar or Jalandhar
"""

import pandas as pd

df = pd.read_csv("students.csv")

# === 1. Multiple conditions: AND ===
# & is "bitwise and". Both conditions must be True for the row to survive.
# Each condition is wrapped in its OWN parentheses - see the GOTCHA below.
amritsar_bca = df[
    (df["city"] == "Amritsar") &
    (df["branch"] == "BCA")
]
print(f"=== 1. AND - Amritsar AND BCA ({len(amritsar_bca)} students) ===")
print(amritsar_bca)

# === 2. Multiple conditions: OR ===
# | is "bitwise or". Either condition being True is enough.
young_or_old = df[
    (df["age"] < 20) |
    (df["age"] > 22)
]
print(f"\n=== 2. OR - under 20 OR over 22 ({len(young_or_old)} students) ===")
print(young_or_old)

# === 3. String contains ===
# .str gives you Python string methods over a whole text column at once.
# contains() is CASE-SENSITIVE by default, so "Sanjana" does not match here
# even though it has an 'a' - add case=False to ignore capitalisation.
a_names = df[df["name"].str.contains("A")]
print(f"\n=== 3. contains - names with a capital 'A' ({len(a_names)} students) ===")
print(a_names)

# === 4. Is in a list ===
# isin() replaces a chain of == joined by | - shorter and easier to read.
cities = df[df["city"].isin(["Amritsar", "Jalandhar"])]
print(f"\n=== 4. isin - Amritsar or Jalandhar ({len(cities)} students) ===")
print(cities)

# GOTCHA: always wrap EACH condition in parentheses when combining with & or |.
# Pandas operator precedence is different from Python's - & binds tighter than
# ==, so this raises a TypeError instead of filtering:
#     df[df["age"] > 20 & df["city"] == "Amritsar"]
# The parentheses are not a style choice. They are required.
