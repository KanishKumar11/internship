"""
05_layout_two_column.py - The same app, Layout 4: two columns

TEACHES : Form left, dashboard right, both in the main area and both on
          screen at once. st.columns([1, 2]) gives the dashboard twice the
          width, because a chart needs the room and a form does not.
SLIDE   : Day 8, Slide 8 - Layout 4, Two-Column (deck page 08/15)
RUN     : streamlit run 05_layout_two_column.py

EXPECTED OUTPUT IN THE BROWSER
    A narrow left column with the four form fields stacked, and a wide
    right column reading "Total Spent  Rs 12,450" over the six-bar
    category chart and a five-row table.
    Add an expense and the right column updates without the form ever
    leaving the screen.

NOTE
    Same expenses.csv as the other apps in this folder. Widen the browser
    window before demoing - at phone width Streamlit stacks the columns
    and the layout collapses into Layout 2.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

CSV_FILE = Path("expenses.csv")
COLUMNS = ["date", "category", "amount", "note"]
CATEGORIES = ["Food", "Transport", "Books", "Rent", "Entertainment", "Other"]


def load_expenses() -> pd.DataFrame:
    """Read the CSV, or return an empty frame if this is the first run."""
    if not CSV_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(CSV_FILE)


def save_expense(date, category: str, amount: float, note: str) -> None:
    """Append one expense to the CSV, keeping everything already stored."""
    new_row = pd.DataFrame(
        [{"date": str(date), "category": category, "amount": amount, "note": note}]
    )
    updated = pd.concat([load_expenses(), new_row], ignore_index=True)
    updated.to_csv(CSV_FILE, index=False)


st.title("My Expense Tracker")

df = load_expenses()

# The ratio, not a plain st.columns(2). A form of four short fields does
# not need half the page; a bar chart and a table do.
col_form, col_dash = st.columns([1, 2])

# --- Left column: the form ---------------------------------------------
with col_form:
    st.write("**Add Expense**")
    with st.form("add_expense", clear_on_submit=True):
        amount = st.number_input("Amount (Rs)", min_value=0.0, step=10.0, key="f_amount")
        category = st.selectbox("Category", CATEGORIES, key="f_category")
        date = st.date_input("Date", key="f_date")
        note = st.text_input("Note (optional)", key="f_note")
        submitted = st.form_submit_button("Add Expense")

    if submitted:
        if amount <= 0:
            st.error("Amount must be greater than 0.")
        else:
            save_expense(date, category, amount, note)
            st.rerun()

# --- Right column: the dashboard ---------------------------------------
with col_dash:
    if df.empty:
        # The empty-state guard lives inside the column here. st.stop()
        # would work too, but it would kill the whole script - and on the
        # first run the form in the left column has already rendered, so
        # there is nothing left to protect. A plain else reads clearer.
        st.info("No expenses yet. Add your first one on the left.")
    else:
        st.metric("Total Spent", f"Rs {df['amount'].sum():,.0f}")

        st.write("**By Category**")
        st.bar_chart(df.groupby("category")["amount"].sum())

        # Five rows, not ten: the column is narrower and the table sits
        # below a chart, so keep it short enough to see without scrolling.
        st.write("**Recent**")
        st.dataframe(df.sort_values("date", ascending=False).head(5))
