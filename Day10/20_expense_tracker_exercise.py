"""
20_expense_tracker_exercise.py - Day 10 exercise: STUDENT SCAFFOLD

TEACHES : Day 8's expense tracker with the CSV ripped out and SQLite put
          in. Same UI, same five features - a different storage layer,
          behind four helper functions.
SLIDE   : Day 10, Slide 15 - Exercise Brief (deck page 15/18)
RUN     : streamlit run 20_expense_tracker_exercise.py

EXPECTED OUTPUT IN THE BROWSER
    Right now: the title, the form, and a warning that the helpers are not
    written yet. Nothing saves.
    Once you finish the TODOs: a form that INSERTs into expenses.db, a
    total from SELECT SUM(amount), and a table from SELECT *. Stop the app
    and start it again - the rows are still there, because they are in the
    database, not in memory.

--------------------------------------------------------------------------
THE BRIEF
    Rebuild Day 8's expense tracker so it stores expenses in SQLite
    instead of a CSV file. Same UI. Different storage.

REQUIREMENTS
    [ ] An expenses table with columns: id, amount, category, date, note
    [ ] On form submit: INSERT a row
    [ ] On app load: SELECT all rows, show them in st.dataframe
    [ ] The total from SELECT SUM(amount) FROM expenses
    [ ] The helper-function pattern: open -> work -> close, one function
        per job
    [ ] ? placeholders for every value. No f-strings in SQL. Ever.

WHY HELPER FUNCTIONS, NOT ONE CONNECTION AT THE TOP
    Streamlit re-runs this entire file on every click. A connection opened
    at module level would be reused across reruns and across threads, and
    sqlite3 objects are not safe to share that way - you get
    "SQLite objects created in a thread can only be used in that same
    thread". Open inside the function, close before it returns, every
    time. That is the whole pattern.

HOW TO WORK
    Fill in one function at a time, save, and watch the browser reload.
    The UI below is already written - it calls the functions you write.
--------------------------------------------------------------------------
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# The database lives next to this file, so it does not matter which folder
# you launched streamlit from.
DB_FILE = Path(__file__).with_name("expenses.db")

CATEGORIES = ["Food", "Transport", "Books", "Rent", "Entertainment", "Other"]

# TODO 0: import sqlite3 at the top of the file, next to the other imports.
# import sqlite3


# --- Helper 1: create the table -----------------------------------------
def init_db() -> None:
    """Create the expenses table if it does not exist yet."""
    # TODO 1: connect, CREATE TABLE IF NOT EXISTS, commit, close.
    #   IF NOT EXISTS is what makes this safe to call on every rerun -
    #   and Streamlit reruns this file on every single interaction.
    # conn = sqlite3.connect(DB_FILE)
    # conn.execute(
    #     """
    #     CREATE TABLE IF NOT EXISTS expenses (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         amount REAL NOT NULL,
    #         category TEXT NOT NULL,
    #         date TEXT NOT NULL,
    #         note TEXT
    #     )
    #     """
    # )
    # conn.commit()
    # conn.close()


# --- Helper 2: insert one expense ---------------------------------------
def add_expense(amount: float, category: str, date: str, note: str) -> None:
    """INSERT one expense into the table."""
    # TODO 2: connect, INSERT with ? placeholders, commit, close.
    #   Four columns named, four ?s, four values in the tuple. Those three
    #   counts must match or you get "Incorrect number of bindings".
    #   Forget commit() and the row is silently lost.
    # conn = sqlite3.connect(DB_FILE)
    # conn.execute(
    #     "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
    #     (amount, category, date, note),
    # )
    # conn.commit()
    # conn.close()


# --- Helper 3: read every expense ---------------------------------------
def get_expenses() -> pd.DataFrame:
    """SELECT every expense, newest first, as a DataFrame."""
    # TODO 3: connect, pd.read_sql_query, close, return the DataFrame.
    #   read_sql_query does execute + fetchall + column names in one call.
    #   ORDER BY id DESC puts the newest row on top.
    # conn = sqlite3.connect(DB_FILE)
    # df = pd.read_sql_query("SELECT * FROM expenses ORDER BY id DESC", conn)
    # conn.close()
    # return df
    return pd.DataFrame(columns=["id", "amount", "category", "date", "note"])


# --- Helper 4: the total ------------------------------------------------
def get_total() -> float:
    """SELECT SUM(amount) - the grand total, as a float."""
    # TODO 4: connect, run the aggregate, fetchone, close, return.
    #   An aggregate returns ONE row, so fetchone() - then [0] for the
    #   number inside the tuple.
    #   "or 0.0" matters: SUM over an empty table returns NULL, which
    #   arrives in Python as None, and None breaks the f-string below.
    # conn = sqlite3.connect(DB_FILE)
    # result = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()
    # conn.close()
    # return result[0] or 0.0
    return 0.0


# --- The UI - already written, calls the functions above ----------------
st.title("Expense Tracker (SQLite)")

# Called on every rerun. CREATE TABLE IF NOT EXISTS makes that harmless.
init_db()

with st.form("add_expense_form", clear_on_submit=True):
    st.write("**Add an expense**")
    amount = st.number_input("Amount (Rs)", min_value=0.0, step=10.0, key="input_amount")
    category = st.selectbox("Category", CATEGORIES, key="input_category")
    # .isoformat() turns the date object into "2026-08-05". SQLite cannot
    # store a Python date directly - it would raise "type 'date' is not
    # supported" (file 19, case 5).
    date = st.date_input("Date", key="input_date").isoformat()
    note = st.text_input("Note (optional)", key="input_note")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    if amount <= 0:
        st.error("Amount must be greater than 0.")
    else:
        add_expense(amount, category, date, note)
        st.success(f"Added Rs {amount:,.2f} to {category}.")

total = get_total()
st.metric("Total Spent", f"Rs {total:,.2f}")

expenses = get_expenses()
st.dataframe(expenses)

if expenses.empty:
    st.info("No expenses yet - or the helper functions are not written yet.")

# TEST BEFORE YOU CALL IT DONE
#   Add three expenses. Stop the app (Ctrl+C). Start it again. If the rows
#   are gone, you are missing a commit() somewhere.
