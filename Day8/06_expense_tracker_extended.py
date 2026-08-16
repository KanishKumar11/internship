"""
06_expense_tracker_extended.py - The bonus features, after the core 5

TEACHES : The three bonus items from the brief - filter by category and
          date range, delete an expense, and chart spending over time -
          plus the two traps they hide: a date_input range that is
          half-picked, and deleting a row by the wrong index.
SLIDE   : Day 8, Slide 3 - The Brief, BONUS box (deck page 03/15)
RUN     : streamlit run 06_expense_tracker_extended.py

EXPECTED OUTPUT IN THE BROWSER
    The Layout 1 app from file 02, plus a sidebar filter block. Unfiltered
    it reads "Total Spent  Rs 12,450" over "24 of 24 expenses", six bars,
    and a line from 27 Jul to 4 Aug.
    Tick only Food and Transport: the total drops to Rs 4,000, the table
    says "12 of 24", and the chart keeps two bars. Delete the Rs 4,500
    Rent row and the total falls to Rs 7,950 permanently - it is gone from
    the CSV.

WARNING
    The delete button really deletes, from the shared expenses.csv. Put
    the original 24 rows back with:  git checkout expenses.csv

ONLY OPEN THIS AFTER THE CORE 5 WORK. A working app with five features
beats a broken one with eight.
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


def save_all(data: pd.DataFrame) -> None:
    """Write the whole frame back to the CSV. Used by both add and delete."""
    data.to_csv(CSV_FILE, index=False)


def save_expense(date, category: str, amount: float, note: str) -> None:
    """Append one expense to the CSV, keeping everything already stored."""
    new_row = pd.DataFrame(
        [{"date": str(date), "category": category, "amount": amount, "note": note}]
    )
    save_all(pd.concat([load_expenses(), new_row], ignore_index=True))


st.title("My Expense Tracker - Extended")

df = load_expenses()

with st.sidebar:
    # --- The form (unchanged from file 02) ------------------------------
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

if df.empty:
    st.info("No expenses yet. Add your first one from the sidebar.")
    st.stop()

# Parse the date column once, here. Everything below - the range filter
# and the daily line chart - needs real dates rather than the strings the
# CSV stores, and parsing twice is how the two end up disagreeing.
dates = pd.to_datetime(df["date"])

# --- BONUS 1: filters ---------------------------------------------------
with st.sidebar:
    st.write("---")
    st.write("**Filters**")

    # A multiselect, not a selectbox: "show me Food AND Transport" is the
    # question people actually ask of an expense tracker. Default to every
    # category present, so the app starts unfiltered.
    present = sorted(df["category"].unique().tolist())
    chosen = st.multiselect("Categories", present, default=present, key="f_cats")

    # A two-date range. THE TRAP: between the two clicks Streamlit reruns
    # with a 1-tuple, so unpacking start, end = ... crashes on the click
    # that opens the picker. Handle the half-picked state instead.
    picked = st.date_input(
        "Date range",
        value=(dates.min().date(), dates.max().date()),
        key="f_range",
    )
    if len(picked) == 2:
        start, end = picked
    else:
        # Only the start date is chosen so far - leave the range open at
        # the end and let the user finish clicking.
        start, end = picked[0], dates.max().date()

# Day 6's stacking filters: start from everything, narrow once per control.
filtered = df[
    df["category"].isin(chosen)
    & (dates >= pd.Timestamp(start))
    & (dates <= pd.Timestamp(end))
]

if filtered.empty:
    st.warning("No expenses match these filters. Widen them in the sidebar.")
    st.stop()

# --- The core 5, now reading `filtered` instead of `df` -----------------
# One filtered DataFrame feeds the metric, both charts and the table, so
# every panel on the page always agrees with every other one.
col_total, col_count = st.columns(2)
col_total.metric("Total Spent", f"Rs {filtered['amount'].sum():,.0f}")
col_count.metric("Expenses", f"{len(filtered)} of {len(df)}")

st.write("**Spending by Category**")
st.bar_chart(filtered.groupby("category")["amount"].sum())

# --- BONUS 2: spending over time ---------------------------------------
# One point per day, not per expense: groupby("date") sums the three rows
# recorded on 31 July into the single spike that makes the line readable.
st.write("**Spending Over Time**")
st.line_chart(filtered.groupby("date")["amount"].sum().sort_index())

# The leftmost column of this table is the DataFrame index - the row
# numbers the delete section below selects by. Leave it visible: it is how
# the student sees that the dropdown and the table are talking about the
# same row.
st.write("**Expenses**")
st.dataframe(filtered.sort_values("date", ascending=False))

# --- BONUS 3: delete an expense ----------------------------------------
# Deleting needs to name ONE row, and "the third row of the table" is not
# a name - it changes the moment the user sorts or filters. Use the
# DataFrame's index instead: filtered is a slice of df, so it carries df's
# original row numbers, and dropping one of those hits the right row no
# matter what the table currently shows.
with st.expander("Delete an expense"):
    to_delete = st.selectbox(
        "Pick the expense to remove",
        options=filtered.index.tolist(),
        format_func=lambda i: (
            f"{df.at[i, 'date']} - {df.at[i, 'category']} - "
            f"Rs {df.at[i, 'amount']:,.0f} - {df.at[i, 'note']}"
        ),
        key="f_delete",
    )

    # Two clicks, not one. A single "Delete" button next to a dropdown is
    # one mis-click away from destroying a row with no undo.
    confirm = st.checkbox("Yes, delete this permanently", key="f_confirm")
    if st.button("Delete", key="b_delete", disabled=not confirm):
        # drop() returns a new frame; reset_index keeps the stored row
        # numbers contiguous, so the next run's indexes match the file.
        save_all(df.drop(index=to_delete).reset_index(drop=True))
        st.rerun()
