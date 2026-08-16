"""
01_expense_tracker_exercise.py - The solo challenge: STUDENT SCAFFOLD

TEACHES : Nothing new. Day 5's form and layout, Day 6's pandas load/filter,
          Day 7's metric and bar chart - assembled into one app that you
          design yourself.
SLIDE   : Day 8, Slide 3 - The Brief (deck page 03/15)
RUN     : streamlit run 01_expense_tracker_exercise.py

EXPECTED OUTPUT IN THE BROWSER
    Right now: a title and a message saying the app is not built yet.
    Once you finish the TODOs: a form that adds an expense, a total that
    updates, a bar chart of spending by category, and a table of recent
    expenses - all still there after you stop and restart the app.

--------------------------------------------------------------------------
THE BRIEF
    Build a personal expense tracker. The five requirements below are
    fixed. The layout, the storage format and the chart type are YOUR
    decisions - brainstorm them before you write a line of code.

REQUIREMENTS - THE APP MUST
    [ ] 1. Let the user add an expense: amount, category, date, optional
           note. Submitted through the app.
    [ ] 2. Store expenses so they PERSIST between runs. Close the app,
           reopen it, the data is still there. (CSV is simplest - Day 6.)
    [ ] 3. Show the total amount spent, as one prominent number.
    [ ] 4. Visualise spending by category with a chart.
    [ ] 5. Show a list of recent expenses.

BONUS - ONLY AFTER THE CORE 5 WORK
    Filter by category or date range. Delete an expense. A line chart of
    spending over time. See 06_expense_tracker_extended.py afterwards.

YOUR DECISIONS - DECIDE THESE FIRST, ON PAPER
    Layout?        sidebar + main / top form / tabs / two columns
    Storage?       CSV / JSON / SQLite
    Categories?    a fixed dropdown list, or free text?
    Form?          st.form (one submit) or individual widgets?
    First run?     what happens when expenses.csv does not exist yet?

HOW TO WORK
    Uncomment one TODO at a time, save, and watch the browser reload.
    Fix each error before uncommenting the next one. If a TODO's shape
    does not fit YOUR design, change it - the requirements are fixed, the
    code is not.

SCOPE RULE
    Core 5 first. If they are not done by minute 45, drop the bonus.
--------------------------------------------------------------------------
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# The file every run reads from and writes to. One constant, so the name
# is never typed twice and never drifts between the load and the save.
CSV_FILE = Path("expenses.csv")

# The columns, in the order they are stored. Also used to build an empty
# DataFrame on the very first run, so the rest of the app can assume these
# columns exist even when there is not a single expense yet.
COLUMNS = ["date", "category", "amount", "note"]

# A fixed list beats free text: no "food" / "Food" / "FOOD" splitting one
# category into three, which would wreck the groupby in requirement 4.
CATEGORIES = ["Food", "Transport", "Books", "Rent", "Entertainment", "Other"]


def load_expenses() -> pd.DataFrame:
    """Read the CSV, or return an empty frame if this is the first run."""
    # TODO 1: handle the first run. On a fresh machine expenses.csv does
    #   not exist yet and pd.read_csv would raise FileNotFoundError before
    #   the page ever renders. Check first, return an empty frame instead.
    # if not CSV_FILE.exists():
    #     return pd.DataFrame(columns=COLUMNS)
    # return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=COLUMNS)


def save_expense(date, category: str, amount: float, note: str) -> None:
    """Append one expense to the CSV."""
    # TODO 2: append the new row and write the whole file back.
    #   Read what is already there, build a one-row DataFrame, concat, save.
    #   index=False or pandas writes an extra unnamed column every time.
    # new_row = pd.DataFrame(
    #     [{"date": str(date), "category": category,
    #       "amount": amount, "note": note}]
    # )
    # updated = pd.concat([load_expenses(), new_row], ignore_index=True)
    # updated.to_csv(CSV_FILE, index=False)


st.title("My Expense Tracker")

# 1. Load the data -------------------------------------------------------
# Streamlit reruns this file top to bottom on every interaction, so the
# CSV is read again each time. Fine for a few hundred rows.
df = load_expenses()

# 2. The form (Day 5) ----------------------------------------------------
# st.form batches the widgets: nothing reruns until the submit button is
# pressed, so the user fills all four fields and the app saves once.
# This scaffold puts the form in the sidebar (Layout 1 from the deck).
# Move it wherever YOUR design says it goes.
with st.sidebar:
    st.write("**Add Expense**")

    # TODO 3: build the four inputs inside a form.
    #   Every widget gets a key - the habit from Day 5.
    # with st.form("add_expense", clear_on_submit=True):
    #     amount = st.number_input("Amount", min_value=0.0, step=10.0,
    #                              key="f_amount")
    #     category = st.selectbox("Category", CATEGORIES, key="f_category")
    #     date = st.date_input("Date", key="f_date")
    #     note = st.text_input("Note (optional)", key="f_note")
    #     submitted = st.form_submit_button("Add Expense")

    # TODO 4: on submit, validate, save, and rerun.
    #   Validate: an expense of 0 is a mistake, not an expense.
    #   st.rerun() restarts the script so the table, total and chart all
    #   re-read the CSV and show the row that was just added.
    # if submitted:
    #     if amount <= 0:
    #         st.error("Amount must be greater than 0.")
    #     else:
    #         save_expense(date, category, amount, note)
    #         st.rerun()

# 3. Empty state ---------------------------------------------------------
# Before anything is added there is no total to show and nothing to chart.
# Say so and stop, rather than letting sum() print 0 and bar_chart draw an
# empty box. st.stop() ends the run here; the code below never executes.
if df.empty:
    st.info("No expenses yet. Add your first one from the sidebar.")
    st.stop()

# 4. The total (Day 7) ---------------------------------------------------
# TODO 5: one prominent number. st.metric is the Day 7 KPI card.
#   The :, in the format string turns 12450 into 12,450.
# st.metric("Total Spent", f"Rs {df['amount'].sum():,.0f}")

# 5. Spending by category (Day 6 groupby + Day 7 chart) ------------------
# TODO 6: aggregate first, then chart. bar_chart draws whatever it is
#   handed - hand it one number per category, not the 24 raw rows.
# st.write("**Spending by Category**")
# by_category = df.groupby("category")["amount"].sum()
# st.bar_chart(by_category)

# 6. Recent expenses (Day 7 table) ---------------------------------------
# TODO 7: show the most recent expenses, newest first.
#   sort_values(ascending=False) puts the newest date on top; .head(10)
#   keeps the table short. ISO dates (2026-08-04) sort correctly as text,
#   which is exactly why the CSV stores them that way.
# st.write("**Recent Expenses**")
# recent = df.sort_values("date", ascending=False).head(10)
# st.dataframe(recent)

# TEST BEFORE YOU DEMO
#   Add 3-4 expenses. Stop the app (Ctrl+C in the terminal). Start it
#   again. If the expenses are gone, requirement 2 is not done - you are
#   overwriting the file instead of appending to it.
