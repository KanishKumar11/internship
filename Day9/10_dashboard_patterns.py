"""
10_dashboard_patterns.py - The three SQL patterns every dashboard uses

TEACHES : DISTINCT (unique values, for filter dropdowns), ORDER BY + LIMIT
          (the most-recent N), and IS NULL / IS NOT NULL (finding empty
          optional fields). Together with WHERE and GROUP BY, this is the
          whole query vocabulary of a Streamlit dashboard.
SLIDE   : Day 9, Slide 22 - DQL Patterns for Dashboards (deck page 22/25)
RUN     : python 10_dashboard_patterns.py

EXPECTED OUTPUT IN THE TERMINAL
        1. DISTINCT category   -> 5 categories
           Books, Food, Other, Rent, Transport
        2. ORDER BY date DESC LIMIT 5 -> the 5 newest expenses
           (three from 2026-08-06, then 2026-08-05, then 2026-08-04)
        3. WHERE note IS NULL     -> 4 expenses with no note
        4. WHERE note IS NOT NULL -> 16 expenses with a note
        4 + 16 = 20, the whole table.

REQUIRES
    expenses.db - run 06_create_table_demo.py first.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("expenses.db")


def print_expense_rows(rows: list[tuple]) -> None:
    """Print full expense rows in a fixed-width layout."""
    for expense_id, amount, category, date, note, _created_at in rows:
        shown_note = note if note is not None else "NULL"
        print(f"  {expense_id:<4} {amount:>8.2f}  {category:<14} {date:<12} {shown_note}")


conn = sqlite3.connect(DB_FILE)

# --- 1. DISTINCT: unique values ----------------------------------------
# This is what builds a filter dropdown. Day 6 did it in pandas with
# df["category"].unique().tolist(); this is the same list, computed by the
# database. ORDER BY makes the dropdown alphabetical instead of arbitrary.
categories = conn.execute(
    "SELECT DISTINCT category FROM expenses ORDER BY category"
).fetchall()
print(f"1. SELECT DISTINCT category  ({len(categories)} categories)")
# Each row is a one-element tuple, so row[0] is the plain string - exactly
# what st.selectbox wants as its options list.
category_options = [row[0] for row in categories]
print(f"   {', '.join(category_options)}")

# --- 2. ORDER BY + LIMIT: the most recent N ----------------------------
# DESC = descending = newest first. LIMIT 5 stops after five rows, so the
# database never builds a result set bigger than the table needs.
#
# The dates are stored as TEXT in YYYY-MM-DD form, which sorts correctly as
# plain text. Store them as "06 Aug 2026" and this query silently returns
# the wrong five rows - the reason ISO format is worth insisting on.
#
# Three rows share 2026-08-06, so "the newest three" could come back in any
# order. Adding id DESC as a tiebreak makes the result identical every run.
recent = conn.execute(
    "SELECT * FROM expenses ORDER BY date DESC, id DESC LIMIT 5"
).fetchall()
print(f"\n2. ORDER BY date DESC LIMIT 5  ({len(recent)} rows)")
print_expense_rows(recent)

# --- 3. IS NULL: the optional field was left empty ----------------------
# NULL means "no value was ever stored". It is NOT the empty string '' and
# NOT 0 - and this is why you cannot test it with = . `note = NULL` matches
# nothing at all, ever. IS NULL is the only thing that works.
no_note = conn.execute("SELECT * FROM expenses WHERE note IS NULL").fetchall()
print(f"\n3. WHERE note IS NULL  ({len(no_note)} rows - the user skipped the note)")
print_expense_rows(no_note)

# --- 4. IS NOT NULL: the field was filled in ----------------------------
with_note = conn.execute("SELECT * FROM expenses WHERE note IS NOT NULL").fetchall()
print(f"\n4. WHERE note IS NOT NULL  ({len(with_note)} rows)")
print(f"   {len(no_note)} + {len(with_note)} = {len(no_note) + len(with_note)}, the whole table.")

# Proof that = does not work on NULL, which is worth showing live:
broken = conn.execute("SELECT COUNT(*) FROM expenses WHERE note = NULL").fetchone()[0]
print(f"\n   For comparison: WHERE note = NULL returns {broken} rows. Always IS NULL.")

conn.close()
