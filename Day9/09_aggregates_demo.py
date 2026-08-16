"""
09_aggregates_demo.py - Aggregates: summarize a column in one number

TEACHES : COUNT, SUM, AVG, MIN, MAX - and GROUP BY, which turns "one
          number for the whole table" into "one number per category".
          The SQL half of Day 6's df.groupby("category")["amount"].sum().
SLIDE   : Day 9, Slide 21 - DQL Deep-Dive, Aggregate Functions
          (deck page 21/25)
RUN     : python 09_aggregates_demo.py

EXPECTED OUTPUT IN THE TERMINAL
        COUNT(*)              20 expenses
        SUM(amount)           12,450.00
        AVG(amount)              622.50
        MIN / MAX                90.00 / 4,500.00
        GROUP BY category:
          Rent            4,500.00   (1 expense)
          Food            3,200.00   (8 expenses)
          Books           2,450.00   (4 expenses)
          Other           1,500.00   (2 expenses)
          Transport         800.00   (5 expenses)
        The five category totals add back up to 12,450.00.

REQUIRES
    expenses.db - run 06_create_table_demo.py first.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("expenses.db")

conn = sqlite3.connect(DB_FILE)

# THE SHAPE OF AN AGGREGATE RESULT.
# SELECT * returns many rows. An aggregate collapses them into ONE row, so
# fetchone() is the right call - and the [0] pulls the single value out of
# the one-element tuple it hands back.

# --- COUNT: how many rows? ---------------------------------------------
# COUNT(*) counts rows. COUNT(note) would count only the rows where note is
# not NULL - a useful difference, and the reason * is the safe default.
expense_count = conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
print(f"COUNT(*)              {expense_count} expenses")

# --- SUM: the total ----------------------------------------------------
total_spent = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
print(f"SUM(amount)           {total_spent:,.2f}")

# --- AVG: the mean -----------------------------------------------------
average_expense = conn.execute("SELECT AVG(amount) FROM expenses").fetchone()[0]
print(f"AVG(amount)           {average_expense:>9,.2f}")

# --- MIN and MAX in one query ------------------------------------------
# Two aggregates in one SELECT come back as one row with two columns, so
# this unpacks straight into two variables.
cheapest, most_expensive = conn.execute(
    "SELECT MIN(amount), MAX(amount) FROM expenses"
).fetchone()
print(f"MIN / MAX             {cheapest:,.2f} / {most_expensive:,.2f}")

# --- GROUP BY: one row per category ------------------------------------
# Without GROUP BY you get one number for the whole table. With it, SQLite
# splits the rows into groups by category and runs the aggregate inside
# each group - so the result is one row per distinct category.
# ORDER BY on the aggregate puts the biggest spender at the top, which is
# exactly what a dashboard wants.
print("\nGROUP BY category:")
group_query = """
    SELECT category, SUM(amount), COUNT(*)
    FROM expenses
    GROUP BY category
    ORDER BY SUM(amount) DESC
"""
for category, category_total, category_count in conn.execute(group_query):
    plural = "expense" if category_count == 1 else "expenses"
    print(f"  {category:<14} {category_total:>9,.2f}   ({category_count} {plural})")

# --- The empty-table trap ----------------------------------------------
# COUNT of nothing is 0, but SUM of nothing is NULL - which arrives in
# Python as None, and None breaks any f-string that tries to format it as
# a number. Every get_total() you write from tomorrow onwards needs the
# "or 0.0" guard for exactly this reason.
empty_sum = conn.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", ("Travel",)).fetchone()[0]
print(f"\nSUM over a category with no rows: {empty_sum}  (None, not 0 - guard it with 'or 0.0')")

conn.close()
