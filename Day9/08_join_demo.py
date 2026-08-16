"""
08_join_demo.py - JOIN: see data from two tables at once

TEACHES : INNER JOIN vs LEFT JOIN, and the one thing that separates them -
          what happens to a student who has no expenses. Also the pandas
          parallel: this is pd.merge, run inside the database.
SLIDE   : Day 9, Slide 20 - DQL Deep-Dive, JOIN (deck page 20/25)
RUN     : python 08_join_demo.py

EXPECTED OUTPUT IN THE TERMINAL
        INNER JOIN - only students who HAVE expenses  (5 rows)
          Aarav          450.00  Food
          ... Aarav x2, Priya x2, Rahul x1. Simran is missing.
        LEFT JOIN - every student, expenses or not  (6 rows)
          ... the same 5 rows, plus:
          Simran           NULL  NULL
        Simran has no expenses. INNER JOIN drops her; LEFT JOIN keeps her
        with NULLs, which is what makes LEFT JOIN the way to FIND the gaps.

REQUIRES
    app.db - run 07_foreign_key_demo.py first. This file adds one extra
    student (Simran, no expenses) so the two JOINs differ; re-running it
    will not add her twice.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("app.db")


def add_student_without_expenses(conn: sqlite3.Connection, name: str, city: str) -> None:
    """Add a student who has no expenses - only if she is not there yet."""
    # An INNER JOIN and a LEFT JOIN return identical results until some
    # parent row has no children. Simran is that row.
    existing = conn.execute("SELECT COUNT(*) FROM students WHERE name = ?", (name,)).fetchone()[0]
    if existing == 0:
        conn.execute("INSERT INTO students (name, city) VALUES (?, ?)", (name, city))
        conn.commit()


def show_join(conn: sqlite3.Connection, label: str, query: str) -> None:
    """Run a JOIN query and print its rows, showing NULLs as NULL."""
    rows = conn.execute(query).fetchall()
    print(f"\n{label}  ({len(rows)} rows)")
    for name, amount, category in rows:
        # A student with no expenses comes back with None for the columns
        # that would have come from the expenses table.
        shown_amount = f"{amount:>8.2f}" if amount is not None else f"{'NULL':>8}"
        shown_category = category if category is not None else "NULL"
        print(f"  {name:<12} {shown_amount}  {shown_category}")


conn = sqlite3.connect(DB_FILE)
add_student_without_expenses(conn, "Simran", "Ludhiana")

# --- INNER JOIN: only rows that match in BOTH tables --------------------
# Read it as: start from students, and for each one find the expenses whose
# student_id equals its id. No match, no row in the output.
show_join(
    conn,
    "INNER JOIN - only students who HAVE expenses",
    """
    SELECT students.name, expenses.amount, expenses.category
    FROM students
    INNER JOIN expenses ON students.id = expenses.student_id
    ORDER BY students.id, expenses.id
    """,
)

# --- LEFT JOIN: every row from the LEFT table, matched or not -----------
# "Left" means the table named first, in FROM. Every student appears; the
# expense columns are filled with NULL where there was nothing to match.
show_join(
    conn,
    "LEFT JOIN - every student, expenses or not",
    """
    SELECT students.name, expenses.amount, expenses.category
    FROM students
    LEFT JOIN expenses ON students.id = expenses.student_id
    ORDER BY students.id, expenses.id
    """,
)

# --- What LEFT JOIN is actually for -------------------------------------
# Combine it with IS NULL and you have a question INNER JOIN cannot ask:
# "which students have spent nothing at all?"
print("\nLEFT JOIN + IS NULL - students with no expenses:")
for (name,) in conn.execute(
    """
    SELECT students.name
    FROM students
    LEFT JOIN expenses ON students.id = expenses.student_id
    WHERE expenses.id IS NULL
    """
):
    print(f"  {name}")

# CROSS-REF, DAY 6: this is pd.merge(students_df, expenses_df,
# left_on="id", right_on="student_id", how="inner" / how="left").
# Same operation - SQL runs it in the database instead of in Python memory.
conn.close()
