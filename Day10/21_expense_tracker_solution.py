"""
21_expense_tracker_solution.py - Day 10 exercise: INSTRUCTOR SOLUTION

TEACHES : The four-helper pattern in full - init_db, add_expense,
          get_expenses, get_total - each opening and closing its own
          connection, each using ? placeholders.
SLIDE   : Day 10, Slide 16 - Solution Walkthrough (deck page 16/18)
          Reveal after students have tried file 20.
RUN     : streamlit run 21_expense_tracker_solution.py

EXPECTED OUTPUT IN THE BROWSER
    "Total Spent  Rs 1,250.00" over a three-row table (Lunch with team,
    Auto to college, Python textbook) if 15_sqlite_full_pattern.py has
    been run.
    Add an expense of 500: the metric becomes Rs 1,750.00 and the new row
    appears at the top, because the table is ordered by id DESC.
    Stop the app and start it again - the row is still there. That is the
    upgrade over Day 8: no CSV, no read-modify-write, real persistence.

NOTE
    Shares expenses.db with files 16-19. Reset it any time by running
    python 15_sqlite_full_pattern.py.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd
import streamlit as st

DB_FILE = Path(__file__).with_name("expenses.db")

CATEGORIES = ["Food", "Transport", "Books", "Rent", "Entertainment", "Other"]

# The deck's brand palette, so the chart and the app agree with the slides.
COLOR_CORAL = "#FF6B5B"
COLOR_PRIMARY = "#2A3284"


def init_db() -> None:
    """Create the expenses table if it does not exist yet."""
    # closing() guarantees the connection is closed even if the CREATE
    # raises - see file 17. `with conn:` handles the commit.
    with closing(sqlite3.connect(DB_FILE)) as conn:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    note TEXT
                )
                """
            )
    # IF NOT EXISTS is doing real work here: Streamlit reruns this whole
    # file on every click, so this function runs dozens of times a session.


def add_expense(amount: float, category: str, date: str, note: str) -> None:
    """INSERT one expense."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        with conn:
            # ? placeholders, always. The note comes straight from a text
            # box the user typed into - the one place an f-string here
            # would be a genuine SQL-injection hole.
            conn.execute(
                "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
                (amount, category, date, note),
            )


def get_expenses() -> pd.DataFrame:
    """SELECT every expense, newest first, as a DataFrame."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        # read_sql_query replaces execute + fetchall + rebuilding the
        # column names by hand. ORDER BY id DESC = newest at the top.
        return pd.read_sql_query("SELECT * FROM expenses ORDER BY id DESC", conn)


def get_total() -> float:
    """SELECT SUM(amount) - the grand total."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        result = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()
    # SUM over an empty table is NULL, which arrives as None. Without the
    # "or 0.0" the very first run of a fresh app crashes on the f-string
    # that formats this number.
    return result[0] or 0.0


def get_category_totals() -> pd.DataFrame:
    """SELECT category, SUM(amount) GROUP BY category - for the chart."""
    with closing(sqlite3.connect(DB_FILE)) as conn:
        # SQL does the aggregating; pandas only carries the 6-row result to
        # the chart. AS total names the column so the chart legend reads
        # "total" rather than "SUM(amount)".
        return pd.read_sql_query(
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
            """,
            conn,
        )


st.title("Expense Tracker (SQLite)")

# Runs on every rerun, and is a no-op after the first one.
init_db()

with st.form("add_expense_form", clear_on_submit=True):
    st.write("**Add an expense**")
    amount = st.number_input("Amount (Rs)", min_value=0.0, step=10.0, key="input_amount")
    category = st.selectbox("Category", CATEGORIES, key="input_category")
    # .isoformat() -> "2026-08-05". SQLite cannot bind a Python date
    # object; storing ISO text also keeps ORDER BY date working correctly.
    date = st.date_input("Date", key="input_date").isoformat()
    note = st.text_input("Note (optional)", key="input_note")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    if amount <= 0:
        st.error("Amount must be greater than 0.")
    else:
        add_expense(amount, category, date, note)
        st.success(f"Added Rs {amount:,.2f} to {category}.")

# Read AFTER the insert, so the metric and the table include the new row on
# this same rerun. Put these two lines above the form and the page would be
# one interaction out of date.
st.metric("Total Spent", f"Rs {get_total():,.2f}")

expenses = get_expenses()
if expenses.empty:
    st.info("No expenses yet. Add your first one above.")
else:
    st.write("**Spending by Category**")
    st.bar_chart(get_category_totals(), x="category", y="total", color=COLOR_CORAL)

    st.write("**All Expenses**")
    st.dataframe(expenses)

# THE UPGRADE OVER DAY 8
#   Day 8: read the whole CSV, append a row in pandas, write the whole file
#          back. Every save rewrote every row.
#   Today: one INSERT. The database handles the rest - and SUM, GROUP BY
#          and ORDER BY run inside it instead of in Python.
