"""
11_day9_exercise.py - Day 9 closing exercise: STUDENT SCAFFOLD

TEACHES : Nothing new - this is where you use it. SELECT, WHERE, DISTINCT,
          ORDER BY + LIMIT and SUM, one per question, against a real
          database you did not build.
SLIDE   : Day 9, Slide 24 - Exercise Brief, 5 Queries (deck page 24/25)
RUN     : python 11_day9_exercise.py

EXPECTED OUTPUT IN THE TERMINAL
    Right now: the connection opens, five headings print, and every answer
    says "not written yet".
    Once you finish the TODOs: five answers, ending with a grand total of
    12,450.00.

REQUIRES
    expenses.db - 20 expense rows, already built for you. If you get
    "no such table: expenses", run 06_create_table_demo.py first.

--------------------------------------------------------------------------
THE BRIEF
    Connect to expenses.db and answer these 5 questions with SQL. One
    query per question. Print the result of each.

THE 5 QUESTIONS
    1. Show all expenses            -> how many rows are there?
    2. Show only Food expenses      -> how many Food expenses?
    3. List all unique categories   -> what categories exist?
    4. Show the 5 most recent       -> what was the most recent expense?
    5. What is the total spent?     -> what is the grand total?

RULES
    - Use WHERE, DISTINCT, ORDER BY, LIMIT and SUM - one each.
    - Use ? placeholders for any value, never an f-string.

HOW TO WORK
    Uncomment one TODO block at a time, run the file, fix the error, move
    on. The print statements are already written - you only write the
    cursor.execute() line and the fetch.
--------------------------------------------------------------------------
"""

import sqlite3
from pathlib import Path

# Path(__file__).with_name() finds expenses.db next to this script, no
# matter which folder you run python from.
DB_FILE = Path(__file__).with_name("expenses.db")

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# The table columns, for reference while you write the queries:
#   id | amount | category | date | note | created_at

# --- Question 1: show all expenses --------------------------------------
# Hint: SELECT * FROM expenses
#       fetchall() gives you a list of tuples - len() counts them.
print("Q1. All expenses")
# cursor.execute("SELECT * FROM expenses")
# all_rows = cursor.fetchall()
# print(f"  {len(all_rows)} rows")
# for row in all_rows[:3]:
#     print(f"  {row}")
print("  not written yet")

# --- Question 2: only Food expenses -------------------------------------
# Hint: SELECT * FROM expenses WHERE category = ?
#       'Food' is a VALUE, so it goes in as ? with a tuple - note the
#       trailing comma in ("Food",), which is what makes it a tuple.
print("\nQ2. Food expenses")
# cursor.execute("SELECT * FROM expenses WHERE category = ?", ("Food",))
# food_rows = cursor.fetchall()
# print(f"  {len(food_rows)} rows")
print("  not written yet")

# --- Question 3: all unique categories ----------------------------------
# Hint: SELECT DISTINCT category FROM expenses ORDER BY category
#       Each row comes back as a one-element tuple, so use row[0] to get
#       the plain string out.
print("\nQ3. Unique categories")
# cursor.execute("SELECT DISTINCT category FROM expenses ORDER BY category")
# category_rows = cursor.fetchall()
# category_names = [row[0] for row in category_rows]
# print(f"  {len(category_names)}: {', '.join(category_names)}")
print("  not written yet")

# --- Question 4: the 5 most recent expenses -----------------------------
# Hint: SELECT * FROM expenses ORDER BY date DESC LIMIT 5
#       DESC = newest first. The dates are TEXT in YYYY-MM-DD form, which
#       sorts correctly as text.
print("\nQ4. 5 most recent expenses")
# cursor.execute("SELECT * FROM expenses ORDER BY date DESC LIMIT 5")
# recent_rows = cursor.fetchall()
# for row in recent_rows:
#     print(f"  {row}")
print("  not written yet")

# --- Question 5: the grand total ----------------------------------------
# Hint: SELECT SUM(amount) FROM expenses
#       An aggregate returns ONE row, so use fetchone() - then [0] to pull
#       the number out of the tuple.
print("\nQ5. Total spent")
# cursor.execute("SELECT SUM(amount) FROM expenses")
# total = cursor.fetchone()[0]
# print(f"  {total:,.2f}")
print("  not written yet")

conn.close()

# STUCK?
#   "no such table: expenses" -> run 06_create_table_demo.py first.
#   "not enough arguments"    -> your ? count does not match your tuple.
#   TypeError on fetchone     -> fetchone() returns a tuple; you need [0].
