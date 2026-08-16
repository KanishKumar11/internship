"""
12_day9_exercise_solution.py - Day 9 closing exercise: INSTRUCTOR SOLUTION

TEACHES : The five queries from the brief, written out - plus the two
          details worth pointing at during the reveal: ? for values, and
          fetchone()[0] for an aggregate.
SLIDE   : Day 9, Slide 24 - Exercise Brief, 5 Queries (deck page 24/25)
          Reveal after students have tried 11_day9_exercise.py.
RUN     : python 12_day9_exercise_solution.py

EXPECTED OUTPUT IN THE TERMINAL
        Q1. All expenses          -> 20 rows
        Q2. Food expenses         -> 8 rows, 3,200.00 on food
        Q3. Unique categories     -> 5: Books, Food, Other, Rent, Transport
        Q4. 5 most recent         -> ids 20, 19, 18 (2026-08-06), 17
                                    (08-05), 16 (08-04)
        Q5. Total spent           -> 12,450.00

    These are the four numbers Day 10's recap slide (page 03/18) reads
    back to the room, so they should match what students see here.

REQUIRES
    expenses.db - run 06_create_table_demo.py first.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("expenses.db")

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# --- Q1. Show all expenses ----------------------------------------------
# SELECT * = every column. fetchall() = every row, as a list of tuples.
cursor.execute("SELECT * FROM expenses")
all_rows = cursor.fetchall()
print(f"Q1. All expenses -> {len(all_rows)} rows")
for row in all_rows[:3]:
    print(f"    {row}")
print("    ...")

# --- Q2. Only Food expenses ---------------------------------------------
# "Food" is a value, so it goes in as ?. The second argument is a TUPLE -
# ("Food",) with the trailing comma. ("Food") without it is just a string,
# and sqlite3 raises "parameters are of unsupported type".
cursor.execute("SELECT * FROM expenses WHERE category = ?", ("Food",))
food_rows = cursor.fetchall()
food_total = sum(row[1] for row in food_rows)  # column 1 is amount
print(f"\nQ2. Food expenses -> {len(food_rows)} rows, {food_total:,.2f} on food")

# --- Q3. All unique categories ------------------------------------------
# DISTINCT drops the duplicates. ORDER BY makes the list stable, which
# matters the moment you feed it to a selectbox.
cursor.execute("SELECT DISTINCT category FROM expenses ORDER BY category")
category_names = [row[0] for row in cursor.fetchall()]
print(f"\nQ3. Unique categories -> {len(category_names)}: {', '.join(category_names)}")

# --- Q4. The 5 most recent expenses -------------------------------------
# ORDER BY date DESC = newest first; LIMIT 5 stops there. Three rows share
# 2026-08-06, so id DESC is added as a tiebreak to make the output the same
# on every run - without it those three could appear in any order.
cursor.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC LIMIT 5")
recent_rows = cursor.fetchall()
print(f"\nQ4. 5 most recent expenses")
for expense_id, amount, category, date, note, _created_at in recent_rows:
    shown_note = note if note is not None else "NULL"
    print(f"    {expense_id:<4} {date}  {amount:>8.2f}  {category:<14} {shown_note}")
print(f"    Most recent: {recent_rows[0][3]}, {recent_rows[0][2]}, {recent_rows[0][1]:,.2f}")

# --- Q5. The grand total ------------------------------------------------
# An aggregate collapses the table to one row, so fetchone() - then [0] to
# get the number out of the one-element tuple.
# "or 0.0" because SUM over an empty table returns NULL, which arrives as
# None and would blow up the f-string below.
cursor.execute("SELECT SUM(amount) FROM expenses")
total_spent = cursor.fetchone()[0] or 0.0
print(f"\nQ5. Total spent -> {total_spent:,.2f}")

conn.close()
